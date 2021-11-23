import unittest
from ...utilities.counter import Counter
from ...calculations.mode import get_modes

class TestModeCalculations( unittest.TestCase ):
    def test_no_values( self ):
        self.assertRaises( ValueError, lambda: get_modes() )

    def test_single_mode( self ):
        self.assertSequenceEqual( get_modes( *[ 1, 2, 3, 4, 5, 4 ] ), ( 4, ), seq_type = tuple )

    def test_multiple_mode( self ):
        self.assertSequenceEqual( get_modes( *[ 1, 2, 3, 4, 5, 3, 4 ] ), ( 3, 4 ), seq_type = tuple )

    def test_counter( self ):
        data = [ 1, 2, 3, 4, 5, 4 ]
        counter = Counter( *data )
        self.assertSequenceEqual( get_modes( counter ), get_modes( *data ), seq_type = tuple )

if __name__ == "__main__":
    unittest.main()
