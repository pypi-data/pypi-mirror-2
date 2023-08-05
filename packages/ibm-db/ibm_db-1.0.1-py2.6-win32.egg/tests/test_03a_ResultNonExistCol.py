# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

import unittest, sys
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

  def test_03a_ResultNonExistCol(self):
    obj = IbmDbTestFunctions()
    obj.assert_expect(self.run_test_03a)

  def run_test_03a(self):
    conn = ibm_db.connect(config.database, config.user, config.password)
    server = ibm_db.server_info( conn )

    if conn:
      stmt = ibm_db.exec_immediate(conn, "SELECT id, breed, name, weight FROM animals WHERE id = 0")
      
      while ( ibm_db.fetch_row(stmt) ):
         breed = ibm_db.result(stmt, 1)
         print "string(%d) \"%s\"" % (len(breed), breed)
         if (server.DBMS_NAME[0:3] == 'IDS'):
            name = ibm_db.result(stmt, "name")
         else:
            name = ibm_db.result(stmt, "NAME")
         print "string(%d) \"%s\"" % (len(name), name)
    
         # following field does not exist in result set
         if (server.DBMS_NAME[0:3] == 'IDS'):
           name = ibm_db.result(stmt, "passport")
         else:
           name = ibm_db.result(stmt, "PASSPORT")
         print name
      ibm_db.close(conn)
      
    else:
      print "Connection failed."

#__END__
#__LUW_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#None
#__ZOS_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#None
#__SYSTEMI_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#None
#__IDS_EXPECTED__
#string(3) "cat"
#string(16) "Pook            "
#None
