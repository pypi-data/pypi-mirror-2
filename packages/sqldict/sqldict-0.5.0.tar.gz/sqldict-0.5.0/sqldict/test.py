from sqldict import sqldict, sqldict_old, _KEYSIZE, _VALSIZE

import doctest
import unittest
from sqlalchemy import *

SQLITEFS_FILE = "//tmp/.sqlitedb_test_sqlitefs"


def randstring(len):
    """
    >>> assert 1==1
    """
    import uuid
    s = uuid.uuid4().__str__().replace("-", "")[:len]
    return s


class Test_sqldict_basic(unittest.TestCase):

    _mysql_uri = 'mysql://sqldict:balalajkaperestrojka@localhost/sqldict'

    _engines = engines = {
        "sqlite"   : create_engine("sqlite://"),
        "sqlitefs" : create_engine("sqlite://"+SQLITEFS_FILE),
        "mysql"    : create_engine(_mysql_uri),
    }
    _testtables = dict(
        t_char_char = """
            CREATE TABLE t_char_char (
                xkey varchar(%(keysize)s),
                xval varchar(%(valsize)s)
            )
        """,
        t_int_char = """
            CREATE TABLE t_int_char (
                xkey integer,
                xval varchar(%(valsize)s)
            )
        """,
        t_int_int = """
            CREATE TABLE t_int_int (
                xkey integer,
                xval integer
            )
        """,
    )
    def tablenames(self):
        return self._testtables.iterkeys()

    def setUp(self):
        for query_template in self._testtables.itervalues():
            query = query_template % dict(
                        keysize = _KEYSIZE,
                        valsize = _VALSIZE,
            )
            for engine in self._engines.itervalues():
                engine.execute(query)

    def tearDown(self):
        import os
        for tablename in self._testtables.iterkeys():
                query = "drop table "+ tablename
                for engine in self._engines.itervalues():
                    engine.execute(query)
        try:
            os.unlink(SQLITEFS_FILE)
        except:
            pass

    def serialization_and_types(self, engine):
        a = sqldict(engine, "serty1", create=1, serialize=1)
        b = sqldict(engine, "serty2", create=1, serialize=1, keytype=Integer)
        try:
            a[1] = (2,3)
            assert a[1] == (2,3)

            b[4] = (5,6)
            assert b[4] == (5,6)

        finally:
            a.drop()
            b.drop()
            pass

    def compare(self, engine, manipulator, tablename):
        facit = {}
        d = sqldict(engine, "setitem_getitem", create=1)
        manipulator(d)
        manipulator(facit)
        assert d == facit
        d.drop()

    def test_main(self):
        engines = self._engines
        #
        for name, engine in self._engines.iteritems():
            self.compare( engine, self.set_get_del, "set_get_del")
            self.sorting(engine)
            self.serialization_and_types(engine)
            self.custom_valgetter(engine)
            self.keymod_valmod(engine)
            self.iterate(engine)
            factor = 1
            self.large_update(engine, count=factor*10)

    def set_get_del(self, d):
        assert len(d) == 0
        d["asd"] = "qwe"
        assert d["asd"] == "qwe"
        assert len(d) == 1
        del d["asd"]
        assert len(d) == 0

    def sorting(self, engine):
        ref = {}
        d = sqldict(engine, "sort_keys", create=1)
        for i in xrange(12):
            rand = randstring(10)
            d[rand] = "%d" % i
            ref[rand] = "%d" % i
        d._sort = 1
        assert len(d.keys())   and d.keys()   == sorted(ref.keys())
        d._sort = 2
        assert len(d.values()) and d.values() == sorted(ref.values())
        d._sort = 1
        assert len(d.items())  and d.items()  == sorted(ref.items())
        d.drop()

    def large_update(self, engine, count=100):
        src = {}
        for i in xrange(count):
            src[randstring(4)] = randstring(10)
        d = sqldict(engine, "large_update", create=1)
        d.update(src)
        assert len(d) == count
        assert d == src
        d.drop()

    def custom_valgetter(self, engine):
        def get_row(row):
            return row
        d = sqldict(engine, "test_valgetter",
                        keycol="kk",
                        valcol="vv",
                        valgetter=get_row,
                        create=1,
                        serialize=1,
                        )
        try:
            d["asd"] = "qwe"
            assert d["asd"]["kk"] == "asd"
            assert d["asd"]["vv"] == "qwe"
            assert d["asd"].kk == "asd"
            assert d["asd"].vv == "qwe"
        finally:
            d.drop()

    def keymod_valmod(self, engine):
        def keymod(key):
            return key+"KK"
        def valmodout(val):
            return val+"VV"
        d = sqldict(engine, "test_valgetter",
                        keycol="kk",
                        valcol="vv",
                        create=1,
                        serialize=1,
                        keymod=keymod,
                        valmodout=valmodout,
                        )
        d2 = sqldict(engine, "test_valgetter",
                        keycol="kk",
                        valcol="vv",
                        #create=1,
                        serialize=1,
                        #keymod=keymod,
                        #valmodout=valmodout,
                        )
        try:
            d["asd"] = "qwe"
            assert d["asd"] == "qweVV"
            assert d2["asdKK"] == "qwe"

            d2.set(valmodin  = lambda val : val+val)
            d2.set(valmodout = lambda val : val.upper())
            d2["x"] = "y"
            assert d2["x"] == "YY"
        finally:
            d.drop()

    def iterate(self, engine):
        for val in ["asd", "qwe", "123", "haha", "hoho"]:
            engine.execute("""
                INSERT INTO t_char_char
                VALUES ('foo', '%s')
            """ % val
            )
        d = sqldict(engine, "t_char_char",
                        keycol="xkey",
                        valcol="xval",
                        iterate=1,
                        sort=1,
                        )
        #
        # sort by key
        #
        i = 0
        for i, val in enumerate(d["foo"]):
            if i==0: assert val == "asd"
            if i==1: assert val == "qwe"
            if i==2: assert val == "123"
            if i==3: assert val == "haha"
            if i==4: assert val == "hoho"
        assert i==4
        #
        # sort by val
        #
        d.set(sort=2)
        i = 0
        for i, val in enumerate(d["foo"]):
            if i==0: assert val == "123"
            if i==1: assert val == "asd"
            if i==2: assert val == "haha"
            if i==3: assert val == "hoho"
            if i==4: assert val == "qwe"
        assert i==4







class Test_sqldict_old(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite://')

    def test_test(self):
        self.assertEqual (1,1)
    
    def large(self, d):
        d['a'] = '1'
        d['b'] = 2
        d['c'] = 3.0
        d[4] = {'foo':'bar'}
        d[5] = u'x'
        d[('asd',123)] = dict(qwe=456)
        count = 4
        for key, val in d.iteritems():
            #print 'IS',key,val, type(val)
            if key=='a':
                assert val=='1'
                assert d[key]==val
            if key=='b':
                assert val==2
                assert d[key]==val
            if key=='c':
                assert val==3.0
                assert d[key]==val
            if key==4:
                assert val=={'foo':'bar'}
                assert d[key]==val
            if key==5:
                assert val==u'x'
                assert d[key]==val
            if key==('asd',123):
                assert val==dict(qwe=456)
                assert d[key]==val

        assert len(d) == 6
        del d['a']
        assert len(d) == 5
        del d['b']
        assert len(d) == 4
        del d['c']
        assert len(d) == 3
        del d[4]
        assert len(d) == 2
        del d[5]
        assert len(d) == 1
        del d[('asd',123)]
        assert len(d) == 0

    def test_sqlite_broken(self):
        #engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        #conn = engine.connect()
        d = sqldict_old(dburi='sqlite://', tablename='haha',
                        create=1, extended=1)
        self.large(d)
        d.drop()

    def test_mysql1(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict_old(conn=conn, tablename='haha', ns='ppp',
                        create=1, extended=1)
        self.large(d)
        d.drop()

    def test_mysql2(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict_old(engine=engine, tablename='haha', ns='qqq',
                        create=1, extended=1)
        self.large(d)
        d.drop()

    def test_mysql3(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict_old(conn=conn, tablename='haha', ns='rrr',
                        create=1, extended=1)
        self.large(d)
        d.drop()

    def test_sorted(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        prefix='rr'
        d = sqldict_old(conn=conn, tablename='sorted_dict',
                        create=1, extended=0) #, ns=prefix+'asd')
        #d = sqldict(conn=conn, tablename='sorted_dict', create=1) #, ns=prefix+'asd')
        #d = sqldict(conn=conn, tablename='sorted_dict', create=1, ns=prefix+'asd')
        d['ggg'] = 723
        d['aaa'] = 123
        d['bbb'] = 223
        d['fff'] = 223
        d['eee'] = 523
        d['ccc'] = 323
        d['ddd'] = 423
        keys = d.keys()
        #print keys
        assert keys == sorted(keys)
        d.drop()

    def test_iteritems(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        prefix='rr'
        d = sqldict_old(conn=conn, tablename='test_iteritems',
                        create=1, extended=1, ns=prefix+'asd')
        d['ggg'] = 723
        d['aaa'] = 123
        d['bbb'] = 223
        d['fff'] = 223
        d['eee'] = 523
        d['ccc'] = 323
        d['ddd'] = 423
        for key, val in d.iteritems():
            pass
            #print 'iteritems', key, val
        d.drop()

    def test_iterkeys(self):
        d = sqldict_old(tablename='test_iterkeys',
                        create=1, extended=1)
        d['a'] = 'asd'
        d['e'] = 'asd'
        d['f'] = 'asd'
        d['b'] = 'asd'
        d['d'] = 'asd'
        d['c'] = 'asd'
        for key in d.iterkeys():
            pass
        keys = list(d.iterkeys())
        assert len(keys) == 6
        assert keys == sorted(keys)
        d.drop()

    def test_iterkeys_int(self):
        d = sqldict_old(tablename='test_iterkeys',
                        create=1, extended=1)
        d[6] = 'asd'
        d[3] = 'asd'
        d[5] = 'asd'
        d[1] = 'asd'
        d[2] = 'asd'
        d[4] = 'asd'
        keys = list(d.iterkeys())
        assert len(keys) == 6
        assert keys == sorted(keys)
        d.drop()

    def test_itervalues_int(self):
        d = sqldict_old(tablename='test_iterkeys',
                        create=1, extended=1, sort=2)
        d['asd'] = 3
        d['qwe'] = 6
        d['foo'] = 2
        d['bar'] = 1
        d['sdf'] = 4
        d['wer'] = 5
        values = list(d.itervalues())
        assert len(values) == 6
        assert values == sorted(values)
        d.drop()

    def test_itervalues(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict_old(conn=conn, tablename='test_itervalues',
                        create=1, extended=1, sort=2)
        d['d'] = 'esd'
        d['a'] = 'asd'
        d['c'] = 'fsd'
        d['f'] = 'csd'
        d['e'] = 'bsd'
        d['b'] = 'dsd'
        values = list(d.itervalues())
        assert values == sorted(values)
        d.drop()

    def test_namespaces(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        prefix='rr'
        nslist = ['na', 'nb', 'ny', 'nn', 'nm']
        d = None
        for ns in nslist:
            d = sqldict_old(conn=conn, tablename='xibi', ns=ns,
                    create=1, extended=1)
            #print d.namespaces()
            d['aa'] = 'asdasd'
            d['bb'] = 'qweqwe'
            d['cc'] = 'rtyrty'
        #print 'NAMESPACES', d.namespaces()
        assert d.namespaces() == ['na', 'nb', 'nm', 'nn', 'ny']
        d.drop()


    def create_test_asdasd(self, conn):
        try:
            self.drop_test_asdasd(conn)
        except:
            pass
        sql = '''
        create table test_asdasd (ref varchar(20),
                                    name varchar(20),
                                    age integer)
        '''
        conn.execute(sql)

    def drop_test_asdasd(self, conn):
        sql = '''
        drop table test_asdasd
        '''
        conn.execute(sql)

    def populate_test_asdasd(self, conn):
        sql = '''
        insert into test_asdasd (ref, name, age)
                    values      ('rr', 'nn', 123)
        '''
        conn.execute(sql)

    def test_custom_columns(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        self.create_test_asdasd(conn)
        try:
            self.populate_test_asdasd(conn)
            from functools import partial


            mydict = partial(sqldict_old, conn=conn, tablename="test_asdasd")
            name_by_ref = mydict(   valcol="name", keycol="ref")
            name_by_age = mydict(   valcol="name", keycol="age")
            age_by_ref  = mydict(   valcol="age", keycol="ref")
            age_by_name = mydict(   valcol="age", keycol="name")
            ref_by_name = mydict(   valcol="ref", keycol="name")
            ref_by_age  = mydict(   valcol="ref", keycol="age")

            assert name_by_ref["rr"]  == "nn"
            assert name_by_age["123"] == "nn"
            assert name_by_age[123]   == "nn"
            assert ref_by_name["nn"]  == "rr"
            assert ref_by_age["123"]  == "rr"
            assert ref_by_age[123]    == "rr"
            assert age_by_ref["rr"]   == 123
            assert age_by_name["nn"]  == 123

            for key,val in name_by_ref.iteritems():
                assert key == "rr"
                assert val == "nn"

            #name_by_ref["rr"] = "nytt namn"

            #for key,val in name_by_ref.iteritems():
            #    print "FAILFAIL", key
            #    assert key == "rr"
            #    assert val == "nytt namn"

            #name_by_ref["rr"] = "nn HAHA"

        finally:
            self.drop_test_asdasd(conn)
            pass
        


if __name__ == "__main__":
    doctest.testmod()
    unittest.main()
