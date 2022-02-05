import jibr.jbHttpConn as jbHttpConn
import jibr.jbFunc as jbFunc
import jibr.jbRecord as jbRecord

import unittest

class TestRecord( unittest.TestCase ):

    # ========================================================================================
    # ... because we can't make an HTTP connection in a unit test (w/o a mock environment)
    def test_pointing_at_a_record( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record abc-25" )

        self.assertTrue( jbRecord.record != None )
        self.assertEqual( jbRecord.record['key'], 'ABC-25' )

    # ========================================================================================
    # ... because we can't make an HTTP connection in a unit test (w/o a mock environment)
    def test_clearing_a_record( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record abc-25" )
        jbFunc.parse( "record clear" )
        self.assertTrue( jbRecord.record == None )

# ======================================================================
if __name__ == '__main__':
    unittest.main()