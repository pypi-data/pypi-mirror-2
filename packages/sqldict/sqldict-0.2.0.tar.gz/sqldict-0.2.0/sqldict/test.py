from sqldict import sqldict

import unittest
from sqlalchemy import *


class Test_sqldict(unittest.TestCase):

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
            print 'IS',key,val, type(val)
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


        d = sqldict(dburi='sqlite://', tablename='haha', create=1)

    def test_mysql1(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict(dburi='sqlite://', tablename='haha', create=1)
        self.large(d)
        d.drop()

    def test_mysql2(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict(engine=engine, tablename='haha', create=1)
        self.large(d)
        d.drop()

    def test_mysql3(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict(conn=conn, tablename='haha', create=1)
        self.large(d)
        d.drop()

    def test_sorted(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        prefix='rr'
        d = sqldict(conn=conn, tablename='sorted_dict', create=1, ns=prefix+'asd')
        d['ggg'] = 723
        d['aaa'] = 123
        d['bbb'] = 223
        d['fff'] = 223
        d['eee'] = 523
        d['ccc'] = 323
        d['ddd'] = 423
        keys = d.keys()
        print keys
        assert keys == sorted(keys)
        d.drop()

    def test_iteritems(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        prefix='rr'
        d = sqldict(conn=conn, tablename='test_iteritems', create=1, ns=prefix+'asd')
        d['ggg'] = 723
        d['aaa'] = 123
        d['bbb'] = 223
        d['fff'] = 223
        d['eee'] = 523
        d['ccc'] = 323
        d['ddd'] = 423
        for key, val in d.iteritems():
            print 'iteritems', key, val
        d.drop()

    def test_namespaces(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        prefix='rr'
        nslist = ['na', 'nb', 'ny', 'nn', 'nm']
        for ns in nslist:
            d = sqldict(conn=conn, tablename='test_namespaces2',
                    create=1, ns=ns)
            d['aa'] = 'asdasd'
            d['bb'] = 'qweqwe'
            d['cc'] = 'rtyrty'
        print d.namespaces()
        assert d.namespaces() == ['na', 'nb', 'nm', 'nn', 'ny']
        d.drop()


        
        

unittest.main()
