import jibr.jbEcho as jbEcho
import jibr.jbHost as jbHost
import jibr.jbFunc as jbFunc

import unittest

class TestScript( unittest.TestCase ):

    # ======================================================================
    # Can we execute a simple script that does not exist?
    def test_non_existent_script( self ):
        jbEcho.testmode()
        jbFunc.parse( "script not-existing-file" )
        self.assertEqual( jbEcho.lastEcho, "File not found: not-existing-file.jibr" )

    # ======================================================================
    # Can we execute a simple script that does nothing?
    def test_non_existent_script( self ):
        jbEcho.testmode()
        jbFunc.parse( "script does-nothing-script" )
        self.assertEqual( jbEcho.lastEcho, "does-nothing-script.jibr: finished" )

    # ======================================================================
    # Can we execute a one parameter script without passing the parameter in?
    def test_without_providing_parameters( self ):
        jbEcho.testmode()
        jbFunc.parse( "script one-param" )
        self.assertEqual( jbEcho.lastEcho, "usage: script one-param number" )

    # ======================================================================
    # Can we execute a one parameter script without passing the parameter in?
    def test_providing_two_parameters( self ):
        jbEcho.testmode()
        jbFunc.parse( "script one-param one two" )
        self.assertEqual( jbEcho.lastEcho, "usage: script one-param number" )

    # ======================================================================
    # Can we execute a one parameter script where the script doesn't work?
    def test_params_but_not_used_in_script( self ):
        jbEcho.testmode()
        jbFunc.parse( "script duff-param one" )
        self.assertEqual( jbEcho.lastEcho, "Parameter {number} declared but not used in script" )

    # ======================================================================
    # Can we execute a one parameter script where the script doesn't work?
    def test_params( self ):
        jbEcho.testmode()
        jbFunc.parse( "script one-param 10" )
        self.assertEqual( jbEcho.lastEcho, "one-param.jibr: finished" )

# ======================================================================
if __name__ == '__main__':
    unittest.main()