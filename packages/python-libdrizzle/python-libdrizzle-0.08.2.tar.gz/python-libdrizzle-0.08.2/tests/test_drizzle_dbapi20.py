#!/usr/bin/env python

# Test suite driver for libdrizzle.

import dbapi20
import unittest
import sys
import os.path
from subprocess import Popen, PIPE
from optparse import OptionParser
# Ensure the current build gets tested.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from drizzle import db

class test_drizzle_dbapi(dbapi20.DatabaseAPI20Test):
    driver = db
    connect_args = ()
    connect_kw_args = {"host": "localhost",
                       "port": 9306,
                       "database": "dbapi20_test"}

    lower_func = 'lower' # For stored procedure test

    def setUp(self):
        # Call superclass setUp In case this does something in the
        # future
        dbapi20.DatabaseAPI20Test.setUp(self) 

        try:
            con = self._connect()
            cur = con.cursor()
            # Attempt a query as libdrizzle will connect even if the DB does not exist.
            cur.execute("show tables;")
            con.close()
        except:
            # The drizzle client should be in your path allowing the DB to be
            # created if necessary.
            cmd = "drizzle -h {host} -p {port} -e 'create database {database}'"\
                  .format(**self.connect_kw_args)
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
            (cin, cout) = (p.stdin, p.stdout)
            cin.close()
            cout.read()

    def tearDown(self):
        dbapi20.DatabaseAPI20Test.tearDown(self)

    def test_nextset(self): pass
    def test_setoutputsize(self): pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-H", "--host", dest="host", default="localhost",
                      help="Host running the Drizzle server on which the test\
                            DB should be run.")
    parser.add_option("-p", "--port", type="int", dest="port", default=9306,
                      help="Port the Drizzle server is running on.")
    parser.add_option("-D", "--database", dest="database", default="dbapi20_test",
                      help="Database to use for testing on the Drizzle server.")
    (options, args) = parser.parse_args()
    test_drizzle_dbapi.connect_kw_args = vars(options)

    suite = unittest.TestLoader().loadTestsFromTestCase(test_drizzle_dbapi)
    unittest.TextTestRunner(verbosity=2).run(suite)
