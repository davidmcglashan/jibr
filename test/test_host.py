import jibr.jbEcho as jbEcho
import jibr.jbHost as jbHost
import jibr.jbFunc as jbFunc

import unittest

class TestHost( unittest.TestCase ):

    # ======================================================================
    # Test that the hostname can be set to localhost
    def test_host_can_be_set( self ):
        jbEcho.testmode()
        jbFunc.parse( "hostname localhost" )
        self.assertEqual( jbHost.hostname, "localhost" )
        self.assertEqual( jbEcho.lastEcho, "Host name is localhost" )

    # ======================================================================
    # Test that the port can be set to 8080
    def test_port_can_be_set( self ):
        jbEcho.testmode()
        jbFunc.parse( "port 8080" )
        self.assertEqual( jbHost.port, "8080" )
        self.assertEqual( jbEcho.lastEcho, "Port number is 8080" )

    # ======================================================================
    # Test that the host and port get combined properly
    def test_host_and_port_can_be_set( self ):
        jbEcho.testmode()
        jbFunc.parse( "hostname example.com" )
        jbFunc.parse( "port 8443" )
        self.assertEqual( jbHost.host(), "example.com:8443" )

        jbFunc.parse( "host" )
        self.assertEqual( jbEcho.lastEcho, "example.com:8443" )

# ======================================================================
if __name__ == '__main__':
    unittest.main()