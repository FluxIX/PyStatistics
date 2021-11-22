import unittest
from ..numeric_test_case import NumericTestCase
from ...statistics_set import StatisticsSet

class TestStatisticsSet( NumericTestCase ):
    def __init__( self, methodName = "runTest", **kwargs ):
        keyword_args = kwargs.copy()

        update_args = { "percent_tolerance": .01 }

        for key in update_args:
            if key not in keyword_args:
                keyword_args[ key ] = update_args[ key ]

        super( TestStatisticsSet, self ).__init__( methodName, **keyword_args )

    def setUp( self ):
        self.data = 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144
        self.statistics_set = StatisticsSet( *self.data, lazy_computation = True )

    def test_immediate_computation( self ):
        statistics_set = StatisticsSet( *self.data, lazy_computation = False )
        self.assertTrue( statistics_set._least_frequent_values.has_value )

    def test_lazy_computation( self ):
        statistics_set = StatisticsSet( *self.data, lazy_computation = True )
        self.assertFalse( statistics_set._least_frequent_values.has_value )

    def test_data( self ):
        self.assertItemsEqual( self.data, self.statistics_set.data )

    def test_min_value( self ):
        self.assertEqual( self.statistics_set.minimum_value, 1 )

    def test_max_value( self ):
        self.assertEqual( self.statistics_set.maximum_value, 144 )

if __name__ == "__main__":
    unittest.main()
