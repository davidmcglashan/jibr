import jibr.jbEcho as jbEcho
import jibr.jbFunc as jbFunc
import unittest

class TestHelp( unittest.TestCase ):

    # ======================================================================
    # Help by itself lists all the commands
    def test_help( self ):
        jbEcho.testmode()
        jbFunc.parse( "help" )
        self.assertTrue( jbEcho.lastEcho.startswith( "   > " ) )

    # ======================================================================
    # Test that the help help command returns help about help
    def test_help_help( self ):
        jbEcho.testmode()
        jbFunc.parse( "help help" )
        self.assertEqual( jbEcho.lastEcho, "  Provides help about [command]." )

if __name__ == '__main__':
    unittest.main()