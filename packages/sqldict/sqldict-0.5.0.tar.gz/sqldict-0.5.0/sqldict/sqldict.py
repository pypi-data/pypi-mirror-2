#
# By Krister Hedfors
#
# + pack/unpack everywhere
# + db-sorted iteritems
# |- inform about broken ordering of anything but strings
# + ns functionality transparently optional
# + create class with a mapping of an existing table
# + move ns- and flags stuff to dedicated functions
#
# - add user controlled key preprocessor and val processor
# - add raw query template as valgetter
# - if valgetter is a string, it's used as an SQL template
#       which is fed with key to obtain val
# - build bunch of rawsql-dicts and build code snipplets
#       with which to extract values
# - build programs using these rawsql-dicts as components
# - joins work just as well, as it's raw dicts
# - iterations simply leave out which constraint
# keymod, valmod, valmodin alongside valgetter
#
#
__all__ = ['sqldict']
__doc__ = '''
    sqldict - dict with sqlalchemy database-agnostic back-end
              capable of using picklable objects as both
              keys and values
'''


import doctest
from UserDict import DictMixin
import pickle
import cPickle
import base64

from sqlalchemy import create_engine


class SQLDictException(Exception): pass
class SQLDictError(SQLDictException): pass


from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy.exc import (
        NoSuchTableError,
        IntegrityError
)


_KEYSIZE = 1000-64
_VALSIZE = 4000
_NSSIZE  = 64

_DEFAULT_KEYCOL   = "sqldict_key"
_DEFAULT_VALCOL   = "sqldict_val"
_DEFAULT_NSCOL    = "sqldict_ns"
_DEFAULT_FLAGSCOL = "sqldict_flags"
_DEFAULT_VALGETTER = lambda row:row[_DEFAULT_VALCOL]
_DEFAULT_KEYMOD   = lambda key:key
_DEFAULT_VALMODIN = lambda val:val
_DEFAULT_VALMODOUT = lambda val:val

_DEFAULT_KEYTYPE=String(_KEYSIZE)
_DEFAULT_VALTYPE=String(_VALSIZE)


def log_execute(conn, query):
    #print str(query)
    result = conn.execute(query)
    return result


class SetConfig(object):
    def set(self, **kw):
        for key, val in kw.iteritems():
            setattr(self, "_"+key, val)


class SQLDict(DictMixin, SetConfig):
    '''
    >>> e = create_engine('sqlite://')
    >>> d = SQLDict(e.connect(), 'asd', create=1)
    '''


    _F_SERIALIZED_KEY = 1 << 0
    _F_SERIALIZED_VAL = 1 << 1
    _F_UNICODE_KEY    = 1 << 2
    _F_UNICODE_VAL    = 1 << 3


    def __init__(self,  conn, tablename,
                            create=0,
                            ns='',
                            keycol=_DEFAULT_KEYCOL,
                            valcol=_DEFAULT_VALCOL,
                            nscol=_DEFAULT_NSCOL,
                            flagscol=_DEFAULT_FLAGSCOL,
                            keytype=_DEFAULT_KEYTYPE,
                            valtype=_DEFAULT_KEYTYPE,
                            valgetter=_DEFAULT_VALGETTER,
                            keymod=_DEFAULT_KEYMOD,
                            valmodin=_DEFAULT_VALMODIN,
                            valmodout=_DEFAULT_VALMODOUT,
                            extended=0, # 0 or 1; simple or complex types
                            sort=1,         # 0=dont, 1=keys, 2=values(broken)
                            iterate=0,

                            nssize=_NSSIZE,
                            ):
        '''
        '''
        if hasattr(conn, 'connect'):
            self._conn = conn.connect()
        else:
            self._conn = conn
        self._tablename = tablename
        self._keycol = keycol #as string name
        self._valcol = valcol #as string name
        self._nscol = nscol #as string name
        self._flagscol = flagscol
        self._keytype = keytype
        self._valtype = valtype
        self._valgetter = valgetter
        self._keymod = keymod
        self._valmodin = valmodin
        self._valmodout = valmodout
        self._extended = extended
        self._ns = ns
        self._create = create
        self._sort = sort
        self._iterate = iterate
        self._nssize =  nssize
        self._meta = MetaData()
        self._meta.bind = conn
        self._keycoltype = None # set by _autoload_table()
        self._keyvaltype = None # set by _autoload_table()
        #

        #
        # If user changes valcol but not valgetter we need
        # to set it for him, otherwise __getitem__ wont work.
        #
        if valcol != _DEFAULT_VALCOL:
            if valgetter != _DEFAULT_VALGETTER:
                pass
            else:
                self._valgetter = lambda row:row[valcol]

        #if create:
        #    if self._extended is None:
        #        self._extended = 1
        try:
            self._table = self._autoload_table()
        except NoSuchTableError, e:
            if create:
                self._create_table()
            else:
                msg = 'initialize sqldict with `create=1` to create table'
                error = (msg, e)
                raise NoSuchTableError(error)

    def _autoload_table(self):
        tablename = self._tablename
        meta = self._meta
        keycol = self._keycol
        keyval = self._valcol
        #
        table = Table(tablename, meta, autoload=True)
        self._keycoltype = type( getattr(table.c, keycol))
        self._keyvaltype = type( getattr(table.c, keyval))
        return table

    def _create_table(self):
        keycol = self._keycol
        valcol = self._valcol
        nscol = self._nscol
        flagscol = self._flagscol
        keytype = self._keytype
        valtype = self._valtype
        nssize = self._nssize
        ns = self._ns
        extended = self._extended
        #
        columns = [
            Column(keycol, keytype, nullable=False, primary_key=True),
            Column(valcol, valtype, nullable=False),
        ]
        if extended:
            columns.append(
                Column(flagscol, Integer, nullable=False),
            )
        if ns:
            columns.append(
                Column(nscol,  String(nssize), nullable=False, primary_key=True)
            )
        table = Table(self._tablename, self._meta, *columns)
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
        table = self._table
        conn = self._conn
        keycol = self._keycol
        valcol = self._valcol
        flagscol = self._flagscol
        extended = self._extended
        key_column = self._get_key_column()
        #
        query = update(table)
        query = self._apply_ns_where_clause(query)
        query = query.where(key_column == key)

        values = {
            valcol : val
        }

        if extended:
            values[flagscol] = flags

        query = query.values(**values)
        log_execute(conn, query)

    def drop(self):
        self._table.drop()

    def _pack_key(self, key, flags):
        extended = self._extended
        keycoltype = self._keytype
        #
        if extended and isinstance(keycoltype, String):
            key_type = type(key)
            if key_type is str:
                pass
            elif key_type is unicode:
                flags |= self._F_UNICODE_KEY
            else:
                flags |= self._F_SERIALIZED_KEY
                key = self._serialize(key)
        return (key, flags)

    def _unpack_key(self, key, flags):
        extended = self._extended
        keycoltype = self._keytype
        #
        if extended and isinstance(keycoltype, String):
            if flags & self._F_SERIALIZED_KEY:
                key = self._deserialize(key)
            elif type(key) is unicode and not (flags & self._F_UNICODE_KEY):
                key = str(key)
        return key


    def _pack_val(self, val, flags):
        extended = self._extended
        valcoltype = self._valtype
        #
        if extended and isinstance(valcoltype, String):
            val_type = type(val)
            if val_type is str:
                pass
            elif val_type is unicode:
                flags |= self._F_UNICODE_VAL
            else:
                flags |= self._F_SERIALIZED_VAL
                val = self._serialize(val)
        return (val, flags)

    def _unpack_val(self, val, flags):
        extended = self._extended
        valcoltype = self._valtype
        #
        if extended and isinstance(valcoltype, String):
            if flags & self._F_SERIALIZED_VAL:
                val = self._deserialize(val)
            elif type(val) is unicode and not (flags & self._F_UNICODE_VAL):
                val = str(val)
        return val

    def _get_key_column(self):
        table = self._table
        return getattr(table.c, self._keycol)

    def _get_val_column(self):
        table = self._table
        return getattr(table.c, self._valcol)

    def _get_ns_column(self):
        table = self._table
        return getattr(table.c, self._nscol)

    def _get_flags_column(self):
        table = self._table
        return getattr(table.c, self._flagscol)

    #def _get_sort_column(self, flags):
    #    "NOT USED"
    #    sort = self._sort
    #    #
    #    if sort == 1:
    #        return self._get_key_column()
    #    elif sort == 2:
    #        return self._get_val_column()

    def _apply_ns_where_clause(self, query):
        table = self._table
        ns = self._ns
        if ns:
            ns_column = self._get_ns_column()
            query = query.where(ns_column == ns)
        return query

    def _apply_key_where_clause(self, query, key):
        key_column = self._get_key_column()
        query = query.where( key_column == key)
        return query

    def _apply_ordering(self, query):
        sort = self._sort
        #
        if sort == 1:
            key_column = self._get_key_column()
            query = query.order_by( key_column)
        if sort == 2:
            val_column = self._get_val_column()
            query = query.order_by( val_column)
        return query

    def _select(self, columns):
        table = self._table
        extended = self._extended
        #
        if extended:
            columns += [self._get_flags_column()]
        query = select(columns)
        query = self._apply_ns_where_clause(query)
        query = self._apply_ordering(query)
        return query

    def _select_items(self):
        key_column = self._get_key_column()
        val_column = self._get_val_column()
        #
        columns = [
            key_column,
            val_column,
        ]
        return self._select(columns)

    def _select_keys(self):
        key_column = self._get_key_column()
        val_column = self._get_val_column()
        #
        columns = [
            key_column,
            val_column,
        ]
        return self._select(columns)

    def _select_values(self):
        key_column = self._get_key_column()
        val_column = self._get_val_column()
        #
        columns = [
            key_column,
            val_column,
        ]
        return self._select(columns)


    #
    # dict methods
    # 
    def iteritems(self):
        conn = self._conn
        keycol = self._keycol
        flagscol = self._flagscol
        extended = self._extended
        valgetter = self._valgetter
        #
        query = self._select_items()
        #print query
        result = log_execute(conn, query)
        for row in result:
            key = row[keycol]
            val = valgetter(row)
            flags = 0
            if extended:
                flags = row[flagscol]
            key = self._unpack_key(key, flags)
            val = self._unpack_val(val, flags)
            yield (key, val)

    def iterkeys(self):
        conn = self._conn
        keycol = self._keycol
        flagscol = self._flagscol
        extended = self._extended
        #
        query = self._select_keys()
        result = log_execute(conn, query)
        for row in result:
            key = row[keycol]
            flags = 0
            if extended:
                flags = row[flagscol]
            key = self._unpack_key(key, flags)
            yield key

    def itervalues(self):
        conn = self._conn
        extended = self._extended
        flagscol = self._flagscol
        valgetter = self._valgetter
        #
        query = self._select_values()
        result = log_execute(conn, query)
        for row in result:
            val = valgetter(row)
            flags = 0
            if extended:
                flags = row[flagscol]
            val = self._unpack_val(val, flags)
            yield val

    def namespaces(self):
        conn = self._conn
        ns = self._ns
        nscol = self._nscol
        ns_column = None # set after `if not ns:`
        table = self._table
        sort = self._sort
        #
        if not ns:
            error = 'namespaces(): not supported, sqldict instantiated without `ns=`'
            raise Exception(error)
        ns_column = self._get_ns_column()
        query = select([ distinct(ns_column) ])
        if sort == 1:
            query = query.order_by(ns_column)
        if sort == 2:
            query = query.order_by(ns_column)
        #print query
        result = log_execute(conn, query)
        namespaces = []
        for row in result:
            ns = row[nscol]
            namespaces.append(ns)
        return namespaces

    def _dup_kwargs(self):
        kwargs = dict(
            conn=self._conn,
            tablename=self._tablename,
            ns=self._ns,
            create=0,
            sort=self._sort,
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
        extended = self._extended
        keycol = self._keycol
        flagscol = self._flagscol
        #
        query = self._select_keys()
        #print query
        result = log_execute(conn, query)
        keys = []
        for row in result:
            key = row[keycol]
            flags = 0
            if extended:
                flags = row[flagscol]
            key = self._unpack_key(key, flags)
            keys.append(key)
        return keys

    def __iter_getitem__(self, key, ordering=0):
        #print 'getitem', key
        #if not type(key) in (str, unicode):
        #    key = self._serialize(key)
        conn = self._conn
        table = self._table
        flagscol = self._flagscol
        key_column = self._get_key_column()
        extended = self._extended
        valgetter = self._valgetter
        keymod = self._keymod
        valmodout = self._valmodout
        #
        if keymod:
            key = keymod(key)
        key, _ = self._pack_key(key, 0)
        query = select([table])
        query = self._apply_ns_where_clause(query)
        query = query.where( key_column == key)
        if ordering:
            query = self._apply_ordering(query)

        result = log_execute(conn, query)
        for row in result:
            #
            val = valgetter(row)
            flags = 0
            if extended:
                flags = row[flagscol]

            val = self._unpack_val(val, flags)
            if valmodout:
                val = valmodout(val)
            yield val

    def __getitem__(self, key):
        iterate = self._iterate
        if iterate:
            return self.__iter_getitem__(key, ordering=1)
        for val in self.__iter_getitem__(key):
            return val
        raise KeyError


    def __delitem__(self, key):
        #print 'delitem', key
        conn = self._conn
        table = self._table
        keymod = self._keymod
        #
        if keymod:
            key = keymod(key)
        if not type(key) in (str, unicode):
            key = self._serialize(key)
        query = table.delete()
        query = self._apply_ns_where_clause(query)
        query = self._apply_key_where_clause(query, key)

        result = log_execute(conn, query)
        if result.rowcount == 0:
            raise KeyError
        elif result.rowcount > 1:
            error = 'Multiple rows affected by delete: %d' %result.rowcount
            raise SQLDictException(error)
        return

    def __setitem__(self, key, val):
        keycol = self._keycol
        valcol = self._valcol
        flagscol = self._flagscol
        nscol = self._nscol
        extended = self._extended
        ns = self._ns
        keymod = self._keymod
        valmodin = self._valmodin
        #
        if keymod:
            key = keymod(key)
        if valmodin:
            val = valmodin(val)

        key, flags = self._pack_key(key, 0)
        val, flags = self._pack_val(val, flags)

        conn = self._conn
        table = self._table
        query = insert(table)

        values = {
            keycol : key,
            valcol : val,
        }
        if extended:
            values[flagscol] = flags
        if ns:
            values[nscol] = ns

        query = query.values(**values)
        try:
            log_execute(conn, query)
        except IntegrityError:
            self._update(key, val, flags)




def sqldict_old(dburi='sqlite://', engine=None, conn=None,
                tablename='',
                ns='',
                create=0,
                extended=0,
                **kw):
    '''
    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('sqlite://')
    >>> conn = engine.connect()
    >>> d1 = sqldict_old(dburi='sqlite://', tablename='t1', create=1)
    >>> d2 = sqldict_old(engine=engine,     tablename='t2', create=1)
    >>> d3 = sqldict_old(conn=conn,         tablename='t3', create=1)
    >>> d4 = sqldict_old(conn=conn,         tablename='t3', ns='asd', create=1)

    And do your dict work.
    Both keys and values can be of arbitrary picklable type.

    Parameter ns='someNameSpace' makes multiple sqldicts able
    to work in the same database table as the primary key
    of the table is (ns, key). Default ns is ''.
    '''

    if not (dburi or engine or conn):
        error = 'sqldict(): must specify exactly one of `dburi`, `engine` or `conn`'
        raise SQLDictError(error)

    if not tablename:
        error = 'sqldict(): must specify `tablename`'
        raise SQLDictError(error)

    if not engine and not conn:
        engine = create_engine(dburi)
    if engine:
        conn = engine.connect()

    return SQLDict(conn=conn, ns=ns, tablename=tablename, 
                    create=create, extended=extended, **kw)



__engine = create_engine("sqlite://")
__conn = __engine.connect()
ConnectionType = type(__conn)
del __conn
del __engine


def sqldict(db, tablename,
                    keycol=_DEFAULT_KEYCOL,
                    valcol=_DEFAULT_VALCOL,
                    keytype=_DEFAULT_KEYTYPE,
                    valtype=_DEFAULT_VALTYPE,
                    valgetter=_DEFAULT_VALGETTER,
                    keymod=_DEFAULT_KEYMOD,
                    valmodin=_DEFAULT_VALMODIN,
                    valmodout=_DEFAULT_VALMODOUT,
                        iterate=0,
                        serialize=0,
                        create=0,
                        sort=1,
                        ns=None,
                        ):

    """
    The various dictionaries, dN, can be used just as an ordinary dict.

    >>> #d0 = sqldict("mysql://user:pass@dbhost/dbname", "table0", create=1)
    >>> e = create_engine("sqlite://")
    >>> d1 = sqldict(e, "table2", create=1)
    >>> d2 = sqldict(e, "table3", create=2, valtype=Integer)
    >>> contents = {"asd":123}
    >>> d1.update(contents)
    >>> d2.update(contents)
    >>> assert d1["asd"] == "123"
    >>> assert d2["asd"] == 123

    >>> _ = e.execute("create table asd (i integer, s varchar(50))")
    >>> _ = e.execute("insert into asd values (42, 'gubbe')")
    >>> _ = e.execute("insert into asd values (99, 'hatt')")
    >>> d3 = sqldict(e, "asd", keycol="s", valcol="i")
    >>> d4 = sqldict(e, "asd", keycol="i", valcol="s")
    >>> #d5 = sqldict(e, "asd", keycol="s", valgetter=lambda r:r)
    >>> assert d3["gubbe"] == 42
    >>> assert d4[42] == "gubbe"
    >>> #assert d5["gubbe"]["i"] == 42

    broken (at least mysql) when combining keytype and serialize,
    it tries to serialize 42.
    FIXME: d[int] = Integer or d[Integer]
    >>> from sqlalchemy import *
    >>> d = sqldict(e, "laarge", create=1, serialize=1, keytype=Integer)
    >>> d[42] = "galning"
    """

    conn = None
    #
    
    if type(db) is str:
        engine = create_engine(db)
        conn = engine.connect()
    elif hasattr(db, "connect"):
        conn = db.connect()
    else:
        conn = db

    if not isinstance(conn, ConnectionType):
        msg = "sqldict `db` arg must be database connect string, " +\
              "sqlalchemy engine or engine.connect()"
        raise SQLDictError(msg)


    return SQLDict(conn=conn, tablename=tablename,
                    ns=ns,
                    extended=serialize,
                    create=create,
                    sort=sort,
                    keycol=keycol,
                    valcol=valcol,
                    keytype=keytype,
                    valtype=valtype,
                    valgetter=valgetter,
                    keymod=keymod,
                    valmodin=valmodin,
                    valmodout=valmodout,
                    iterate=iterate,
                    )


if __name__ == '__main__':
    import doctest
    doctest.testmod()
