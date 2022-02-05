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
    # Concatenate two arrays
    def test_array_plus( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array a status" )
        jbFunc.parse( "array b key" )

        self.assertEqual( len(jbArray.arrays['a']), 2 )
        self.assertEqual( len(jbArray.arrays['b']), 2 )

        jbFunc.parse( "array a + b" )
        self.assertEqual( len(jbArray.arrays['a']), 4 )
        self.assertEqual( len(jbArray.arrays['b']), 2 )

        jbFunc.parse( "array a + b" )
        self.assertEqual( len(jbArray.arrays['a']), 6 )
        self.assertEqual( len(jbArray.arrays['b']), 2 )

    # ======================================================================
    # You are not permitted to + an array to itself
    def test_array_plus_to_itself( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array a status" )
        self.assertEqual( len(jbArray.arrays['a']), 2 )

        jbFunc.parse( "array a + a")
        self.assertEqual( jbEcho.lastEcho, "Cannot add array 'a' to itself." )
        self.assertEqual( len(jbArray.arrays['a']), 2 )

    # ======================================================================
    # Subtract an array from another
    def test_array_minus( self ):
        jbEcho.testmode()
        jbFunc.parse( "array clear all" )
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "array a status" )
        jbFunc.parse( "array b status" )

        self.assertEqual( len(jbArray.arrays['a']), 2 )
        self.assertEqual( len(jbArray.arrays['b']), 2 )

        jbFunc.parse( "array a - b" )
        self.assertEqual( len(jbArray.arrays['a']), 0 )
        self.assertEqual( len(jbArray.arrays['b']), 2 )

# ======================================================================
if __name__ == '__main__':
    unittest.main()