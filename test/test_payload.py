import jibr.jbWeb as jbWeb
import jibr.jbFunc as jbFunc
import jibr.jbPayload as jbPayload
import unittest

class TestPayload( unittest.TestCase ):

    # ========================================================================================
    # ... because we can't make an HTTP connection in a unit test (w/o a mock environment)
    def test_loading_a_payload( self ):
        jbWeb.testmode()
        jbFunc.parse( "payload load test-payload" )

        self.assertTrue( jbPayload.payload != None )
        self.assertEqual( len( jbPayload.payload['issues'] ), 2 )

if __name__ == '__main__':
    unittest.main()