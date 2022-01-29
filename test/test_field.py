import jibr.jbHttpConn as jbHttpConn
import jibr.jbField as jbField
import jibr.jbFunc as jbFunc
import jibr.jbEcho as jbEcho

import unittest

class TestField( unittest.TestCase ):

    # ========================================================================================
    def test_no_record_means_no_fields( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record clear" )
        jbFunc.parse( "field" )
        self.assertEqual( jbEcho.lastEcho, "No record. Point to one before setting fields." )

    # ========================================================================================
    def test_a_record_allows_fields_to_be_set( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record clear" )
        jbFunc.parse( "record ABC-25" )
        jbFunc.parse( "field title setting title in a test" )
        self.assertEqual( jbField.fields['title'], "setting title in a test" )

        jbFunc.parse( "field" )
        self.assertEqual( jbEcho.lastEcho, "title: setting title in a test" )

if __name__ == '__main__':
    unittest.main()