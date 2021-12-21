import jibr.jbHost as jbHost
import jibr.jbFunc as jbFunc

import unittest

class TestHost( unittest.TestCase ):

    # Test that the hostname can be set to localhost
    def test_host_can_be_set( self ):
        jbFunc.parse( "hostname localhost" )
        self.assertEqual( jbHost.hostname, "localhost" )

    # Test that the port can be set to 8080
    def test_port_can_be_set( self ):
        jbFunc.parse( "port 8080" )
        self.assertEqual( jbHost.port, "8080" )

    # Test that the host and port get combined properly
    def test_host_and_port_can_be_set( self ):
        jbFunc.parse( "hostname example.com" )
        jbFunc.parse( "port 8443" )
        self.assertEqual( jbHost.host(), "example.com:8443" )

if __name__ == '__main__':
    unittest.main()