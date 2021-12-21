import jibr.jbEcho as jbEcho
import jibr.jbFunc as jbFunc
import unittest

class TestEcho( unittest.TestCase ):

    # ======================================================================
    # Test that echo off properly sets its level
    def test_echo_off( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo off" )
        self.assertEqual( jbEcho.level, 1 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 1" )

    # ======================================================================
    # Test that echo on properly sets its level
    def test_echo_on( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo on" )
        self.assertEqual( jbEcho.level, 2 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 2" )

    # ======================================================================
    # Test that echo 0 properly sets its level
    def test_echo_0( self ):
        jbEcho.testmode()

        jbFunc.parse( "echo on" )   # so we can be sure about lastEcho
        self.assertEqual( jbEcho.lastEcho, "Echo level is 2" )

        # This should set the level to zero but not echo the change.
        jbFunc.parse( "echo 0" )
        self.assertEqual( jbEcho.level, 0 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 2" )

    # ======================================================================
    # Test that echo 1 properly sets its level
    def test_echo_1( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo 1" )
        self.assertEqual( jbEcho.level, 1 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 1" )

    # ======================================================================
    # Test that echo 2 properly sets its level
    def test_echo_2( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo 2" )
        self.assertEqual( jbEcho.level, 2 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 2" )

    # ======================================================================
    # Test that echo 3 properly sets its level
    def test_echo_3( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo 3" )
        self.assertEqual( jbEcho.level, 3 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 3" )

    # ======================================================================
    # Test that echo 99 is ignored
    def test_echo_99( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo on" )
        jbFunc.parse( "echo 99" )
        self.assertEqual( jbEcho.level, 2 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 2" )

    # ======================================================================
    # Test that echo david is ignored
    def test_echo_david( self ):
        jbEcho.testmode()
        jbFunc.parse( "echo on" )
        jbFunc.parse( "echo david" )
        self.assertEqual( jbEcho.level, 2 )
        self.assertEqual( jbEcho.lastEcho, "Echo level is 2" )

if __name__ == '__main__':
    unittest.main()