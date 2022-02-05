import jibr.jbEcho as jbEcho
import jibr.jbHost as jbHost
import jibr.jbFunc as jbFunc

import unittest

class TestToken( unittest.TestCase ):

    # ======================================================================
    # Test that the PAT can be set to an arbitrary string
    def test_token_can_be_set( self ):
        jbEcho.testmode()
        jbFunc.parse( "token david" )
        self.assertEqual( jbHost._accessToken, "david" )
        self.assertEqual( jbEcho.lastEcho, "Access token is david..." )

    # ======================================================================
    # Test that the PAT can be a long arbitrary string which isn't echoed in full back to the user
    def test_long_tokens_arent_echoed( self ):
        jbEcho.testmode()
        jbFunc.parse( "token daviddaviddaviddavid" )
        self.assertEqual( jbHost._accessToken, "daviddaviddaviddavid" )
        self.assertEqual( jbEcho.lastEcho, "Access token is daviddavidda..." )

    # ======================================================================
    # Test that the PAT gets included in a dict used to communicate with remore servers
    def test_tokens_are_added_to_auth_headers( self ):
        jbEcho.testmode()
        jbFunc.parse( "token daviddaviddaviddavid" )

        header = dict()
        jbHost.addAuthHeader( header )
        self.assertTrue( 'Authorization' in header )
        self.assertEqual( header['Authorization'], 'Bearer daviddaviddaviddavid' )

# ======================================================================
if __name__ == '__main__':
    unittest.main()