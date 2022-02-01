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

    # ========================================================================================
    def test_record_clear_also_clears_fields( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record clear" )
        jbFunc.parse( "record ABC-25" )
        jbFunc.parse( "field title setting title in a test" )
        self.assertEqual( jbField.fields['title'], "setting title in a test" )
        jbFunc.parse( "field assignee john.smith" )
        self.assertEqual( jbField.fields['assignee'], "john.smith" )
        self.assertEqual( len(jbField.fields), 2 )

        jbFunc.parse( "record clear" )
        self.assertEqual( len(jbField.fields), 0 )

    # ========================================================================================
    def test_minus_removes_a_field( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record clear" )
        jbFunc.parse( "record ABC-25" )
        jbFunc.parse( "field abc the first field" )
        jbFunc.parse( "field def the second field" )
        jbFunc.parse( "field ghi the third field" )
        self.assertEqual( len(jbField.fields), 3 )

        jbFunc.parse( "field - def" )
        self.assertEqual( len(jbField.fields), 2 )
        self.assertEqual( jbEcho.lastEcho, "def removed" )

    # ========================================================================================
    def test_minus_minus_removes_all_fields( self ):
        jbHttpConn.testmode()
        jbFunc.parse( "record clear" )
        jbFunc.parse( "record ABC-25" )
        jbFunc.parse( "field abc the first field" )
        jbFunc.parse( "field def the second field" )
        jbFunc.parse( "field ghi the third field" )
        self.assertEqual( len(jbField.fields), 3 )

        jbFunc.parse( "field --" )
        self.assertEqual( len(jbField.fields), 0 )
        self.assertEqual( jbEcho.lastEcho, "3 field(s) removed" )

if __name__ == '__main__':
    unittest.main()