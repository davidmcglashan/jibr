import jibr.jbEcho as jbEcho
import jibr.jbFunc as jbFunc
import jibr.jbArray as jbArray

import unittest

class TestArray( unittest.TestCase ):

    # ======================================================================
    # Simple array creation
    def test_array_from_payload( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array testkeys key" )

        self.assertEqual( len(jbArray.arrays), 1 )
        self.assertEqual( len(jbArray.arrays['testkeys']), 2 )

    # ======================================================================
    # Clear an array
    def test_array_clear( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )

        jbFunc.parse( "array one key" )
        jbFunc.parse( "array two key" )
        self.assertEqual( len(jbArray.arrays), 2 )
        self.assertTrue( 'one' in jbArray.arrays )

        jbFunc.parse( "array clear one" )
        self.assertEqual( len(jbArray.arrays), 1 )
        self.assertTrue( 'one' not in jbArray.arrays )

    # ======================================================================
    # Clear all arrays
    def test_array_clear_all( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )

        jbFunc.parse( "array one key" )
        jbFunc.parse( "array two key" )
        self.assertEqual( len(jbArray.arrays), 2 )
        self.assertTrue( 'one' in jbArray.arrays )
        self.assertTrue( 'two' in jbArray.arrays )

        jbFunc.parse( "array clear all" )
        self.assertEqual( len(jbArray.arrays), 0 )

    # ======================================================================
    # Display an array
    def test_array_display( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array one key" )

        jbFunc.parse( "array one" )
        self.assertEqual( jbEcho.lastEcho, "one: ['ABC-25', 'ABC-24']" )

    # ======================================================================
    # Display all arrays
    def test_array_display_all( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array two key" )
        jbFunc.parse( "array one key" )
        jbFunc.parse( "array zed key" )
        jbFunc.parse( "array abc key" )
        
        # A soft test, but if we get this far we know it's not broken!
        jbFunc.parse( "array" )
        self.assertTrue( jbEcho.lastEcho.endswith( ": ['ABC-25', 'ABC-24']" ) )

    # ======================================================================
    # Remove the dupes
    def test_array_unique( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array ss status" )

        self.assertEqual( len(jbArray.arrays['ss']), 2 )
        jbFunc.parse( "array unique ss" )
        self.assertEqual( len(jbArray.arrays['ss']), 1 )

# ======================================================================
if __name__ == '__main__':
    unittest.main()