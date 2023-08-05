#
# By Krister Hedfors
#
# + pack/unpack everywhere
# + db-sorted iteritems
#
#
__all__ = ['sqldict']

__doc__ = '''

    sqldict - dict with sqlalchemy database-agnostic back-end
              capable of using picklable objects as both
              keys and values
'''

import unittest
import doctest
from UserDict import DictMixin
import pickle
import cPickle
import base64

from sqlalchemy import create_engine


class UDictException(Exception):pass
class SQLDictException(UDictException): pass
class SQLDictError(UDictException): pass


from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy.exc import (
        NoSuchTableError,
        IntegrityError
)



class BaseSQLDict(DictMixin):
    '''
    >>> e = create_engine('sqlite://')
    >>> d = BaseSQLDict(e.connect(), 'asd', create=1)
    '''

    _KEYSIZE = 1000-64
    _VALSIZE = 4000
    _NSSIZE  = 64

    _F_SERIALIZED_KEY = 1 << 0
    _F_SERIALIZED_VAL = 1 << 1
    _F_UNICODE_KEY    = 1 << 2
    _F_UNICODE_VAL    = 1 << 3

    _flags = 0

    def __init__(self,  conn, tablename,
                            ns='',
                            create=0,
                            flags=_flags,
                            sort=1, # 0=dont, 1=keys, 2=values
                            keysize=_KEYSIZE,
                            valsize=_VALSIZE,
                            nssize=_NSSIZE,
                            ):
        '''
        '''
        if hasattr(conn, 'connect'):
            self._conn = conn.connect()
        else:
            self._conn = conn
        self._tablename = tablename
        self._ns = ns
        self._create = create
        self._sort = sort
        self._keysize = keysize
        self._valsize =  valsize
        self._nssize =  nssize
        #
        self._meta = MetaData()
        self._meta.bind = conn
        try:
            self._table = Table(tablename, self._meta, autoload=True)
        except NoSuchTableError, e:
            if create:
                self._create_table()
            else:
                msg = 'initialize sqldict with `create=1` to create table'
                error = (msg, e)
                raise NoSuchTableError(error)

    def _create_table(self):
        keysize = self._KEYSIZE
        valsize = self._VALSIZE
        nssize = self._NSSIZE
        #
        table = Table(self._tablename, self._meta,
            Column('sqldict_ns',  String(nssize), nullable=False, primary_key=True),
            Column('sqldict_key', String(keysize), nullable=False, primary_key=True),
            Column('sqldict_val', String(valsize), nullable=False),
            Column('sqldict_flags', Integer, nullable=False),
        )
        self._table = table
        self._meta.create_all()

    def _serialize(self, obj):
        blob = pickle.dumps(obj)
        blob = base64.b64encode(blob)
        return blob

    def _deserialize(self, blob):
        blob = base64.b64decode(blob)
        obj = pickle.loads(blob)
        return obj

    def _update(self, key, val, flags):
        'key and or val must be serialized according to flags'
        ns = self._ns
        table = self._table
        conn = self._conn
        query = update(table)
        query = query.where(table.c.sqldict_ns == ns)
        query = query.where(table.c.sqldict_key == key)
        query = query.values(sqldict_val=val, sqldict_flags=flags)
        conn.execute(query)

    def drop(self):
        self._table.drop()

    def pack_key(self, key, flags):
        key_type = type(key)
        if key_type is str:
            pass
        elif key_type is unicode:
            flags |= self._F_UNICODE_KEY
        else:
            flags |= self._F_SERIALIZED_KEY
            key = self._serialize(key)
        return (key, flags)

    def unpack_key(self, key, flags):
        if flags & self._F_SERIALIZED_KEY:
            key = self._deserialize(key)
        elif type(key) is unicode and not (flags & self._F_UNICODE_KEY):
            key = str(key)
        return key


    def pack_val(self, val, flags):
        val_type = type(val)
        if val_type is str:
            pass
        elif val_type is unicode:
            flags |= self._F_UNICODE_VAL
        else:
            flags |= self._F_SERIALIZED_VAL
            val = self._serialize(val)
        return (val, flags)

    def unpack_val(self, val, flags):
        if flags & self._F_SERIALIZED_VAL:
            val = self._deserialize(val)
        elif type(val) is unicode and not (flags & self._F_UNICODE_VAL):
            val = str(val)
        return val

    #
    # dict methods
    # 
    def iteritems(self):
        conn = self._conn
        ns = self._ns
        table = self._table
        sort = self._sort
        #
        #print 'keys'
        query = select([table.c.sqldict_key,
                        table.c.sqldict_val,
                        table.c.sqldict_flags])
        query = query.where(table.c.sqldict_ns == ns)
        if sort == 1:
            #print 'sort 1'
            query = query.order_by(table.c.sqldict_key)
        if sort == 2:
            #print 'sort 2'
            query = query.order_by(table.c.sqldict_val)
        #print query
        result = conn.execute(query)
        for row in result:
            key = row['sqldict_key']
            val = row['sqldict_val']
            flags = row['sqldict_flags']
            key = self.unpack_key(key, flags)
            val = self.unpack_val(val, flags)
            yield (key, val)

    def namespaces(self):
        conn = self._conn
        ns = self._ns
        table = self._table
        sort = self._sort
        #
        query = select([ distinct(table.c.sqldict_ns) ])
        if sort == 1:
            query = query.order_by(table.c.sqldict_ns)
        if sort == 2:
            query = query.order_by(table.c.sqldict_ns)
        #print query
        result = conn.execute(query)
        namespaces = []
        for row in result:
            ns = row['sqldict_ns']
            namespaces.append(ns)
        return namespaces

    def _dup_kwargs(self):
        kwargs = dict(
            conn=self._conn,
            tablename=self._tablename,
            ns=self._ns,
            create=0,
            sort=self._sort,
            keysize=self._keysize,
            valsize=self._valsize,
            nssize=self._nssize,
        )
        return kwargs

    def dup(self):
        cls = self.__class__
        kwargs = self._dup_kwargs()
        duplicate = cls(**kwargs)
        return duplicate

    def using_ns(self, ns):
        cls = self.__class__
        kwargs = self._dup_kwargs()
        kwargs['ns'] = ns
        duplicate = cls(**kwargs)
        return duplicate

        
    def keys(self):
        conn = self._conn
        ns = self._ns
        table = self._table
        sort = self._sort
        #
        #print 'keys'
        query = select([table.c.sqldict_key, table.c.sqldict_flags])
        query = query.where(table.c.sqldict_ns == ns)
        if sort == 1:
            #print 'sort 1'
            query = query.order_by(table.c.sqldict_key)
        if sort == 2:
            #print 'sort 2'
            query = query.order_by(table.c.sqldict_val)
        #print query
        result = conn.execute(query)
        keys = []
        for row in result:
            key = row['sqldict_key']
            flags = row['sqldict_flags']
            key = self.unpack_key(key, flags)
            keys.append(key)
        return keys

    def __getitem__(self, key):
        #print 'getitem', key
        if not type(key) in (str, unicode):
            key = self._serialize(key)
        conn = self._conn
        ns = self._ns
        table = self._table
        #
        query = select([table])
        query = query.where(table.c.sqldict_ns == ns)
        query = query.where(table.c.sqldict_key == key)
        result = conn.execute(query)
        for row in result:
            val = row['sqldict_val']
            flags = row['sqldict_flags']
            val = self.unpack_val(val, flags)
            return val
        raise KeyError

    def __delitem__(self, key):
        #print 'delitem', key
        if not type(key) in (str, unicode):
            key = self._serialize(key)
        conn = self._conn
        ns = self._ns
        table = self._table
        #
        query = table.delete()
        query = query.where(table.c.sqldict_ns == ns)
        query = query.where(table.c.sqldict_key == key)
        result = conn.execute(query)
        if result.rowcount == 0:
            raise KeyError
        elif result.rowcount > 1:
            error = 'Multiple rows affected by delete: %d' %result.rowcount
            raise SQLDictException(error)
        return

    def __setitem__(self, key, val):
        #print 'setitem', key, val
        flags = self._flags
        ns = self._ns

        key, flags = self.pack_key(key, 0)
        val, flags = self.pack_val(val, flags)

        conn = self._conn
        table = self._table
        query = insert(table)
        query = query.values(
            sqldict_ns=ns,
            sqldict_key=key,
            sqldict_val=val,
            sqldict_flags=flags,
        )
        try:
            conn.execute(query)
        except IntegrityError:
            self._update(key, val, flags)




def sqldict(dburi='sqlite://', engine=None, conn=None, ns='', tablename='',
                create=0, **kw):
    '''
    '''

    if not (dburi or engine or conn):
        error = 'sqldict(): must specify exactly one of `dburi`, `engine` or `conn`'
        raise SQLDictError(error)

    if not engine and not conn and dburi=='sqlite://':
        create = 1
        tablename = 'sqldict_dummy'

    if not tablename:
        error = 'sqldict(): must specify `tablename`'
        raise SQLDictError(error)

    if not engine and not conn:
        engine = create_engine(dburi)
    if engine:
        conn = engine.connect()

    return BaseSQLDict(conn=conn, ns=ns, tablename=tablename, create=create, **kw)




