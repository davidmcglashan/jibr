import jibr.jbWeb as jbWeb
import jibr.jbFunc as jbFunc
import jibr.jbHost as jbHost
import unittest

class TestJira( unittest.TestCase ):

    # ======================================================================
    # Test that the jira command can open a single issue.
    def test_a_single_jira_issue( self ):
        jbWeb.testmode()
        jbFunc.parse( "hostname localhost" )
        jbFunc.parse( "port 80" )
        self.assertEqual( jbHost.host(), "localhost:80" )

        jbFunc.parse( "jira abc-1" )
        self.assertEqual( jbWeb.lastUrl, "https://localhost:80/browse/abc-1" )

if __name__ == '__main__':
    unittest.main()