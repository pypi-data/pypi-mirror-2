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
            print 'IS',key,val
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

    def test_mysql2(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict(engine=engine, tablename='haha', create=1)
        self.large(d)

    def test_mysql3(self):
        engine = create_engine('mysql://sqldict:balalajkaperestrojka@localhost/sqldict')
        conn = engine.connect()
        d = sqldict(conn=conn, tablename='haha', create=1)
        self.large(d)
        
        

unittest.main()
