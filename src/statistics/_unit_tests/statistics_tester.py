__version__ = r"1.0"

from ..regression import LinearRegression
from ..statistics_set import StatisticsSet

class StatisticsTester( object ):
    def __init__( self ):
        # Data taken from: https://en.wikipedia.org/wiki/Simple_regression
        independent_set = [ 1.47, 1.5, 1.52, 1.55, 1.57, 1.6, 1.63, 1.65, 1.68, 1.7, 1.73, 1.75, 1.78, 1.8, 1.83 ]
        dependent_set = [ 52.21, 53.12, 54.48, 55.84, 57.2, 58.57, 59.93, 61.29, 63.11, 64.47, 66.28, 68.1, 69.92, 72.19, 74.46 ]

        self.positive_linear_data = independent_set, dependent_set

        negative_independent_set = independent_set[:] # Clones the list
        negative_independent_set.reverse()
        self.negative_linear_data = negative_independent_set, dependent_set

    def compute_difference( self, actual_value, expected_value ):
        import math
        difference = math.fabs( actual_value - expected_value )
        mean_value = float( actual_value + expected_value ) / 2
        percent_difference = float( difference ) / mean_value * 100
        percent_error = float( difference ) / expected_value * 100

        return difference, percent_difference, percent_error

    def print_difference( self, actual_value, expected_value, label = None ):
        difference = self.compute_difference( actual_value, expected_value )

        if label is not None and len( label ) > 0:
            print( "{}:".format( label ) )

        tab_Spacing = " " * 3
        message_data = [ ( "Expected Value", expected_value ), ( "Actual Value", actual_value ), ] + zip( [ "Value Difference", "Percent Difference", "Percent Error" ], difference )
        for message, data in message_data:
            print( "{}{}: {}".format( tab_Spacing, message, data ) )

    def run_linear_regression_tests( self ):
        independent_set = StatisticsSet( *self.positive_linear_data[ 0 ], lazy_computation = False, is_sample = False )
        dependent_set = StatisticsSet( *self.positive_linear_data[ 1 ], is_sample = False )

        print( "Linear Regression Tests:" )

        print( "Positive Correlation Test:" )
        print( "Independent Data (Height (m)): {}".format( self.positive_linear_data[ 0 ] ) )
        print( "Dependent Data (Mass (kg)): {}".format( self.positive_linear_data[ 1 ] ) )

        regression_data = LinearRegression( independent_set, dependent_set, lazy_computation = False )
        self.print_difference( regression_data.slope, 61.272, "Slope" )
        self.print_difference( regression_data.intercept, -39.062, "Intercept" )
        self.print_difference( regression_data.correlation_coefficient, .9945, "Correlation Coefficient" )
        self.print_difference( regression_data.standard_error_squared, .5762, "Standard Error Squared" )
        self.print_difference( regression_data.slope_error_squared, 3.1539, "Slope Error Squared" )
        self.print_difference( regression_data.intercept_error_squared, 8.63185, "Intercept Error Squared" )

        del independent_set
        del dependent_set
        del regression_data

    def run( self ):
        self.run_linear_regression_tests()
        return 0
