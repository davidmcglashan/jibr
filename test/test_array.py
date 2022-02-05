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
if __name__ == '__main__':
    unittest.main()