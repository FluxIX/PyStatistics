import unittest
from ..numeric_test_case import NumericTestCase
from ...statistics_set import StatisticsSet
from ...regression.linear_regression import LinearRegression

class TestLinearRegression( NumericTestCase ):
    def __init__( self, methodName = "runTest", **kwargs ):
        keyword_args = kwargs.copy()

        update_args = { "percent_tolerance": .01 }

        for key in update_args:
            if key not in keyword_args:
                keyword_args[ key ] = update_args[ key ]

        super( TestLinearRegression, self ).__init__( methodName, **keyword_args )

    def setUp( self ):
        # Data taken from: https://en.wikipedia.org/wiki/Simple_regression
        independent_data_set = [ 1.47, 1.5, 1.52, 1.55, 1.57, 1.6, 1.63, 1.65, 1.68, 1.7, 1.73, 1.75, 1.78, 1.8, 1.83 ]
        dependent_data_set = [ 52.21, 53.12, 54.48, 55.84, 57.2, 58.57, 59.93, 61.29, 63.11, 64.47, 66.28, 68.1, 69.92, 72.19, 74.46 ]

        self.positive_linear_data = independent_data_set, dependent_data_set

        negative_independent_set = independent_data_set[:] # Clones the list
        negative_independent_set.reverse()
        self.negative_linear_data = negative_independent_set, dependent_data_set

        self.independent_set = StatisticsSet( *independent_data_set, is_sample = False )
        self.dependent_set = StatisticsSet( *dependent_data_set, is_sample = False )

        self.regression = LinearRegression( self.independent_set, self.dependent_set )

    def test_slope( self ):
        self.assertFloatingPointPercentEqual( self.regression.slope, 61.272 )

    def test_intercept( self ):
        self.assertFloatingPointPercentEqual( self.regression.intercept, -39.062 )

    def test_correlation_coefficient( self ):
        self.assertFloatingPointPercentEqual( self.regression.correlation_coefficient, .9945 )

    def test_standard_error_squared( self ):
        self.assertFloatingPointPercentEqual( self.regression.standard_error_squared, .5762 )

    def test_slope_error_squared( self ):
        self.assertFloatingPointPercentEqual( self.regression.slope_error_squared, 3.1539 )

    def test_intercept_error_squared( self ):
        self.assertFloatingPointPercentEqual( self.regression.intercept_error_squared, 8.63185 )

    def test_immediate_computation( self ):
        regression = LinearRegression( self.independent_set, self.dependent_set, lazy_computation = False )
        self.assertTrue( regression._covariance is not None )

    def test_lazy_computation( self ):
        regression = LinearRegression( self.independent_set, self.dependent_set, lazy_computation = True )
        self.assertTrue( regression._covariance is None )

if __name__ == "__main__":
    unittest.main()
