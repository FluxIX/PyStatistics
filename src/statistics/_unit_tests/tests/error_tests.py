import unittest
from ...calculations.error import compute_relative_difference, compute_relative_error

class TestErrorCalculations( unittest.TestCase ):
    def test_relative_difference( self ):
        self.assertAlmostEqual( compute_relative_difference( 4, 6 ), .4, delta = .001 )
        self.assertAlmostEqual( compute_relative_difference( 6, 4, positive_difference = False ), -.4, delta = .001 )
        self.assertAlmostEqual( compute_relative_difference( 6, 4 ), .4, delta = .001 )
        self.assertAlmostEqual( compute_relative_difference( 4, 6, scale = 10 ), 4, delta = .001 )
        self.assertAlmostEqual( compute_relative_difference( 6, 4, positive_difference = False, scale = 10 ), -4, delta = .001 )
        self.assertAlmostEqual( compute_relative_difference( 6, 4, scale = 10 ), 4, delta = .001 )

    def test_relative_error( self ):
        self.assertAlmostEqual( compute_relative_error( 4, 5 ), .2, delta = .001 )
        self.assertAlmostEqual( compute_relative_error( 6, 5 ), .2, delta = .001 )
        self.assertAlmostEqual( compute_relative_error( 6, 5, positive_error = False ), -.2, delta = .001 )
        self.assertAlmostEqual( compute_relative_error( 4, 5, scale = 10 ), 2, delta = .001 )
        self.assertAlmostEqual( compute_relative_error( 6, 5, scale = 10 ), 2, delta = .001 )
        self.assertAlmostEqual( compute_relative_error( 6, 5, positive_error = False, scale = 10 ), -2, delta = .001 )

if __name__ == "__main__":
    unittest.main()
