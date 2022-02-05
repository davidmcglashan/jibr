import jibr.jbEcho as jbEcho
import jibr.jbFunc as jbFunc
import jibr.jbBucket as jbBucket

import unittest

class TestBucket( unittest.TestCase ):

    # ======================================================================
    # Simple field bucketing
    def test_bucket_by_status( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by status" )

        self.assertEqual( len(jbBucket.buckets), 1 )
        self.assertEqual( jbBucket.buckets['0']['name'], 'Ready for Development' )

    # ======================================================================
    # Simple field bucketing
    def test_bucket_by_creator( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by creator" )

        self.assertEqual( len(jbBucket.buckets), 2 )
        self.assertEqual( jbBucket.buckets['0']['name'], 'John Doe' )
        self.assertEqual( jbBucket.buckets['1']['name'], 'Kevin Smith' )

    # ======================================================================
    # Does bucket clear remove the numbered buckets
    def test_bucket_clear( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        self.assertEqual( len(jbBucket.buckets), 0 )

        jbFunc.parse( "bucket by status" )
        self.assertEqual( len(jbBucket.buckets), 1 )

        jbFunc.parse( "bucket clear" )
        self.assertEqual( len(jbBucket.buckets), 0 )

    # ======================================================================
    # Does bucket clear remove the numbered buckets
    def test_bucket_cant_clear_numbered( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by creator" )
        self.assertEqual( len(jbBucket.buckets), 2 )

        jbFunc.parse( "bucket clear 0" )
        self.assertEqual( len(jbBucket.buckets), 2 )
        self.assertEqual( jbEcho.lastEcho, "Cannot clear numbered buckets" )

    # ======================================================================
    # Copying a numbered bucket
    def test_bucket_copy( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by creator" )
        self.assertEqual( len(jbBucket.buckets), 2 )
        self.assertTrue( 'copy_of_0' not in jbBucket.buckets )

        jbFunc.parse( "bucket copy 0 copy_of_0" )
        self.assertEqual( len(jbBucket.buckets), 3 )
        self.assertEqual( jbBucket.buckets['copy_of_0']['name'], 'John Doe' )
        self.assertEqual( len(jbBucket.buckets['copy_of_0']['keys']), 1 )

    # ======================================================================
    # Copying a numbered bucket
    def test_bucket_clear_named( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by creator" )
        jbFunc.parse( "bucket copy 0 copy_of_0" )
        self.assertEqual( len(jbBucket.buckets), 3 )
        self.assertTrue( 'copy_of_0' in jbBucket.buckets )

        jbFunc.parse( "bucket clear copy_of_0" )
        self.assertEqual( len(jbBucket.buckets), 2 )
        self.assertTrue( 'copy_of_0' not in jbBucket.buckets )

    # ======================================================================
    # Bucket arithmetic plus
    def test_bucket_plus_bucket( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by creator" )
        self.assertEqual( len(jbBucket.buckets), 2 )
        self.assertEqual( len(jbBucket.buckets['0']['keys']), 1 )
        self.assertEqual( jbBucket.buckets['0']['keys'][0], 'ABC-24' )

        jbFunc.parse( "bucket 0 + 1" )
        self.assertEqual( len(jbBucket.buckets['0']['keys']), 2 )
        self.assertEqual( jbBucket.buckets['0']['keys'][0], 'ABC-24' )
        self.assertEqual( jbBucket.buckets['0']['keys'][1], 'ABC-25' )

    # ======================================================================
    # Clear all should remove all the buckets, numbered and named!
    def test_bucket_clear_all( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket by creator" )
        jbFunc.parse( "bucket copy 0 copy" )
        self.assertEqual( len(jbBucket.buckets), 3 )

        jbFunc.parse( "bucket clear all" )
        self.assertEqual( len(jbBucket.buckets), 0 )

    # ======================================================================
    # Bucket payload puts all the keys in 0
    def test_bucket_payload( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket payload" )

        self.assertEqual( len(jbBucket.buckets), 1 )
        self.assertEqual( jbBucket.buckets['0']['name'], 'Payload keys' )
        self.assertEqual( len(jbBucket.buckets['0']['keys']), 2 )

    # ======================================================================
    # Bucket payload puts all the keys in 0
    def test_bucket_payload_into_id( self ):
        jbEcho.testmode()
        jbFunc.parse( "payload load test-payload" )
        jbFunc.parse( "bucket clear all" )
        jbFunc.parse( "bucket payload test" )

        self.assertEqual( len(jbBucket.buckets), 1 )
        self.assertEqual( jbBucket.buckets['test']['name'], 'Payload keys' )
        self.assertEqual( len(jbBucket.buckets['test']['keys']), 2 )

# ======================================================================
if __name__ == '__main__':
    unittest.main()