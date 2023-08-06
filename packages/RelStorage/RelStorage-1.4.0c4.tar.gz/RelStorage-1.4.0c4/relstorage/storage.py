##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""The core of RelStorage, a ZODB storage for relational databases.

Stores pickles in the database.
"""

from persistent.TimeStamp import TimeStamp
from relstorage.cache import StorageCache
from relstorage.options import Options
from relstorage.util import is_blob_record
from ZODB.BaseStorage import DataRecord
from ZODB.BaseStorage import TransactionRecord
from ZODB import ConflictResolution
from ZODB import POSException
from ZODB.POSException import POSKeyError
from ZODB.UndoLogCompatible import UndoLogCompatible
from ZODB.utils import p64
from ZODB.utils import u64
from zope.interface import implements
from zope.interface import Interface
import base64
import cPickle
import logging
import os
import sys
import tempfile
import threading
import time
import weakref
import ZODB.interfaces

try:
    from ZODB.interfaces import StorageStopIteration
except ImportError:
    class StorageStopIteration(IndexError, StopIteration):
        """A combination of StopIteration and IndexError to provide a
        backwards-compatible exception.
        """

_relstorage_interfaces = []
for name in (
    'IStorage',
    'IMVCCStorage',
    'IStorageRestoreable',
    'IStorageIteration',
    'IStorageUndoable',
    'IBlobStorage',
    'IBlobStorageRestoreable',
    ):
    if hasattr(ZODB.interfaces, name):
        _relstorage_interfaces.append(getattr(ZODB.interfaces, name))

log = logging.getLogger("relstorage")

# Set the RELSTORAGE_ABORT_EARLY environment variable when debugging
# a failure revealed by the ZODB test suite.  The test suite often fails
# to call tpc_abort in the event of an error, leading to deadlocks.
# This variable causes RelStorage to abort failed transactions
# early rather than wait for an explicit abort.
abort_early = os.environ.get('RELSTORAGE_ABORT_EARLY')


class RelStorage(
        UndoLogCompatible,
        ConflictResolution.ConflictResolvingStorage
        ):
    """Storage to a relational database, based on invalidation polling"""
    implements(*_relstorage_interfaces)

    _transaction=None # Transaction that is being committed
    _tstatus=' '      # Transaction status, used for copying data
    _is_read_only = False

    # load_conn and load_cursor are open most of the time.
    _load_conn = None
    _load_cursor = None
    _load_transaction_open = False

    # store_conn and store_cursor are open during commit,
    # but not necessarily open at other times.
    _store_conn = None
    _store_cursor = None

    # _tid is the current transaction ID being committed; generally
    # only set after tpc_vote().
    _tid = None

    # _ltid is the ID of the last transaction committed by this instance.
    _ltid = None

    # _prepared_txn is the name of the transaction to commit in the
    # second phase.
    _prepared_txn = None

    # _closed is True after self.close() is called.  Since close()
    # can be called from another thread, access to self._closed should
    # be inside a _lock_acquire()/_lock_release() block.
    _closed = False

    # _max_stored_oid is the highest OID stored by the current
    # transaction
    _max_stored_oid = 0

    # _max_new_oid is the highest OID provided by new_oid()
    _max_new_oid = 0

    # _cache, if set, is a StorageCache object.
    _cache = None

    # _prev_polled_tid contains the tid at the previous poll
    _prev_polled_tid = None

    # _poll_at is the time to force a poll
    _poll_at = 0

    # If the blob directory is set, fshelper is a filesystem blob
    # helper.  Otherwise, fshelper is None.
    fshelper = None

    # _txn_blobs: {oid->filename}; contains blob data for the
    # currently uncommitted transaction.
    _txn_blobs = None

    # _batcher: An object that accumulates store operations
    # so they can be executed in batch (to minimize latency).
    _batcher = None

    # _batcher_row_limit: The number of rows to queue before
    # calling the database.
    _batcher_row_limit = 100

    def __init__(self, adapter, name=None, create=True,
            options=None, cache=None, **kwoptions):
        self._adapter = adapter

        if options is None:
            options = Options(**kwoptions)
        elif kwoptions:
            raise TypeError("The RelStorage constructor accepts either "
                "an options parameter or keyword arguments, not both")
        self._options = options

        if not name:
            name = options.name
            if not name:
                name = 'RelStorage: %s' % adapter
        self.__name__ = name

        self._is_read_only = options.read_only

        if create:
            self._adapter.schema.prepare()

        self._open_load_connection()

        self.__lock = threading.RLock()
        self.__commit_lock = threading.Lock()
        self._lock_acquire = self.__lock.acquire
        self._lock_release = self.__lock.release
        self._commit_lock_acquire = self.__commit_lock.acquire
        self._commit_lock_release = self.__commit_lock.release

        # _instances is a list of weak references to storage instances bound
        # to the same database.
        self._instances = []

        # _preallocated_oids contains OIDs provided by the database
        # but not yet used.
        self._preallocated_oids = []

        if cache is not None:
            self._cache = cache
        else:
            self._cache = StorageCache(adapter, options)

        if options.blob_dir:
            from ZODB.blob import FilesystemHelper
            self.fshelper = FilesystemHelper(options.blob_dir)
            if create:
                self.fshelper.create()
                self.fshelper.checkSecure()

    def _open_load_connection(self):
        """Open the load connection to the database.  Return nothing."""
        conn, cursor = self._adapter.connmanager.open_for_load()
        self._drop_load_connection()
        self._load_conn, self._load_cursor = conn, cursor
        self._load_transaction_open = True

    def _drop_load_connection(self):
        """Unconditionally drop the load connection"""
        conn, cursor = self._load_conn, self._load_cursor
        self._load_conn, self._load_cursor = None, None
        self._adapter.connmanager.close(conn, cursor)
        self._load_transaction_open = False

    def _rollback_load_connection(self):
        if self._load_conn is not None:
            try:
                self._load_conn.rollback()
            except:
                self._drop_load_connection()
                raise
            self._load_transaction_open = False

    def _restart_load_and_call(self, f, *args, **kw):
        """Restart the load connection and call a function.

        The first two function parameters are the load connection and cursor.
        """
        if self._load_cursor is None:
            need_restart = False
            self._open_load_connection()
        else:
            need_restart = True
        try:
            if need_restart:
                self._adapter.connmanager.restart_load(
                    self._load_conn, self._load_cursor)
                self._load_transaction_open = True
            return f(self._load_conn, self._load_cursor, *args, **kw)
        except self._adapter.connmanager.disconnected_exceptions, e:
            log.warning("Reconnecting load_conn: %s", e)
            self._drop_load_connection()
            try:
                self._open_load_connection()
            except:
                log.exception("Reconnect failed.")
                raise
            log.info("Reconnected.")
            return f(self._load_conn, self._load_cursor, *args, **kw)

    def _open_store_connection(self):
        """Open the store connection to the database.  Return nothing."""
        conn, cursor = self._adapter.connmanager.open_for_store()
        self._drop_store_connection()
        self._store_conn, self._store_cursor = conn, cursor

    def _drop_store_connection(self):
        """Unconditionally drop the store connection"""
        conn, cursor = self._store_conn, self._store_cursor
        self._store_conn, self._store_cursor = None, None
        self._adapter.connmanager.close(conn, cursor)

    def _restart_store(self):
        """Restart the store connection, creating a new connection if needed"""
        if self._store_cursor is None:
            self._open_store_connection()
            return
        try:
            self._adapter.connmanager.restart_store(
                self._store_conn, self._store_cursor)
        except self._adapter.connmanager.disconnected_exceptions, e:
            log.warning("Reconnecting store_conn: %s", e)
            self._drop_store_connection()
            try:
                self._open_store_connection()
            except:
                log.exception("Reconnect failed.")
                raise
            else:
                log.info("Reconnected.")

    def _with_store(self, f, *args, **kw):
        """Call a function with the store connection and cursor."""
        if self._store_cursor is None:
            self._open_store_connection()
        try:
            return f(self._store_conn, self._store_cursor, *args, **kw)
        except self._adapter.connmanager.disconnected_exceptions, e:
            if self._transaction is not None:
                # If transaction commit is in progress, it's too late
                # to reconnect.
                raise
            log.warning("Reconnecting store_conn: %s", e)
            self._drop_store_connection()
            try:
                self._open_store_connection()
            except:
                log.exception("Reconnect failed.")
                raise
            log.info("Reconnected.")
            return f(self._store_conn, self._store_cursor, *args, **kw)

    def zap_all(self):
        """Clear all objects and transactions out of the database.

        Used by the test suite and the ZODBConvert script.
        """
        self._adapter.schema.zap_all()
        self._rollback_load_connection()
        self._cache.clear()

    def release(self):
        """Release back end database sessions used by this storage instance.
        """
        self._lock_acquire()
        try:
            self._drop_load_connection()
            self._drop_store_connection()
        finally:
            self._lock_release()

    def close(self):
        """Close the storage and all instances."""
        self._lock_acquire()
        try:
            self._closed = True
            self._drop_load_connection()
            self._drop_store_connection()
            for wref in self._instances:
                instance = wref()
                if instance is not None:
                    instance.close()
        finally:
            self._lock_release()

    def new_instance(self):
        """Creates and returns another storage instance.

        See ZODB.interfaces.IMVCCStorage.
        """
        adapter = self._adapter.new_instance()
        cache = self._cache.new_instance()
        other = RelStorage(adapter=adapter, name=self.__name__,
            create=False, options=self._options, cache=cache)
        self._instances.append(weakref.ref(other))
        return other

    def __len__(self):
        return self._adapter.stats.get_object_count()

    def sortKey(self):
        """Return a string that can be used to sort storage instances.

        The key must uniquely identify a storage and must be the same
        across multiple instantiations of the same storage.
        """
        return self.__name__

    def getName(self):
        return self.__name__

    def getSize(self):
        """Return database size in bytes"""
        return self._adapter.stats.get_db_size()

    def registerDB(self, db, limit=None):
        pass # we don't care

    def isReadOnly(self):
        return self._is_read_only

    def abortVersion(self, src, transaction):
        # this method is only here for b/w compat with ZODB 3.7
        if transaction is not self._transaction:
            raise POSException.StorageTransactionError(self, transaction)
        return self._tid, []

    def commitVersion(self, src, dest, transaction):
        # this method is only here for b/w compat with ZODB 3.7
        if transaction is not self._transaction:
            raise POSException.StorageTransactionError(self, transaction)
        return self._tid, []

    def getExtensionMethods(self):
        # this method is only here for b/w compat with ZODB 3.7
        return {}

    def versionEmpty(self, version):
        # this method is only here for b/w compat with ZODB 3.7
        return 1

    def versions(self, max=None):
        # this method is only here for b/w compat with ZODB 3.7
        return ()

    def _log_keyerror(self, oid_int, reason):
        """Log just before raising POSKeyError in load().

        KeyErrors in load() are generally not supposed to happen,
        so this is a good place to gather information.
        """
        cursor = self._load_cursor
        adapter = self._adapter
        logfunc = log.warning
        msg = ["POSKeyError on oid %d: %s" % (oid_int, reason)]

        if adapter.keep_history:
            rows = adapter.dbiter.iter_transactions(cursor)
            row = None
            for row in rows:
                # just get the first row
                break
            if not row:
                # This happens when initializing a new database or
                # after packing, so it's not a warning.
                logfunc = log.debug
                msg.append("No previous transactions exist")
            else:
                msg.append("Current transaction is %d" % row[0])

            tids = []
            try:
                rows = adapter.dbiter.iter_object_history(cursor, oid_int)
            except KeyError:
                # The object has no history, at least from the point of view
                # of the current database load connection.
                pass
            else:
                for row in rows:
                    tids.append(row[0])
                    if len(tids) >= 10:
                        break
            msg.append("Recent object tids: %s" % repr(tids))

        else:
            if oid_int == 0:
                # This happens when initializing a new database or
                # after packing, so it's usually not a warning.
                logfunc = log.debug
            msg.append("history-free adapter")

        logfunc('; '.join(msg))

    def load(self, oid, version):
        oid_int = u64(oid)
        cache = self._cache

        self._lock_acquire()
        try:
            if not self._load_transaction_open:
                self._restart_load_and_poll()
            cursor = self._load_cursor
            state, tid_int = cache.load(cursor, oid_int)
        finally:
            self._lock_release()

        if tid_int is not None:
            if not state:
                # This can happen if something attempts to load
                # an object whose creation has been undone.
                self._log_keyerror(oid_int, "creation has been undone")
                raise POSKeyError(oid)
            state = str(state or '')
            return state, p64(tid_int)
        else:
            self._log_keyerror(oid_int, "no tid found")
            raise POSKeyError(oid)

    def getTid(self, oid):
        state, serial = self.load(oid, '')
        return serial

    getSerial = getTid  # ZODB 3.7

    def loadEx(self, oid, version):
        # Since we don't support versions, just tack the empty version
        # string onto load's result.
        return self.load(oid, version) + ("",)

    def loadSerial(self, oid, serial):
        """Load a specific revision of an object"""
        oid_int = u64(oid)
        tid_int = u64(serial)

        self._lock_acquire()
        try:
            if not self._load_transaction_open:
                self._restart_load_and_poll()
            state = self._adapter.mover.load_revision(
                self._load_cursor, oid_int, tid_int)
            if state is None and self._store_cursor is not None:
                # Allow loading data from later transactions
                # for conflict resolution.
                state = self._adapter.mover.load_revision(
                    self._store_cursor, oid_int, tid_int)
        finally:
            self._lock_release()

        if state is not None:
            state = str(state)
            if not state:
                raise POSKeyError(oid)
            return state
        else:
            raise POSKeyError(oid)

    def loadBefore(self, oid, tid):
        """Return the most recent revision of oid before tid committed."""
        oid_int = u64(oid)

        self._lock_acquire()
        try:
            if self._store_cursor is not None:
                # Allow loading data from later transactions
                # for conflict resolution.
                cursor = self._store_cursor
            else:
                if not self._load_transaction_open:
                    self._restart_load_and_poll()
                cursor = self._load_cursor
            if not self._adapter.mover.exists(cursor, u64(oid)):
                raise POSKeyError(oid)

            state, start_tid = self._adapter.mover.load_before(
                cursor, oid_int, u64(tid))
            if start_tid is not None:
                end_int = self._adapter.mover.get_object_tid_after(
                    cursor, oid_int, start_tid)
                if end_int is not None:
                    end = p64(end_int)
                else:
                    end = None
                if state is not None:
                    state = str(state)
                return state, p64(start_tid), end
            else:
                return None
        finally:
            self._lock_release()


    def store(self, oid, serial, data, version, transaction):
        if self._is_read_only:
            raise POSException.ReadOnlyError()
        if transaction is not self._transaction:
            raise POSException.StorageTransactionError(self, transaction)
        if version:
            raise POSException.Unsupported("Versions aren't supported")

        # If self._prepared_txn is not None, that means something is
        # attempting to store objects after the vote phase has finished.
        # That should not happen, should it?
        assert self._prepared_txn is None

        adapter = self._adapter
        cache = self._cache
        cursor = self._store_cursor
        assert cursor is not None
        oid_int = u64(oid)
        if serial:
            prev_tid_int = u64(serial)
        else:
            prev_tid_int = 0

        self._lock_acquire()
        try:
            self._max_stored_oid = max(self._max_stored_oid, oid_int)
            # save the data in a temporary table
            adapter.mover.store_temp(
                cursor, self._batcher, oid_int, prev_tid_int, data)
            cache.store_temp(oid_int, data)
            return None
        finally:
            self._lock_release()


    def restore(self, oid, serial, data, version, prev_txn, transaction):
        # Like store(), but used for importing transactions.  See the
        # comments in FileStorage.restore().  The prev_txn optimization
        # is not used.
        if self._is_read_only:
            raise POSException.ReadOnlyError()
        if transaction is not self._transaction:
            raise POSException.StorageTransactionError(self, transaction)
        if version:
            raise POSException.Unsupported("Versions aren't supported")

        assert self._tid is not None
        assert self._prepared_txn is None

        adapter = self._adapter
        cursor = self._store_cursor
        assert cursor is not None
        oid_int = u64(oid)
        tid_int = u64(serial)

        self._lock_acquire()
        try:
            self._max_stored_oid = max(self._max_stored_oid, oid_int)
            # save the data.  Note that data can be None.
            adapter.mover.restore(
                cursor, self._batcher, oid_int, tid_int, data)
        finally:
            self._lock_release()


    def tpc_begin(self, transaction, tid=None, status=' '):
        if self._is_read_only:
            raise POSException.ReadOnlyError()
        self._lock_acquire()
        try:
            if self._transaction is transaction:
                if self._options.strict_tpc:
                    raise POSException.StorageTransactionError(
                        "Duplicate tpc_begin calls for same transaction")
                return
            self._lock_release()
            self._commit_lock_acquire()
            self._lock_acquire()
            self._clear_temp()
            self._transaction = transaction

            user = str(transaction.user)
            desc = str(transaction.description)
            ext = transaction._extension
            if ext:
                ext = cPickle.dumps(ext, 1)
            else:
                ext = ""
            self._ude = user, desc, ext
            self._tstatus = status

            self._restart_store()
            adapter = self._adapter
            self._cache.tpc_begin()
            self._batcher = self._adapter.mover.make_batcher(
                self._store_cursor, self._batcher_row_limit)

            if tid is not None:
                # hold the commit lock and add the transaction now
                cursor = self._store_cursor
                packed = (status == 'p')
                adapter.locker.hold_commit_lock(cursor, ensure_current=True)
                tid_int = u64(tid)
                try:
                    adapter.txncontrol.add_transaction(
                        cursor, tid_int, user, desc, ext, packed)
                except:
                    self._drop_store_connection()
                    raise
            # else choose the tid later
            self._tid = tid

        finally:
            self._lock_release()

    def tpc_transaction(self):
        return self._transaction

    def _prepare_tid(self):
        """Choose a tid for the current transaction.

        This should be done as late in the commit as possible, since
        it must hold an exclusive commit lock.
        """
        if self._tid is not None:
            return
        if self._transaction is None:
            raise POSException.StorageError("No transaction in progress")

        adapter = self._adapter
        cursor = self._store_cursor
        adapter.locker.hold_commit_lock(cursor, ensure_current=True)
        user, desc, ext = self._ude

        # Choose a transaction ID.
        # Base the transaction ID on the current time,
        # but ensure that the tid of this transaction
        # is greater than any existing tid.
        last_tid = adapter.txncontrol.get_tid(cursor)
        now = time.time()
        stamp = TimeStamp(*(time.gmtime(now)[:5] + (now % 60,)))
        stamp = stamp.laterThan(TimeStamp(p64(last_tid)))
        tid = repr(stamp)

        tid_int = u64(tid)
        adapter.txncontrol.add_transaction(cursor, tid_int, user, desc, ext)
        self._tid = tid


    def _clear_temp(self):
        # Clear all attributes used for transaction commit.
        # It is assumed that self._lock_acquire was called before this
        # method was called.
        self._transaction = None
        self._ude = None
        self._tid = None
        self._prepared_txn = None
        self._max_stored_oid = 0
        self._batcher = None
        self._txn_blobs = None
        self._cache.clear_temp()


    def _finish_store(self):
        """Move stored objects from the temporary table to final storage.

        Returns a list of (oid, tid) to be received by
        Connection._handle_serial().
        """
        assert self._tid is not None
        cursor = self._store_cursor
        adapter = self._adapter
        cache = self._cache

        # Detect conflicting changes.
        # Try to resolve the conflicts.
        resolved = set()  # a set of OIDs
        while True:
            conflict = adapter.mover.detect_conflict(cursor)
            if conflict is None:
                break

            oid_int, prev_tid_int, serial_int, data = conflict
            oid = p64(oid_int)
            prev_tid = p64(prev_tid_int)
            serial = p64(serial_int)

            rdata = self.tryToResolveConflict(oid, prev_tid, serial, data)
            if rdata is None:
                # unresolvable; kill the whole transaction
                raise POSException.ConflictError(
                    oid=oid, serials=(prev_tid, serial), data=data)
            else:
                # resolved
                data = rdata
                self._adapter.mover.replace_temp(
                    cursor, oid_int, prev_tid_int, data)
                resolved.add(oid)
                cache.store_temp(oid_int, data)

        # Move the new states into the permanent table
        tid_int = u64(self._tid)
        serials = []
        oid_ints = adapter.mover.move_from_temp(cursor, tid_int)
        for oid_int in oid_ints:
            oid = p64(oid_int)
            if oid in resolved:
                serial = ConflictResolution.ResolvedSerial
            else:
                serial = self._tid
            serials.append((oid, serial))

        return serials


    def tpc_vote(self, transaction):
        self._lock_acquire()
        try:
            if transaction is not self._transaction:
                if self._options.strict_tpc:
                    raise POSException.StorageTransactionError(
                        "tpc_vote called with wrong transaction")
                return
            try:
                return self._vote()
            except:
                if abort_early:
                    # abort early to avoid lockups while running the
                    # somewhat brittle ZODB test suite
                    self.tpc_abort(transaction)
                raise
        finally:
            self._lock_release()

    def _vote(self):
        """Prepare the transaction for final commit."""
        # This method initiates a two-phase commit process,
        # saving the name of the prepared transaction in self._prepared_txn.

        # It is assumed that self._lock_acquire was called before this
        # method was called.

        if self._prepared_txn is not None:
            # the vote phase has already completed
            return

        cursor = self._store_cursor
        assert cursor is not None
        conn = self._store_conn

        # execute all remaining batch store operations
        self._batcher.flush()

        # Reserve all OIDs used by this transaction
        if self._max_stored_oid > self._max_new_oid:
            self._adapter.oidallocator.set_min_oid(
                cursor, self._max_stored_oid + 1)

        self._prepare_tid()
        tid_int = u64(self._tid)

        serials = self._finish_store()
        self._adapter.mover.update_current(cursor, tid_int)
        self._prepared_txn = self._adapter.txncontrol.commit_phase1(
            conn, cursor, tid_int)

        if self._txn_blobs:
            # We now have a transaction ID, so rename all the blobs
            # accordingly.
            for oid, sourcename in self._txn_blobs.items():
                targetname = self.fshelper.getBlobFilename(oid, self._tid)
                if sourcename != targetname:
                    ZODB.blob.rename_or_copy_blob(sourcename, targetname)
                    self._txn_blobs[oid] = targetname

        return serials


    def tpc_finish(self, transaction, f=None):
        self._lock_acquire()
        try:
            if transaction is not self._transaction:
                if self._options.strict_tpc:
                    raise POSException.StorageTransactionError(
                        "tpc_finish called with wrong transaction")
                return
            try:
                try:
                    if f is not None:
                        f(self._tid)
                    u, d, e = self._ude
                    self._finish(self._tid, u, d, e)
                finally:
                    self._clear_temp()
            finally:
                self._commit_lock_release()
        finally:
            self._lock_release()


    def _finish(self, tid, user, desc, ext):
        """Commit the transaction."""
        # It is assumed that self._lock_acquire was called before this
        # method was called.
        assert self._tid is not None
        self._rollback_load_connection()
        txn = self._prepared_txn
        assert txn is not None
        self._adapter.txncontrol.commit_phase2(
            self._store_conn, self._store_cursor, txn)
        self._adapter.locker.release_commit_lock(self._store_cursor)
        self._cache.after_tpc_finish(self._tid)

        # N.B. only set _ltid after the commit succeeds,
        # including cache updates.
        self._ltid = self._tid

        #if self._txn_blobs and not self._adapter.keep_history:
            ## For each blob just committed, get the name of
            ## one earlier revision (if any) and write the
            ## name of the file to a log.  At pack time,
            ## all the files in the log will be deleted and
            ## the log will be cleared.
            #for oid, filename in self._txn_blobs.iteritems():
                #dirname, current_name = os.path.split(filename)
                #names = os.listdir(dirname)
                #names.sort()
                #if current_name in names:
                    #i = names.index(current_name)
                    #if i > 0:
                    #    to_delete = os.path.join(dirname, names[i-1])
                    #    log.write('%s\n') % to_delete


    def tpc_abort(self, transaction):
        self._lock_acquire()
        try:
            if transaction is not self._transaction:
                return
            try:
                try:
                    self._abort()
                finally:
                    self._clear_temp()
            finally:
                self._commit_lock_release()
        finally:
            self._lock_release()

    def _abort(self):
        # the lock is held here
        self._rollback_load_connection()
        if self._store_cursor is not None:
            self._adapter.txncontrol.abort(
                self._store_conn, self._store_cursor, self._prepared_txn)
            self._adapter.locker.release_commit_lock(self._store_cursor)
        if self._txn_blobs:
            for oid, filename in self._txn_blobs.iteritems():
                if os.path.exists(filename):
                    ZODB.blob.remove_committed(filename)
                    dirname = os.path.dirname(filename)
                    if not os.listdir(dirname):
                        ZODB.blob.remove_committed_dir(dirname)


    def lastTransaction(self):
        return self._ltid

    def new_oid(self):
        if self._is_read_only:
            raise POSException.ReadOnlyError()
        self._lock_acquire()
        try:
            if self._preallocated_oids:
                oid_int = self._preallocated_oids.pop()
            else:
                def f(conn, cursor):
                    return list(self._adapter.oidallocator.new_oids(cursor))
                preallocated = self._with_store(f)
                preallocated.sort(reverse=True)
                oid_int = preallocated.pop()
                self._preallocated_oids = preallocated
            self._max_new_oid = max(self._max_new_oid, oid_int)
            return p64(oid_int)
        finally:
            self._lock_release()

    def cleanup(self):
        pass

    def supportsVersions(self):
        return False

    def modifiedInVersion(self, oid):
        return ''

    def supportsUndo(self):
        return self._adapter.keep_history

    def supportsTransactionalUndo(self):
        return self._adapter.keep_history

    def undoLog(self, first=0, last=-20, filter=None):
        if last < 0:
            last = first - last

        # use a private connection to ensure the most current results
        adapter = self._adapter
        conn, cursor = adapter.connmanager.open()
        try:
            rows = adapter.dbiter.iter_transactions(cursor)
            i = 0
            res = []
            for tid_int, user, desc, ext in rows:
                tid = p64(tid_int)
                d = {'id': base64.encodestring(tid)[:-1],
                     'time': TimeStamp(tid).timeTime(),
                     'user_name': user or '',
                     'description': desc or ''}
                if ext:
                    d.update(cPickle.loads(ext))
                if filter is None or filter(d):
                    if i >= first:
                        res.append(d)
                    i += 1
                    if i >= last:
                        break
            return res

        finally:
            adapter.connmanager.close(conn, cursor)

    def history(self, oid, version=None, size=1, filter=None):
        self._lock_acquire()
        try:
            cursor = self._load_cursor
            oid_int = u64(oid)
            try:
                rows = self._adapter.dbiter.iter_object_history(
                    cursor, oid_int)
            except KeyError:
                raise POSKeyError(oid)

            res = []
            for tid_int, username, description, extension, length in rows:
                tid = p64(tid_int)
                if extension:
                    d = loads(extension)
                else:
                    d = {}
                d.update({"time": TimeStamp(tid).timeTime(),
                          "user_name": username or '',
                          "description": description or '',
                          "tid": tid,
                          "version": '',
                          "size": length,
                          })
                if filter is None or filter(d):
                    res.append(d)
                    if size is not None and len(res) >= size:
                        break
            return res
        finally:
            self._lock_release()


    def undo(self, transaction_id, transaction):
        """Undo a transaction identified by transaction_id.

        transaction_id is the base 64 encoding of an 8 byte tid.
        Undo by writing new data that reverses the action taken by
        the transaction.
        """

        if self._is_read_only:
            raise POSException.ReadOnlyError()
        if transaction is not self._transaction:
            raise POSException.StorageTransactionError(self, transaction)

        undo_tid = base64.decodestring(transaction_id + '\n')
        assert len(undo_tid) == 8
        undo_tid_int = u64(undo_tid)

        self._lock_acquire()
        try:
            adapter = self._adapter
            cursor = self._store_cursor
            assert cursor is not None

            adapter.locker.hold_pack_lock(cursor)
            try:
                # Note that _prepare_tid acquires the commit lock.
                # The commit lock must be acquired after the pack lock
                # because the database adapters also acquire in that
                # order during packing.
                self._prepare_tid()
                adapter.packundo.verify_undoable(cursor, undo_tid_int)

                self_tid_int = u64(self._tid)
                copied = adapter.packundo.undo(
                    cursor, undo_tid_int, self_tid_int)
                oids = [p64(oid_int) for oid_int, _ in copied]

                # Update the current object pointers immediately, so that
                # subsequent undo operations within this transaction will see
                # the new current objects.
                adapter.mover.update_current(cursor, self_tid_int)

                if self.fshelper is not None:
                    self._copy_undone_blobs(copied)

                return self._tid, oids
            finally:
                adapter.locker.release_pack_lock(cursor)
        finally:
            self._lock_release()

    def _copy_undone_blobs(self, copied):
        """After an undo operation, copy the matching blobs forward.

        The copied parameter is a list of (integer oid, integer tid).
        """
        for oid_int, old_tid_int in copied:
            oid = p64(oid_int)
            old_tid = p64(old_tid_int)
            orig_fn = self.fshelper.getBlobFilename(oid, old_tid)
            if not os.path.exists(orig_fn):
                # not a blob
                continue

            new_fn = self.fshelper.getBlobFilename(oid, self._tid)
            orig = open(orig_fn, 'r')
            new = open(new_fn, 'wb')
            ZODB.utils.cp(orig, new)
            orig.close()
            new.close()

            self._add_blob_to_transaction(oid, new_fn)

    def pack(self, t, referencesf, sleep=None):
        if self._is_read_only:
            raise POSException.ReadOnlyError()

        pack_point = repr(TimeStamp(*time.gmtime(t)[:5]+(t%60,)))
        pack_point_int = u64(pack_point)

        def get_references(state):
            """Return the set of OIDs the given state refers to."""
            refs = set()
            if state:
                for oid in referencesf(str(state)):
                    refs.add(u64(oid))
            return refs

        # Use a private connection (lock_conn and lock_cursor) to
        # hold the pack lock.  Have the adapter open temporary
        # connections to do the actual work, allowing the adapter
        # to use special transaction modes for packing.
        adapter = self._adapter
        lock_conn, lock_cursor = adapter.connmanager.open()
        try:
            adapter.locker.hold_pack_lock(lock_cursor)
            try:
                # Find the latest commit before or at the pack time.
                tid_int = adapter.packundo.choose_pack_transaction(
                    pack_point_int)
                if tid_int is None:
                    log.debug("all transactions before %s have already "
                        "been packed", time.ctime(t))
                    return

                if self._options.pack_dry_run:
                    log.info("pack: beginning dry run")

                s = time.ctime(TimeStamp(p64(tid_int)).timeTime())
                log.info("pack: analyzing transactions committed "
                    "%s or before", s)

                # In pre_pack, the adapter fills tables with
                # information about what to pack.  The adapter
                # must not actually pack anything yet.
                adapter.packundo.pre_pack(
                    tid_int, get_references, self._options)

                if self._options.pack_dry_run:
                    log.info("pack: dry run complete")
                else:
                    # Now pack.
                    if self.fshelper is not None:
                        packed_func = self._after_pack
                    else:
                        packed_func = None
                    adapter.packundo.pack(tid_int, self._options, sleep=sleep,
                        packed_func=packed_func)
            finally:
                adapter.locker.release_pack_lock(lock_cursor)
        finally:
            lock_conn.rollback()
            adapter.connmanager.close(lock_conn, lock_cursor)
        self.sync()

        self._pack_finished()

    def _after_pack(self, oid_int, tid_int):
        """Called after an object state has been removed by packing.

        Removes the corresponding blob file.
        """
        oid = p64(oid_int)
        tid = p64(tid_int)
        fn = self.fshelper.getBlobFilename(oid, tid)
        if self._adapter.keep_history:
            # remove only the revision just packed
            if os.path.exists(fn):
                ZODB.blob.remove_committed(fn)
                dirname = os.path.dirname(fn)
                if not os.listdir(dirname):
                    ZODB.blob.remove_committed_dir(dirname)
        else:
            # remove all revisions
            dirname = os.path.dirname(fn)
            if os.path.exists(dirname):
                for name in os.listdir(dirname):
                    ZODB.blob.remove_committed(os.path.join(dirname, name))
                ZODB.blob.remove_committed_dir(dirname)

    def _pack_finished(self):
        if self.fshelper is None or self._adapter.keep_history:
            return

        # Remove all old revisions of blobs.

    def iterator(self, start=None, stop=None):
        return TransactionIterator(self._adapter, start, stop)

    def sync(self, force=True):
        """Updates to a current view of the database.

        This is implemented by rolling back the relational database
        transaction.

        If force is False and a poll interval has been set, this call
        is ignored. The poll_invalidations method will later choose to
        sync with the database only if enough time has elapsed since
        the last poll.
        """
        if not force and self._options.poll_interval:
            # keep the load transaction open so that it's possible
            # to ignore the next poll.
            return
        self._lock_acquire()
        try:
            if self._load_transaction_open:
                self._rollback_load_connection()
        finally:
            self._lock_release()

    def need_poll(self):
        """Return true if polling is needed"""
        now = time.time()

        if self._cache.need_poll():
            # There is new data ready to poll
            self._poll_at = now
            return True

        if not self._load_transaction_open:
            # Since the load connection is closed or does not have
            # a transaction in progress, polling is required.
            return True

        if now >= self._poll_at:
            # The poll timeout has expired
            return True

        return False

    def _restart_load_and_poll(self):
        """Call _restart_load, poll for changes, and update self._cache.
        """
        # Ignore changes made by the last transaction committed
        # by this connection.
        if self._ltid is not None:
            ignore_tid = u64(self._ltid)
        else:
            ignore_tid = None
        prev = self._prev_polled_tid

        # get a list of changed OIDs and the most recent tid
        changes, new_polled_tid = self._restart_load_and_call(
            self._adapter.poller.poll_invalidations, prev, ignore_tid)

        # Inform the cache of the changes.
        self._cache.after_poll(
            self._load_cursor, prev, new_polled_tid, changes)

        return changes, new_polled_tid

    def poll_invalidations(self):
        """Looks for OIDs of objects that changed since _prev_polled_tid

        Returns {oid: 1}, or None if all objects need to be invalidated
        because prev_polled_tid is not in the database (presumably it
        has been packed).
        """
        self._lock_acquire()
        try:
            if self._closed:
                return {}

            if self._options.poll_interval:
                if not self.need_poll():
                    return {}
                # reset the timeout
                self._poll_at = time.time() + self._options.poll_interval

            changes, new_polled_tid = self._restart_load_and_poll()

            self._prev_polled_tid = new_polled_tid

            if changes is None:
                oids = None
            else:
                oids = {}
                for oid_int, tid_int in changes:
                    oids[p64(oid_int)] = 1
            return oids
        finally:
            self._lock_release()

    def loadBlob(self, oid, serial):
        """Return the filename of the Blob data for this OID and serial.

        Returns a filename.

        Raises POSKeyError if the blobfile cannot be found.
        """
        if self.fshelper is None:
            raise POSException.Unsupported("No blob directory is configured.")

        blob_filename = self.fshelper.getBlobFilename(oid, serial)
        if os.path.exists(blob_filename):
            return blob_filename
        else:
            raise POSKeyError("No blob file", oid, serial)

    def openCommittedBlobFile(self, oid, serial, blob=None):
        """Return a file for committed data for the given object id and serial

        If a blob is provided, then a BlobFile object is returned,
        otherwise, an ordinary file is returned.  In either case, the
        file is opened for binary reading.

        This method is used to allow storages that cache blob data to
        make sure that data are available at least long enough for the
        file to be opened.
        """
        blob_filename = self.loadBlob(oid, serial)
        if blob is None:
            return open(blob_filename, 'rb')
        else:
            return ZODB.blob.BlobFile(blob_filename, 'r', blob)

    def temporaryDirectory(self):
        """Return a directory that should be used for uncommitted blob data.

        If Blobs use this, then commits can be performed with a simple rename.
        """
        return self.fshelper.temp_dir

    def storeBlob(self, oid, oldserial, data, blobfilename, version, txn):
        """Stores data that has a BLOB attached.

        The blobfilename argument names a file containing blob data.
        The storage will take ownership of the file and will rename it
        (or copy and remove it) immediately, or at transaction-commit
        time.  The file must not be open.

        The new serial is returned.
        """
        assert not version
        self.store(oid, oldserial, data, '', txn)
        self._store_blob_data(oid, oldserial, blobfilename)
        return None

    def restoreBlob(self, oid, serial, data, blobfilename, prev_txn, txn):
        """Write blob data already committed in a separate database

        See the restore and storeBlob methods.
        """
        self.restore(oid, serial, data, '', prev_txn, txn)
        self._lock_acquire()
        try:
            self.fshelper.getPathForOID(oid, create=True)
            targetname = self.fshelper.getBlobFilename(oid, serial)
            ZODB.blob.rename_or_copy_blob(blobfilename, targetname)
        finally:
            self._lock_release()

    def _store_blob_data(self, oid, oldserial, filename):
        self.fshelper.getPathForOID(oid, create=True)
        fd, target = self.fshelper.blob_mkstemp(oid, oldserial)
        os.close(fd)
        if sys.platform == 'win32':
            # On windows, we can't rename to an existing file.  We'll
            # use a slightly different file name. We keep the old one
            # until we're done to avoid conflicts. Then remove the old name.
            target += 'w'
            ZODB.blob.rename_or_copy_blob(filename, target)
            os.remove(target[:-1])
        else:
            ZODB.blob.rename_or_copy_blob(filename, target)

        self._add_blob_to_transaction(oid, target)

    def _add_blob_to_transaction(self, oid, filename):
        if self._txn_blobs is None:
            self._txn_blobs = {}
        else:
            old_filename = self._txn_blobs.get(oid)
            if old_filename is not None and old_filename != filename:
                ZODB.blob.remove_committed(old_filename)
        self._txn_blobs[oid] = filename

    def copyTransactionsFrom(self, other):
        # adapted from ZODB.blob.BlobStorageMixin
        for trans in other.iterator():
            self.tpc_begin(trans, trans.tid, trans.status)
            for record in trans:
                blobfilename = None
                if self.fshelper is not None:
                    if is_blob_record(record.data):
                        try:
                            blobfilename = other.loadBlob(
                                record.oid, record.tid)
                        except POSKeyError:
                            pass
                if blobfilename is not None:
                    fd, name = tempfile.mkstemp(
                        suffix='.tmp', dir=self.fshelper.temp_dir)
                    os.close(fd)
                    ZODB.utils.cp(open(blobfilename, 'rb'), open(name, 'wb'))
                    self.restoreBlob(record.oid, record.tid, record.data,
                                     name, record.data_txn, trans)
                else:
                    self.restore(record.oid, record.tid, record.data,
                                 '', record.data_txn, trans)

            self.tpc_vote(trans)
            self.tpc_finish(trans)

    # The propagate_invalidations flag implements the old
    # invalidation polling API and is not otherwise used. Set to a
    # false value, it tells the Connection not to propagate object
    # invalidations across connections, since that ZODB feature is
    # detrimental when the storage provides its own MVCC.
    propagate_invalidations = False

    def bind_connection(self, zodb_conn):
        """Make a new storage instance.

        This implements the old invalidation polling API and is not
        otherwise used.
        """
        return self.new_instance()

    def connection_closing(self):
        """Release resources

        This implements the old invalidation polling API and is not
        otherwise used.
        """
        self.sync(False)


class TransactionIterator(object):
    """Iterate over the transactions in a RelStorage instance."""

    def __init__(self, adapter, start, stop):
        self._adapter = adapter
        self._conn, self._cursor = self._adapter.connmanager.open_for_load()
        self._closed = False

        if start is not None:
            start_int = u64(start)
        else:
            start_int = 1
        if stop is not None:
            stop_int = u64(stop)
        else:
            stop_int = None

        # _transactions: [(tid, username, description, extension, packed)]
        self._transactions = list(adapter.dbiter.iter_transactions_range(
            self._cursor, start_int, stop_int))
        self._index = 0

    def close(self):
        self._adapter.connmanager.close(self._conn, self._cursor)
        self._closed = True

    def iterator(self):
        return self

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, n):
        self._index = n
        return self.next()

    def next(self):
        if self._closed:
            raise IOError("TransactionIterator already closed")
        if self._index >= len(self._transactions):
            raise StorageStopIteration()
        params = self._transactions[self._index]
        res = RelStorageTransactionRecord(self, *params)
        self._index += 1
        return res


class RelStorageTransactionRecord(TransactionRecord):

    def __init__(self, trans_iter, tid_int, user, desc, ext, packed):
        self._trans_iter = trans_iter
        self._tid_int = tid_int
        self.tid = p64(tid_int)
        self.status = packed and 'p' or ' '
        self.user = user or ''
        self.description = desc or ''
        if ext:
            self.extension = cPickle.loads(ext)
        else:
            self.extension = {}

    # maintain compatibility with the old (ZODB 3.8 and below) name of
    # the extension attribute.
    def _ext_set(self, value):
        self.extension = value
    def _ext_get(self):
        return self.extension
    _extension = property(fset=_ext_set, fget=_ext_get)

    def __iter__(self):
        return RecordIterator(self)


class RecordIterator(object):
    """Iterate over the objects in a transaction."""
    def __init__(self, record):
        # record is a RelStorageTransactionRecord.
        cursor = record._trans_iter._cursor
        adapter = record._trans_iter._adapter
        tid_int = record._tid_int
        self.tid = record.tid
        self._records = list(adapter.dbiter.iter_objects(cursor, tid_int))
        self._index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._records)

    def __getitem__(self, n):
        self._index = n
        return self.next()

    def next(self):
        if self._index >= len(self._records):
            raise StorageStopIteration()
        params = self._records[self._index]
        res = Record(self.tid, *params)
        self._index += 1
        return res


class Record(DataRecord):
    """An object state in a transaction"""
    version = ''
    data_txn = None

    def __init__(self, tid, oid_int, data):
        self.tid = tid
        self.oid = p64(oid_int)
        if data is not None:
            self.data = str(data)
        else:
            self.data = None
