##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""History preserving IObjectMover implementation.
"""

from base64 import decodestring
from base64 import encodestring
from relstorage.adapters.interfaces import IObjectMover
from relstorage.adapters.batch import MySQLRowBatcher
from relstorage.adapters.batch import OracleRowBatcher
from relstorage.adapters.batch import PostgreSQLRowBatcher
from zope.interface import implements
import os

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5


def compute_md5sum(data):
    if data is not None:
        return md5(data).hexdigest()
    else:
        # George Bailey object
        return None


class ObjectMover(object):
    implements(IObjectMover)

    _method_names = (
        'load_current',
        'load_revision',
        'exists',
        'load_before',
        'get_object_tid_after',
        'current_object_tids',
        'on_store_opened',
        'make_batcher',
        'store_temp',
        'restore',
        'detect_conflict',
        'replace_temp',
        'move_from_temp',
        'update_current',
        'download_blob',
        'upload_blob',
        )

    def __init__(self, database_name, options, runner=None,
            Binary=None, inputsizes=None, version_detector=None):
        # The inputsizes parameter is for Oracle only.
        self.database_name = database_name
        self.keep_history = options.keep_history
        self.blob_chunk_size = options.blob_chunk_size
        self.runner = runner
        self.Binary = Binary
        self.inputsizes = inputsizes
        self.version_detector = version_detector

        for method_name in self._method_names:
            method = getattr(self, '%s_%s' % (database_name, method_name))
            setattr(self, method_name, method)




    def postgresql_load_current(self, cursor, oid):
        """Returns the current pickle and integer tid for an object.

        oid is an integer.  Returns (None, None) if object does not exist.
        """
        if self.keep_history:
            stmt = """
            SELECT encode(state, 'base64'), tid
            FROM current_object
                JOIN object_state USING(zoid, tid)
            WHERE zoid = %s
            """
        else:
            stmt = """
            SELECT encode(state, 'base64'), tid
            FROM object_state
            WHERE zoid = %s
            """
        cursor.execute(stmt, (oid,))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            state64, tid = cursor.fetchone()
            if state64 is not None:
                state = decodestring(state64)
            else:
                # This object's creation has been undone
                state = None
            return state, tid
        else:
            return None, None

    def mysql_load_current(self, cursor, oid):
        """Returns the current pickle and integer tid for an object.

        oid is an integer.  Returns (None, None) if object does not exist.
        """
        if self.keep_history:
            stmt = """
            SELECT state, tid
            FROM current_object
                JOIN object_state USING(zoid, tid)
            WHERE zoid = %s
            """
        else:
            stmt = """
            SELECT state, tid
            FROM object_state
            WHERE zoid = %s
            """
        cursor.execute(stmt, (oid,))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            return cursor.fetchone()
        else:
            return None, None

    def oracle_load_current(self, cursor, oid):
        """Returns the current pickle and integer tid for an object.

        oid is an integer.  Returns (None, None) if object does not exist.
        """
        if self.keep_history:
            stmt = """
            SELECT state, tid
            FROM current_object
                JOIN object_state USING(zoid, tid)
            WHERE zoid = :1
            """
        else:
            stmt = """
            SELECT state, tid
            FROM object_state
            WHERE zoid = :1
            """
        return self.runner.run_lob_stmt(
            cursor, stmt, (oid,), default=(None, None))




    def postgresql_load_revision(self, cursor, oid, tid):
        """Returns the pickle for an object on a particular transaction.

        Returns None if no such state exists.
        """
        stmt = """
        SELECT encode(state, 'base64')
        FROM object_state
        WHERE zoid = %s
            AND tid = %s
        """
        cursor.execute(stmt, (oid, tid))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            (state64,) = cursor.fetchone()
            if state64 is not None:
                return decodestring(state64)
        return None

    def mysql_load_revision(self, cursor, oid, tid):
        """Returns the pickle for an object on a particular transaction.

        Returns None if no such state exists.
        """
        stmt = """
        SELECT state
        FROM object_state
        WHERE zoid = %s
            AND tid = %s
        """
        cursor.execute(stmt, (oid, tid))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            (state,) = cursor.fetchone()
            return state
        return None

    def oracle_load_revision(self, cursor, oid, tid):
        """Returns the pickle for an object on a particular transaction.

        Returns None if no such state exists.
        """
        stmt = """
        SELECT state
        FROM object_state
        WHERE zoid = :1
            AND tid = :2
        """
        (state,) = self.runner.run_lob_stmt(
            cursor, stmt, (oid, tid), default=(None,))
        return state




    def generic_exists(self, cursor, oid):
        """Returns a true value if the given object exists."""
        if self.keep_history:
            stmt = "SELECT 1 FROM current_object WHERE zoid = %s"
        else:
            stmt = "SELECT 1 FROM object_state WHERE zoid = %s"
        cursor.execute(stmt, (oid,))
        return cursor.rowcount

    postgresql_exists = generic_exists
    mysql_exists = generic_exists

    def oracle_exists(self, cursor, oid):
        """Returns a true value if the given object exists."""
        if self.keep_history:
            stmt = "SELECT 1 FROM current_object WHERE zoid = :1"
        else:
            stmt = "SELECT 1 FROM object_state WHERE zoid = :1"
        cursor.execute(stmt, (oid,))
        for row in cursor:
            return True
        return False




    def postgresql_load_before(self, cursor, oid, tid):
        """Returns the pickle and tid of an object before transaction tid.

        Returns (None, None) if no earlier state exists.
        """
        stmt = """
        SELECT encode(state, 'base64'), tid
        FROM object_state
        WHERE zoid = %s
            AND tid < %s
        ORDER BY tid DESC
        LIMIT 1
        """
        cursor.execute(stmt, (oid, tid))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            state64, tid = cursor.fetchone()
            if state64 is not None:
                state = decodestring(state64)
            else:
                # The object's creation has been undone
                state = None
            return state, tid
        else:
            return None, None

    def mysql_load_before(self, cursor, oid, tid):
        """Returns the pickle and tid of an object before transaction tid.

        Returns (None, None) if no earlier state exists.
        """
        stmt = """
        SELECT state, tid
        FROM object_state
        WHERE zoid = %s
            AND tid < %s
        ORDER BY tid DESC
        LIMIT 1
        """
        cursor.execute(stmt, (oid, tid))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            return cursor.fetchone()
        else:
            return None, None

    def oracle_load_before(self, cursor, oid, tid):
        """Returns the pickle and tid of an object before transaction tid.

        Returns (None, None) if no earlier state exists.
        """
        stmt = """
        SELECT state, tid
        FROM object_state
        WHERE zoid = :oid
            AND tid = (
                SELECT MAX(tid)
                FROM object_state
                WHERE zoid = :oid
                    AND tid < :tid
            )
        """
        return self.runner.run_lob_stmt(
            cursor, stmt, {'oid': oid, 'tid': tid}, default=(None, None))




    def generic_get_object_tid_after(self, cursor, oid, tid):
        """Returns the tid of the next change after an object revision.

        Returns None if no later state exists.
        """
        stmt = """
        SELECT tid
        FROM object_state
        WHERE zoid = %s
            AND tid > %s
        ORDER BY tid
        LIMIT 1
        """
        cursor.execute(stmt, (oid, tid))
        if cursor.rowcount:
            assert cursor.rowcount == 1
            return cursor.fetchone()[0]
        else:
            return None

    postgresql_get_object_tid_after = generic_get_object_tid_after
    mysql_get_object_tid_after = generic_get_object_tid_after

    def oracle_get_object_tid_after(self, cursor, oid, tid):
        """Returns the tid of the next change after an object revision.

        Returns None if no later state exists.
        """
        stmt = """
        SELECT MIN(tid)
        FROM object_state
        WHERE zoid = :1
            AND tid > :2
        """
        cursor.execute(stmt, (oid, tid))
        rows = cursor.fetchall()
        if rows:
            assert len(rows) == 1
            return rows[0][0]
        else:
            return None




    def generic_current_object_tids(self, cursor, oids):
        """Returns the current {oid: tid} for specified object ids."""
        res = {}
        if self.keep_history:
            table = 'current_object'
        else:
            table = 'object_state'
        oids = list(oids)
        while oids:
            oid_list = ','.join(str(oid) for oid in oids[:1000])
            del oids[:1000]
            stmt = "SELECT zoid, tid FROM %s WHERE zoid IN (%s)" % (
                table, oid_list)
            cursor.execute(stmt)
            for oid, tid in cursor:
                res[oid] = tid
        return res

    postgresql_current_object_tids = generic_current_object_tids
    mysql_current_object_tids = generic_current_object_tids
    oracle_current_object_tids = generic_current_object_tids




    def postgresql_on_store_opened(self, cursor, restart=False):
        """Create the temporary tables for storing objects"""
        # note that the md5 column is not used if self.keep_history == False.
        stmt = """
        CREATE TEMPORARY TABLE temp_store (
            zoid        BIGINT NOT NULL,
            prev_tid    BIGINT NOT NULL,
            md5         CHAR(32),
            state       BYTEA
        ) ON COMMIT DROP;
        CREATE UNIQUE INDEX temp_store_zoid ON temp_store (zoid);

        CREATE TEMPORARY TABLE temp_blob_chunk (
            zoid        BIGINT NOT NULL,
            chunk_num   BIGINT NOT NULL,
            chunk       BYTEA
        ) ON COMMIT DROP;
        CREATE UNIQUE INDEX temp_blob_chunk_key
            ON temp_blob_chunk (zoid, chunk_num);
        """
        cursor.execute(stmt)

    def mysql_on_store_opened(self, cursor, restart=False):
        """Create the temporary table for storing objects"""
        if restart:
            stmt = "DROP TEMPORARY TABLE IF EXISTS temp_store"
            cursor.execute(stmt)
            stmt = "DROP TEMPORARY TABLE IF EXISTS temp_blob_chunk"
            cursor.execute(stmt)

        # note that the md5 column is not used if self.keep_history == False.
        stmt = """
        CREATE TEMPORARY TABLE temp_store (
            zoid        BIGINT NOT NULL PRIMARY KEY,
            prev_tid    BIGINT NOT NULL,
            md5         CHAR(32),
            state       LONGBLOB
        ) ENGINE MyISAM
        """
        cursor.execute(stmt)

        stmt = """
        CREATE TEMPORARY TABLE temp_blob_chunk (
            zoid        BIGINT NOT NULL,
            chunk_num   BIGINT NOT NULL,
                        PRIMARY KEY (zoid, chunk_num),
            chunk       LONGBLOB
        ) ENGINE MyISAM
        """
        cursor.execute(stmt)

    # no store connection initialization needed for Oracle
    oracle_on_store_opened = None




    def postgresql_make_batcher(self, cursor, row_limit):
        return PostgreSQLRowBatcher(cursor, self.version_detector, row_limit)

    def mysql_make_batcher(self, cursor, row_limit):
        return MySQLRowBatcher(cursor, row_limit)

    def oracle_make_batcher(self, cursor, row_limit):
        return OracleRowBatcher(cursor, self.inputsizes, row_limit)




    def postgresql_store_temp(self, cursor, batcher, oid, prev_tid, data):
        """Store an object in the temporary table."""
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None
        batcher.delete_from('temp_store', zoid=oid)
        batcher.insert_into(
            "temp_store (zoid, prev_tid, md5, state)",
            "%s, %s, %s, decode(%s, 'base64')",
            (oid, prev_tid, md5sum, encodestring(data)),
            rowkey=oid,
            size=len(data),
            )

    def mysql_store_temp(self, cursor, batcher, oid, prev_tid, data):
        """Store an object in the temporary table."""
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None
        batcher.insert_into(
            "temp_store (zoid, prev_tid, md5, state)",
            "%s, %s, %s, %s",
            (oid, prev_tid, md5sum, self.Binary(data)),
            rowkey=oid,
            size=len(data),
            command='REPLACE',
            )

    def oracle_store_temp(self, cursor, batcher, oid, prev_tid, data):
        """Store an object in the temporary table."""
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None

        if len(data) <= 2000:
            # Send data inline for speed.  Oracle docs say maximum size
            # of a RAW is 2000 bytes.
            stmt = "BEGIN relstorage_op.store_temp(:1, :2, :3, :4); END;"
            batcher.add_array_op(
                stmt,
                'oid prev_tid md5sum rawdata',
                (oid, prev_tid, md5sum, data),
                rowkey=oid,
                size=len(data),
                )
        else:
            # Send data as a BLOB
            row = {
                'oid': oid,
                'prev_tid': prev_tid,
                'md5sum': md5sum,
                'blobdata': data,
                }
            batcher.insert_into(
                "temp_store (zoid, prev_tid, md5, state)",
                ":oid, :prev_tid, :md5sum, :blobdata",
                row,
                rowkey=oid,
                size=len(data),
                )




    def postgresql_restore(self, cursor, batcher, oid, tid, data):
        """Store an object directly, without conflict detection.

        Used for copying transactions into this database.
        """
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None

        if data is not None:
            encoded = encodestring(data)
        else:
            encoded = None

        if self.keep_history:
            batcher.delete_from("object_state", zoid=oid, tid=tid)
            row_schema = """
                %s, %s,
                COALESCE((SELECT tid FROM current_object WHERE zoid = %s), 0),
                %s, decode(%s, 'base64')
            """
            batcher.insert_into(
                "object_state (zoid, tid, prev_tid, md5, state)",
                row_schema,
                (oid, tid, oid, md5sum, encoded),
                rowkey=(oid, tid),
                size=len(data or ''),
                )
        else:
            batcher.delete_from('object_state', zoid=oid)
            if data:
                batcher.insert_into(
                    "object_state (zoid, tid, state)",
                    "%s, %s, decode(%s, 'base64')",
                    (oid, tid, encoded),
                    rowkey=oid,
                    size=len(data),
                    )

    def mysql_restore(self, cursor, batcher, oid, tid, data):
        """Store an object directly, without conflict detection.

        Used for copying transactions into this database.
        """
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None

        if data is not None:
            encoded = self.Binary(data)
        else:
            encoded = None

        if self.keep_history:
            row_schema = """
                %s, %s,
                COALESCE((SELECT tid FROM current_object WHERE zoid = %s), 0),
                %s, %s
            """
            batcher.insert_into(
                "object_state (zoid, tid, prev_tid, md5, state)",
                row_schema,
                (oid, tid, oid, md5sum, encoded),
                rowkey=(oid, tid),
                size=len(data or ''),
                command='REPLACE',
                )
        else:
            if data:
                batcher.insert_into(
                    "object_state (zoid, tid, state)",
                    "%s, %s, %s",
                    (oid, tid, encoded),
                    rowkey=oid,
                    size=len(data),
                    command='REPLACE',
                    )
            else:
                batcher.delete_from('object_state', zoid=oid)

    def oracle_restore(self, cursor, batcher, oid, tid, data):
        """Store an object directly, without conflict detection.

        Used for copying transactions into this database.
        """
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None

        if not data or len(data) <= 2000:
            # Send data inline for speed.  Oracle docs say maximum size
            # of a RAW is 2000 bytes.
            if self.keep_history:
                stmt = "BEGIN relstorage_op.restore(:1, :2, :3, :4); END;"
                batcher.add_array_op(
                    stmt,
                    'oid tid md5sum rawdata',
                    (oid, tid, md5sum, data),
                    rowkey=(oid, tid),
                    size=len(data or ''),
                    )
            else:
                stmt = "BEGIN relstorage_op.restore(:1, :2, :3); END;"
                batcher.add_array_op(
                    stmt,
                    'oid tid rawdata',
                    (oid, tid, data),
                    rowkey=(oid, tid),
                    size=len(data or ''),
                    )

        else:
            # Send as a BLOB
            if self.keep_history:
                row = {
                    'oid': oid,
                    'tid': tid,
                    'md5sum': md5sum,
                    'blobdata': data,
                    }
                row_schema = """
                    :oid, :tid,
                    COALESCE((SELECT tid
                              FROM current_object
                              WHERE zoid = :oid), 0),
                    :md5sum, :blobdata
                """
                batcher.insert_into(
                    "object_state (zoid, tid, prev_tid, md5, state)",
                    row_schema,
                    row,
                    rowkey=(oid, tid),
                    size=len(data or ''),
                    )
            else:
                batcher.delete_from('object_state', zoid=oid)
                if data:
                    batcher.insert_into(
                        "object_state (zoid, tid, state)",
                        ":oid, :tid, :blobdata",
                        {'oid': oid, 'tid': tid, 'blobdata': data},
                        rowkey=oid,
                        size=len(data),
                        )




    def postgresql_detect_conflict(self, cursor):
        """Find one conflict in the data about to be committed.

        If there is a conflict, returns (oid, prev_tid, attempted_prev_tid,
        attempted_data).  If there is no conflict, returns None.
        """
        if self.keep_history:
            stmt = """
            SELECT temp_store.zoid, current_object.tid, temp_store.prev_tid,
                encode(temp_store.state, 'base64')
            FROM temp_store
                JOIN current_object ON (temp_store.zoid = current_object.zoid)
            WHERE temp_store.prev_tid != current_object.tid
            LIMIT 1
            """
        else:
            stmt = """
            SELECT temp_store.zoid, object_state.tid, temp_store.prev_tid,
                encode(temp_store.state, 'base64')
            FROM temp_store
                JOIN object_state ON (temp_store.zoid = object_state.zoid)
            WHERE temp_store.prev_tid != object_state.tid
            LIMIT 1
            """
        cursor.execute(stmt)
        if cursor.rowcount:
            oid, prev_tid, attempted_prev_tid, data = cursor.fetchone()
            return oid, prev_tid, attempted_prev_tid, decodestring(data)
        return None

    def mysql_detect_conflict(self, cursor):
        """Find one conflict in the data about to be committed.

        If there is a conflict, returns (oid, prev_tid, attempted_prev_tid,
        attempted_data).  If there is no conflict, returns None.
        """
        # Lock in share mode to ensure the data being read is up to date.
        if self.keep_history:
            stmt = """
            SELECT temp_store.zoid, current_object.tid, temp_store.prev_tid,
                temp_store.state
            FROM temp_store
                JOIN current_object ON (temp_store.zoid = current_object.zoid)
            WHERE temp_store.prev_tid != current_object.tid
            LIMIT 1
            LOCK IN SHARE MODE
            """
        else:
            stmt = """
            SELECT temp_store.zoid, object_state.tid, temp_store.prev_tid,
                temp_store.state
            FROM temp_store
                JOIN object_state ON (temp_store.zoid = object_state.zoid)
            WHERE temp_store.prev_tid != object_state.tid
            LIMIT 1
            LOCK IN SHARE MODE
            """
        cursor.execute(stmt)
        if cursor.rowcount:
            return cursor.fetchone()
        return None

    def oracle_detect_conflict(self, cursor):
        """Find one conflict in the data about to be committed.

        If there is a conflict, returns (oid, prev_tid, attempted_prev_tid,
        attempted_data).  If there is no conflict, returns None.
        """
        if self.keep_history:
            stmt = """
            SELECT temp_store.zoid, current_object.tid, temp_store.prev_tid,
                temp_store.state
            FROM temp_store
                JOIN current_object ON (temp_store.zoid = current_object.zoid)
            WHERE temp_store.prev_tid != current_object.tid
            """
        else:
            stmt = """
            SELECT temp_store.zoid, object_state.tid, temp_store.prev_tid,
                temp_store.state
            FROM temp_store
                JOIN object_state ON (temp_store.zoid = object_state.zoid)
            WHERE temp_store.prev_tid != object_state.tid
            """
        return self.runner.run_lob_stmt(cursor, stmt)




    def postgresql_replace_temp(self, cursor, oid, prev_tid, data):
        """Replace an object in the temporary table.

        This happens after conflict resolution.
        """
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None
        stmt = """
        UPDATE temp_store SET
            prev_tid = %s,
            md5 = %s,
            state = decode(%s, 'base64')
        WHERE zoid = %s
        """
        cursor.execute(stmt, (prev_tid, md5sum, encodestring(data), oid))

    def mysql_replace_temp(self, cursor, oid, prev_tid, data):
        """Replace an object in the temporary table.

        This happens after conflict resolution.
        """
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None
        stmt = """
        UPDATE temp_store SET
            prev_tid = %s,
            md5 = %s,
            state = %s
        WHERE zoid = %s
        """
        cursor.execute(stmt, (prev_tid, md5sum, self.Binary(data), oid))

    def oracle_replace_temp(self, cursor, oid, prev_tid, data):
        """Replace an object in the temporary table.

        This happens after conflict resolution.
        """
        if self.keep_history:
            md5sum = compute_md5sum(data)
        else:
            md5sum = None
        stmt = """
        UPDATE temp_store SET
            prev_tid = :prev_tid,
            md5 = :md5sum,
            state = :blobdata
        WHERE zoid = :oid
        """
        cursor.setinputsizes(blobdata=self.inputsizes['blobdata'])
        cursor.execute(stmt, oid=oid, prev_tid=prev_tid,
            md5sum=md5sum, blobdata=self.Binary(data))




    def generic_move_from_temp(self, cursor, tid, txn_has_blobs):
        """Moved the temporarily stored objects to permanent storage.

        Returns the list of oids stored.
        """
        if self.keep_history:
            if self.database_name == 'oracle':
                stmt = """
                INSERT INTO object_state (zoid, tid, prev_tid, md5, state)
                SELECT zoid, :1, prev_tid, md5, state
                FROM temp_store
                """
            else:
                stmt = """
                INSERT INTO object_state (zoid, tid, prev_tid, md5, state)
                SELECT zoid, %s, prev_tid, md5, state
                FROM temp_store
                """
            cursor.execute(stmt, (tid,))

        else:
            if self.database_name == 'mysql':
                stmt = """
                REPLACE INTO object_state (zoid, tid, state)
                SELECT zoid, %s, state
                FROM temp_store
                """
                cursor.execute(stmt, (tid,))

            else:
                stmt = """
                DELETE FROM object_state
                WHERE zoid IN (SELECT zoid FROM temp_store)
                """
                cursor.execute(stmt)

                if self.database_name == 'oracle':
                    stmt = """
                    INSERT INTO object_state (zoid, tid, state)
                    SELECT zoid, :1, state
                    FROM temp_store
                    """
                else:
                    stmt = """
                    INSERT INTO object_state (zoid, tid, state)
                    SELECT zoid, %s, state
                    FROM temp_store
                    """
                cursor.execute(stmt, (tid,))

            if txn_has_blobs:
                stmt = """
                DELETE FROM blob_chunk
                WHERE zoid IN (SELECT zoid FROM temp_store)
                """
                cursor.execute(stmt)

        if txn_has_blobs:
            if self.database_name == 'oracle':
                stmt = """
                INSERT INTO blob_chunk (zoid, tid, chunk_num, chunk)
                SELECT zoid, :1, chunk_num, chunk
                FROM temp_blob_chunk
                """
            else:
                stmt = """
                INSERT INTO blob_chunk (zoid, tid, chunk_num, chunk)
                SELECT zoid, %s, chunk_num, chunk
                FROM temp_blob_chunk
                """
            cursor.execute(stmt, (tid,))

        stmt = """
        SELECT zoid FROM temp_store
        """
        cursor.execute(stmt)
        return [oid for (oid,) in cursor]

    postgresql_move_from_temp = generic_move_from_temp
    mysql_move_from_temp = generic_move_from_temp
    oracle_move_from_temp = generic_move_from_temp




    def postgresql_update_current(self, cursor, tid):
        """Update the current object pointers.

        tid is the integer tid of the transaction being committed.
        """
        if not self.keep_history:
            # nothing needs to be updated
            return

        cursor.execute("""
        -- Insert objects created in this transaction into current_object.
        INSERT INTO current_object (zoid, tid)
        SELECT zoid, tid FROM object_state
        WHERE tid = %(tid)s
            AND prev_tid = 0;

        -- Change existing objects.  To avoid deadlocks,
        -- update in OID order.
        UPDATE current_object SET tid = %(tid)s
        WHERE zoid IN (
            SELECT zoid FROM object_state
            WHERE tid = %(tid)s
                AND prev_tid != 0
            ORDER BY zoid
        )
        """, {'tid': tid})

    def mysql_update_current(self, cursor, tid):
        """Update the current object pointers.

        tid is the integer tid of the transaction being committed.
        """
        if not self.keep_history:
            # nothing needs to be updated
            return

        cursor.execute("""
        REPLACE INTO current_object (zoid, tid)
        SELECT zoid, tid FROM object_state
        WHERE tid = %s
        """, (tid,))

    def oracle_update_current(self, cursor, tid):
        """Update the current object pointers.

        tid is the integer tid of the transaction being committed.
        """
        if not self.keep_history:
            # nothing needs to be updated
            return

        # Insert objects created in this transaction into current_object.
        stmt = """
        INSERT INTO current_object (zoid, tid)
        SELECT zoid, tid FROM object_state
        WHERE tid = :1
            AND prev_tid = 0
        """
        cursor.execute(stmt, (tid,))

        # Change existing objects.
        stmt = """
        UPDATE current_object SET tid = :1
        WHERE zoid IN (
            SELECT zoid FROM object_state
            WHERE tid = :1
                AND prev_tid != 0
        )
        """
        cursor.execute(stmt, (tid,))




    def generic_download_blob(self, cursor, oid, tid, filename):
        """Download a blob into a file."""
        stmt = """
        SELECT chunk
        FROM blob_chunk
        WHERE zoid = %s
            AND tid = %s
            AND chunk_num = %s
        """

        use_base64 = False
        if self.database_name == 'postgresql':
            use_base64 = True
            stmt = stmt.replace(
                "SELECT chunk", "SELECT encode(chunk, 'base64')")
        elif self.database_name == 'oracle':
            for n in (1, 2, 3):
                stmt = stmt.replace('%s', ':%d' % n, 1)

        f = None
        bytes = 0
        try:
            chunk_num = 0
            while True:
                if self.database_name == 'oracle':
                    row = self.runner.run_lob_stmt(
                        cursor, stmt, (oid, tid, chunk_num))
                    if row is not None:
                        chunk = row[0] or ''
                    else:
                        chunk = None
                else:
                    cursor.execute(stmt, (oid, tid, chunk_num))
                    rows = list(cursor)
                    if rows:
                        assert len(rows) == 1
                        chunk = rows[0][0]
                    else:
                        chunk = None

                if chunk is None:
                    # No more chunks.  Note: if there are no chunks at
                    # all, then this method should not write a file.
                    break

                if use_base64:
                    chunk = decodestring(chunk)
                if f is None:
                    f = open(filename, 'wb')
                f.write(chunk)
                bytes += len(chunk)
                chunk_num += 1
        except:
            if f is not None:
                f.close()
                os.remove(filename)
            raise

        if f is not None:
            f.close()
        return bytes

    mysql_download_blob = generic_download_blob
    postgresql_download_blob = generic_download_blob
    oracle_download_blob = generic_download_blob




    def generic_upload_blob(self, cursor, oid, tid, filename):
        """Upload a blob from a file.

        If serial is None, upload to the temporary table.
        """
        if tid is not None:
            if self.keep_history:
                delete_stmt = """
                DELETE FROM blob_chunk
                WHERE zoid = %s AND tid = %s
                """
                cursor.execute(delete_stmt, (oid, tid))
            else:
                delete_stmt = "DELETE FROM blob_chunk WHERE zoid = %s"
                cursor.execute(delete_stmt, (oid,))

            use_tid = True
            insert_stmt = """
            INSERT INTO blob_chunk (zoid, tid, chunk_num, chunk)
            VALUES (%s, %s, %s, CHUNK)
            """
        else:
            use_tid = False
            delete_stmt = "DELETE FROM temp_blob_chunk WHERE zoid = %s"
            cursor.execute(delete_stmt, (oid,))

            insert_stmt = """
            INSERT INTO temp_blob_chunk (zoid, chunk_num, chunk)
            VALUES (%s, %s, CHUNK)
            """

        use_base64 = False
        if self.database_name == 'postgresql':
            use_base64 = True
            insert_stmt = insert_stmt.replace(
                "CHUNK", "decode(%s, 'base64')", 1)
        else:
            insert_stmt = insert_stmt.replace("CHUNK", "%s")

        f = open(filename, 'rb')
        try:
            chunk_num = 0
            while True:
                chunk = f.read(self.blob_chunk_size)
                if not chunk and chunk_num > 0:
                    # EOF.  Note that we always write at least one
                    # chunk, even if the blob file is empty.
                    break
                if use_base64:
                    chunk = encodestring(chunk)
                if use_tid:
                    params = (oid, tid, chunk_num, chunk)
                else:
                    params = (oid, chunk_num, chunk)
                cursor.execute(insert_stmt, params)
                chunk_num += 1
        finally:
            f.close()

    mysql_upload_blob = generic_upload_blob
    postgresql_upload_blob = generic_upload_blob

    def oracle_upload_blob(self, cursor, oid, tid, filename):
        """Upload a blob from a file.

        If serial is None, upload to the temporary table.
        """
        if tid is not None:
            if self.keep_history:
                delete_stmt = """
                DELETE FROM blob_chunk
                WHERE zoid = :1 AND tid = :2
                """
                cursor.execute(delete_stmt, (oid, tid))
            else:
                delete_stmt = "DELETE FROM blob_chunk WHERE zoid = :1"
                cursor.execute(delete_stmt, (oid,))

            use_tid = True
            insert_stmt = """
            INSERT INTO blob_chunk (zoid, tid, chunk_num, chunk)
            VALUES (:oid, :tid, :chunk_num, :blobdata)
            """

        else:
            use_tid = False
            delete_stmt = "DELETE FROM temp_blob_chunk WHERE zoid = :1"
            cursor.execute(delete_stmt, (oid,))

            insert_stmt = """
            INSERT INTO temp_blob_chunk (zoid, chunk_num, chunk)
            VALUES (:oid, :chunk_num, :blobdata)
            """

        f = open(filename, 'rb')
        try:
            chunk_num = 0
            while True:
                chunk = f.read(self.blob_chunk_size)
                if not chunk and chunk_num > 0:
                    # EOF.  Note that we always write at least one
                    # chunk, even if the blob file is empty.
                    break
                params = {
                    'oid': oid,
                    'chunk_num': chunk_num,
                    'blobdata': chunk,
                }
                if use_tid:
                    params['tid'] = tid
                cursor.setinputsizes(blobdata=self.inputsizes['blobdata'])
                cursor.execute(insert_stmt, params)
                chunk_num += 1
        finally:
            f.close()
