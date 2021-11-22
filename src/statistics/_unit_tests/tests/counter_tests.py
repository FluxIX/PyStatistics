import unittest
from ...utilities.counter import Counter, FrozenCounter

class TestCounter( unittest.TestCase ):
    pass

class TestFrozenCounter( unittest.TestCase ):
    def setUp( self ):
        self.counter_data = [ 1, 2, 3, 4, 4, 5 ]
        self.counter = Counter( *self.counter_data )

    def test_as_tuple( self ):
        self.assertSequenceEqual( self.counter.to_tuple(), tuple( self.counter_data ), seq_type = tuple )

if __name__ == "__main__":
    unittest.main()
