__version__ = r"1.0"

from ..utilities.dict import update_if_not_set
from ..utilities.sorting import get_values
from .median import get_median_positions
from .partitioning import PartitionMedianBehavior, get_split_plan

class MedianValueInformation( object ):
    """
    Stores information regarding a median value.
    """

    def __init__( self, value, value_position, **kwargs ):
        self._value = value
        self._value_position = value_position

    @property
    def value( self ):
        """
        Gets the value of the median.
        """

        return self._value

    @property
    def value_position( self ):
        """
        Gets the zero-based position of the median value in the sorted input data.

        If the median was not in the sorted input data, the position is `None`.
        """

        return self._value_position

    @property
    def value_in_dataset( self ):
        """
        True if the median value is in the sorted input data, False otherwise.
        """

        return self.value_position is not None

class DataSetQuartileInformation( object ):
    """
    Stores information regarding the quartiles of the input data set.
    """

    def __init__( self, *values, **kwargs ):
        self._compute_data( *values, **kwargs )

    @property
    def sorted_data( self ):
        """
        Gets the sorted input data.
        """

        return self._sorted_data

    @property
    def q1_values( self ):
        """
        Gets the first quartile values of the input values.
        """

        return self._q1_values

    @property
    def q2_values( self ):
        """
        Gets the second quartile values of the input values.
        """

        return self._q2_values

    @property
    def q3_values( self ):
        """
        Gets the third quartile values of the input values.
        """

        return self._q3_values

    @property
    def q4_values( self ):
        """
        Gets the fourth quartile values of the input values.
        """

        return self._q4_values

    @property
    def q1_q2_fence( self ):
        """
        Gets the fence between the first and second quartiles.
        """

        return self._q1_q2_fence

    @property
    def q2_q3_fence( self ):
        """
        Gets the fence between the second and third quartiles.
        """

        return self._q2_q3_fence

    @property
    def q3_q4_fence( self ):
        """
        Gets the fence between the third and fourth quartiles.
        """

        return self._q3_q4_fence

    @property
    def interquartile_range( self ):
        """
        Gets the interquartile range for the input values.
        """

        return self._interquartile_range

    @property
    def lower_extreme_outlier_fence( self ):
        """
        Gets the lower extreme outlier fence.
        """

        return self._lower_extreme_outlier_fence

    @property
    def lower_mild_outlier_fence( self ):
        """
        Gets the lower mild outlier fence.
        """

        return self._lower_mild_outlier_fence

    @property
    def upper_mild_outlier_fence( self ):
        """
        Gets the upper mild outlier fence.
        """

        return self._upper_mild_outlier_fence

    @property
    def upper_extreme_outlier_fence( self ):
        """
        Gets the upper extreme outlier fence.
        """

        return self._upper_extreme_outlier_fence

    @property
    def lower_extreme_outliers( self ):
        """
        Gets all of the extreme outliers in the first and second quartiles.
        """

        return self._lower_extreme_outliers

    @property
    def lower_mild_outliers( self ):
        """
        Gets all of the mild outliers in the first and second quartiles.
        """

        return self._lower_mild_outliers

    @property
    def upper_mild_outliers( self ):
        """
        Gets all of the mild outliers in the third and fourth quartiles.
        """

        return self._upper_mild_outliers

    @property
    def upper_extreme_outliers( self ):
        """
        Gets all of the extreme outliers in the third and fourth quartiles.
        """

        return self._upper_extreme_outliers

    @property
    def lower_outliers( self ):
        """
        Gets all of the outliers in the first and second quartiles.
        """

        return self.lower_extreme_outliers + self.lower_mild_outliers

    @property
    def upper_outliers( self ):
        """
        Gets all of the outliers in the third and fourth quartiles.
        """

        return self.upper_mild_outliers + self.upper_extreme_outliers

    @property
    def all_outliers( self ):
        """
        Gets all of the outliers in the input values.
        """

        return self.lower_outliers + self.upper_outliers

    @property
    def five_number_summary( self ):
        """
        Gets the five-number summary (quartiles zero through four) for the input values.
        """

        return self._five_number_summary

    @property
    def q1_non_outlier_values( self ):
        """
        Gets the values in the first quartile which are not outliers.
        """

        return self._q1_non_outlier_values

    @property
    def q4_non_outlier_values( self ):
        """
        Gets the values in the fourth quartile which are not outliers.
        """

        return self._q4_non_outlier_values

    def _compute_data( self, *values, **kwargs ):
        keyword_args = update_if_not_set( kwargs, ( "sort", True ), in_place = False )
        data_values = get_values( *values, **keyword_args )

        data_length = len( data_values )

        # Quartile and quartile fence calculations.
        q2_q3_fence = self._get_median_fence_value( *data_values, **keyword_args )

        q1_q2_values, q3_q4_values = [ self._get_values( data_values, plan[ 0 ], plan[ 1 ] ) for plan in get_split_plan( data_length, **keyword_args ) ]

        q1_q2_fence = self._get_median_fence_value( *q1_q2_values, **keyword_args )
        q3_q4_fence = self._get_median_fence_value( *q3_q4_values, **keyword_args )

        q1_values, q2_values = [ self._get_values( q1_q2_values, plan[ 0 ], plan[ 1 ] ) for plan in get_split_plan( len( q1_q2_values ), **keyword_args ) ]
        q3_values, q4_values = [ self._get_values( q3_q4_values, plan[ 0 ], plan[ 1 ] ) for plan in get_split_plan( len( q3_q4_values ), **keyword_args ) ]

        # Outlier fence calculations.
        mild_fence_multiplier = self._get_kwargs_value( kwargs, "mild_fence_multiplier", 1.5, float )
        extreme_fence_multiplier = self._get_kwargs_value( kwargs, "extreme_fence_multiplier", 3, float )
        lower_mild_fence_muliplier = self._get_kwargs_value( kwargs, "lower_mild_fence_muliplier", mild_fence_multiplier, float )
        upper_mild_fence_muliplier = self._get_kwargs_value( kwargs, "upper_mild_fence_muliplier", mild_fence_multiplier, float )
        lower_extreme_fence_multiplier = self._get_kwargs_value( kwargs, "lower_mild_fence_muliplier", extreme_fence_multiplier, float )
        upper_extreme_fence_multiplier = self._get_kwargs_value( kwargs, "upper_extreme_fence_multiplier", extreme_fence_multiplier, float )

        iqr = q3_q4_fence.value - q1_q2_fence.value

        lower_extreme_fence = q1_q2_fence.value - iqr * lower_extreme_fence_multiplier
        lower_mild_fence = q1_q2_fence.value - iqr * lower_mild_fence_muliplier
        upper_mild_fence = q3_q4_fence.value + iqr * upper_mild_fence_muliplier
        upper_extreme_fence = q3_q4_fence.value + iqr * upper_extreme_fence_multiplier

        # Outlier calculations.
        lower_extreme_outliers = filter( lambda x: x <= lower_extreme_fence, q1_values )
        lower_mild_outliers = filter( lambda x: x <= lower_mild_fence and x > lower_extreme_fence, q1_values )
        upper_mild_outliers = filter( lambda x: x >= upper_mild_fence and x < upper_extreme_fence, q4_values )
        upper_extreme_outliers = filter( lambda x: x >= upper_extreme_fence, q4_values )
        q1_non_outlier_values = filter( lambda x: x > lower_mild_fence, q1_values )
        q4_non_outlier_values = filter( lambda x: x < upper_mild_fence, q4_values )

        # Value setting.
        self._sorted_data = tuple( data_values )
        self._q1_values = tuple( q1_values )
        self._q2_values = tuple( q2_values )
        self._q3_values = tuple( q3_values )
        self._q4_values = tuple( q4_values )
        self._q1_q2_fence = q1_q2_fence
        self._q2_q3_fence = q2_q3_fence
        self._q3_q4_fence = q3_q4_fence
        self._interquartile_range = iqr
        self._lower_extreme_outlier_fence = lower_extreme_fence
        self._lower_mild_outlier_fence = lower_mild_fence
        self._upper_mild_outlier_fence = upper_mild_fence
        self._upper_extreme_outlier_fence = upper_extreme_fence
        self._five_number_summary = q1_values[ 0 ], q1_q2_fence.value, q2_q3_fence.value, q3_q4_fence.value, q4_values[ -1 ]
        self._lower_extreme_outliers = tuple( lower_extreme_outliers )
        self._lower_mild_outliers = tuple( lower_mild_outliers )
        self._upper_mild_outliers = tuple( upper_mild_outliers )
        self._upper_extreme_outliers = tuple( upper_extreme_outliers )
        self._q1_non_outlier_values = tuple( q1_non_outlier_values )
        self._q4_non_outlier_values = tuple( q4_non_outlier_values )

    def _get_median_fence_value( self, *values, **kwargs ):
        positions = get_median_positions( len( values ), **kwargs )
        if len( positions ) == 1:
            position = positions[ 0 ]
            result = MedianValueInformation( values[ position ], position )
        else:
            lower_median = values[ positions[ 0 ] ]
            upper_median = values[ positions[ 1 ] ]

            result = MedianValueInformation( float( lower_median + upper_median ) / 2, None )

        return result

    def _get_values( self, values, starting_index, length ):
        ending_index = starting_index + length
        return values[ starting_index: ending_index ]

    def _get_kwargs_value( self, kwargs, key, default_value = None, value_conversion = None ):
        value = kwargs.get( key, None )
        if value is None:
            value = default_value
        elif value_conversion is not None:
            value = value_conversion( value )

        return value
