__version__ = r"1.0"

from . import utilities

class StatisticsSet( object ):
    def __init__( self, data, lazy_computation = True ):
        self._copy_data( data )

        self.clear_results()
        if not lazy_computation:
            self.compute_results()

    def clear_results( self ):
        self.__minimum_value = None
        self.__maximum_value = None
        self.__least_frequent_values = None
        self.__most_frequent_values = None
        self.__unique_values = None
        self.__range = None
        self.__frequency_distribution = None
        self.__sum = None
        self.__sum_squared = None
        self.__sum_of_squares = None
        self.__mean = None
        self.__mode = None
        self.__mode_count = None
        self.__median = None
        self.__median_count = None
        self.__variance = None
        self.__standard_deviation = None
        self.__skew = None
        self.__kurtosis_excess = None

    def compute_results( self ):
        self.minimum_value
        self.maximum_value
        self.least_frequent_values
        self.most_frequent_values
        self.range
        self.frequency_distribution
        self.unique_values
        self.sum
        self.sum_squared
        self.sum_of_squares
        self.mean
        self.mode
        self.mode_count
        self.median
        self.median_count
        self.variance
        self.standard_deviation
        self.skew
        self.kurtosis_excess

    def _copy_data( self, input_data ):
        self.__data = input_data[:]
        self.__sorted_data = input_data[:]
        self.__sorted_data.sort( reverse = False )

    def _compute_statistics_item_moment( self, item, degree ):
        return utilities.integer_power( item - self.mean, degree )

    def _compute_moment( self, degree ):
        result = 0

        for item in self.data:
            result += self._compute_statistics_item_moment( item, degree )

        return result

    @property
    def data( self ):
        return self.__data

    @property
    def sorted_data( self ):
        return self.__sorted_data

    @property
    def size( self ):
        return len( self.data )

    @property
    def minimum_value( self ):
        if self.__minimum_value is None:
            self.__minimum_value = self.sorted_data[ 0 ]

        return self.__minimum_value

    @property
    def maximum_value( self ):
        if self.__maximum_value is None:
            self.__maximum_value = self.sorted_data[ -1 ]

        return self.__maximum_value

    def _get_frequencies( self, frequency_selection_predicate ):
        selected_frequency = 0
        result = []

        for key in self.frequency_distribution:
            item_frequency = self.frequency_distribution[ key ]
            if selected_frequency == 0 or frequency_selection_predicate( item_frequency, selected_frequency ):
                selected_frequency = item_frequency
                result = [ key ]
            elif item_frequency == selected_frequency:
                result.append( key )

        return result

    @property
    def least_frequent_values( self ):
        if self.__least_frequent_values is None:
            self.__least_frequent_values = self._get_frequencies( lambda x, y : x < y )

        return self.__least_frequent_values

    @property
    def most_frequent_values( self ):
        if self.__most_frequent_values is None:
            self.__most_frequent_values = self._get_frequencies( lambda x, y : x > y )

        return self.__least_frequent_values

    @property
    def unique_values( self ):
        if self.__unique_values is None:
            self.__unique_values = []
            for key in self.frequency_distribution:
                if key not in self.__unique_values:
                    self.__unique_values.append( key )

        return self.__unique_values

    @property
    def unique_value_count( self ):
        return len( self.unique_values )

    @property
    def range( self ):
        if self.__range is None:
            self.__range = self.__sorted_data[ -1 ] - self.__sorted_data[ 0 ]

        return self.__range

    @property
    def frequency_distribution( self ):
        if self.__frequency_distribution is None:
            frequency_distribution = {}
            for item in self.data:
                if item not in frequency_distribution:
                    frequency_distribution[ item ] = 0
                frequency_distribution[ item ] += 1

            self.__frequency_distribution = frequency_distribution

        return self.__frequency_distribution

    @property
    def sum( self ):
        if self.__sum is None:
            result = 0

            for item in self.data:
                result += item

            self.__sum = result

        return self.__sum

    @property
    def sum_squared( self ):
        if self.__sum_squared is None:
            self.__sum_squared = utilities.integer_power( self.sum, 2 )

        return self.__sum_squared

    @property
    def sum_of_squares( self ):
        if self.__sum_of_squares is None:
            result = 0

            for item in self.data:
                result += utilities.integer_power( item, 2 )

            self.__sum_of_squares = result

        return self.__sum_of_squares

    @property
    def mean( self ):
        if self.__mean is None:
            self.__mean = float( self.sum ) / self.size

        return self.__mean

    @property
    def mode( self ):
        if self.__mode is None:
            for key in self.frequency_distribution:
                if self.__mode is None or self.frequency_distribution[ self.__mode ] < self.frequency_distribution[ key ]:
                    self.__mode = key

        return self.__mode

    @property
    def mode_count( self ):
        if self.__mode_count is None:
            self.__mode_count = self.frequency_distribution[ self.mode ]

        return self.__mode_count

    @property
    def median( self ):
        if self.__median is None:
            self.__median = self.__sorted_data[ self.size / 2 ]

        return self.__median

    @property
    def median_count( self ):
        if self.__median_count is None:
            self.__median_count = self.frequency_distribution[ self.median ]

        return self.__median_count

    @property
    def variance( self ):
        if self.__variance is None:
            self.__variance = float( self._compute_moment( 2 ) ) / self.size

        return self.__variance

    @property
    def standard_deviation( self ):
        if self.__standard_deviation is None:
            import math
            self.__standard_deviation = math.sqrt( self.variance )

        return self.__standard_deviation

    @property
    def skew( self ):
        if self.__skew is None:
            self.__skew = float( self._compute_moment( 3 ) ) / ( self.variance * self.standard_deviation ) / self.size

        return self.__skew

    @property
    def kurtosis_excess( self ):
        if self.__kurtosis_excess is None:
            self.__kurtosis_excess = float( self._compute_moment( 4 ) ) / utilities.integer_power( self.variance, 2 ) / self.size - 3

        return self.__kurtosis_excess
