__version__ = r"2.0"

from .utilities.cached_value import CachedValue
from .utilities.hashing import get_hash
from .utilities.sorting import sort_values
from .calculations import mean, mode, moments, quartiles, scores
from .calculations.frequency import get_frequency_distribution

class StatisticsSet( object ):
    """
    Represents an immutable data set and computes descriptive statistics on the data set. 
    """

    # TODO: add subset/slice functionality, should return a new StatisticsSet

    def __init__( self, *data, **kwargs ):
        """
        Keyword Arguments:
        `label`: optional label to identify the data set; defaults to `None`.
        `is_simple`: optional boolean; defaults to `True`. If `True`, the data set is a population sample, `False` otherwise.
        `lazy_computation`: optional boolean; defaults to `True`. If `True`, the statistics should be computed only when they are asked for or required, `False` otherwise.
        """

        lazy_computation = bool( kwargs.get( "lazy_computation", True ) )
        label = kwargs.get( "label", None )

        is_sample = kwargs.get( "is_sample", None )
        if is_sample is None:
            is_sample = True
        else:
            is_sample = bool( is_sample )

        self._label = label
        self._copy_data( data )
        self._is_sample = is_sample

        self._initialize()
        self.clear_results()

        if not lazy_computation:
            self.compute_results()

    def _initialize( self ):
        self._total_range = CachedValue()
        self._quartiles = CachedValue()

        self._frequency_distribution = CachedValue()
        self._least_frequent_values = CachedValue()
        self._most_frequent_values = CachedValue()
        self._unique_values = CachedValue()

        self._arithmetic_mean = CachedValue()
        self._quadratic_mean = CachedValue()
        self._cubic_mean = CachedValue()
        self._geometric_mean = CachedValue()
        self._harmonic_mean = CachedValue()

        self._modes = CachedValue()
        self._mode_frequency = CachedValue()

        self._median_frequency = CachedValue()
        self._low_median = CachedValue()
        self._low_median_frequency = CachedValue()
        self._high_median = CachedValue()
        self._high_median_frequency = CachedValue()
        self._median_count = CachedValue()

        self._variance = CachedValue()
        self._standard_deviation = CachedValue()
        self._skew = CachedValue()
        self._kurtosis_excess = CachedValue()

        self._sum = CachedValue()
        self._standard_scores = CachedValue()

    def clear_results( self ):
        self._frequency_distribution.clear()
        self._least_frequent_values.clear()
        self._most_frequent_values.clear()
        self._unique_values.clear()

        self._total_range.clear()
        self._quartiles.clear()

        self._arithmetic_mean.clear()
        self._quadratic_mean.clear()
        self._cubic_mean.clear()
        self._geometric_mean.clear()
        self._harmonic_mean.clear()

        self._modes.clear()
        self._mode_frequency.clear()

        self._median_frequency.clear()
        self._low_median.clear()
        self._low_median_frequency.clear()
        self._high_median.clear()
        self._high_median_frequency.clear()
        self._median_count.clear()

        self._variance.clear()
        self._standard_deviation.clear()
        self._skew.clear()
        self._kurtosis_excess.clear()

        self._sum.clear()
        self._standard_scores.clear()

    def compute_results( self ):
        self.frequency_distribution
        self.least_frequent_values
        self.most_frequent_values
        self.unique_values

        self.total_range
        self.quartiles

        self.arithmetic_mean
        self.quadratic_mean
        self.cubic_mean
        self.geometric_mean
        self.harmonic_mean

        self.modes
        self.mode_frequency

        self.median_frequency
        self.low_median
        self.low_median_frequency
        self.high_median
        self.high_median_frequency
        self.median_count

        self.variance
        self.standard_deviation
        self.skew
        self.kurtosis_excess

        self.sum
        self.standard_scores

    def _copy_data( self, input_data ):
        self._data = input_data
        self.__raw_data = input_data

    @property
    def label( self ):
        """
        The label used to identify the data set.
        """

        return self._label

    @property
    def has_label( self ):
        """
        `True` if the data set's label is not `None`, `False` otherwise.
        """

        return self.label is not None

    @property
    def _raw_data( self ):
        return self.__raw_data

    @property
    def data( self ):
        """
        The items of the data set.
        """

        return self._data

    def get_sorted_data( self, comparator = None, reverse = False ):
        """
        Gets the data set sorted in a specific fashion specified by the comparator and option reversal.

        Default comparator is used if none is provided.
        Default ordering is ascending.
        """

        kwargs = { "sort_cmp": comparator, "sort_reverse": reverse }
        return sort_values( *self._raw_data, **kwargs )

    @property
    def size( self ):
        """
        Gets the number of items in the data set.
        """

        return len( self._raw_data )

    def __len__( self ):
        """
        Gets the number of items in the data set.
        """

        return self.size

    @property
    def is_population( self ):
        """
        `True` if the data set is an entire population, `False` otherwise.
        """

        return not self.is_sample

    @property
    def is_sample( self ):
        """
        `True` if the data set is a sample of a population, 'False` otherwise.
        """

        return self._is_sample

    @property
    def minimum_value( self ):
        """
        Gets the minimum data set value.
        """

        return self.quartiles.five_number_summary[ 0 ]

    @property
    def maximum_value( self ):
        """
        Gets the maximum data set value.
        """

        return self.quartiles.five_number_summary[ -1 ]

    def get_least_frequent_values( self, quantity = 1 ):
        """
        Gets the given quantity of the least frequent of data set values. If there is a tie between the least frequent data set values, all of the data set values which the least frequently-occurring values are returned.
        """

        frequencies = self.frequency_distribution.get_least_common_frequencies( quantity )
        return frozenset( self.frequency_distribution.get_values_with_frequencies( lambda freq: freq in frequencies ) )

    @property
    def least_frequent_values( self ):
        """
        Gets the least frequent of data set values.
        """

        if not self._least_frequent_values.has_value:
            self._least_frequent_values.set_value( self.get_least_frequent_values() )

        return self._least_frequent_values.value

    def get_most_frequent_values( self, quantity = 1 ):
        """
        Gets the given quantity of the most frequent of data set values. If there is a tie between the most frequent data set values, all of the data set values which the most frequently-occurring values are returned.
        """

        frequencies = self.frequency_distribution.get_most_common_frequencies( quantity )
        return frozenset( self.frequency_distribution.get_values_with_frequencies( lambda freq: freq in frequencies ) )

    @property
    def most_frequent_values( self ):
        """
        Gets the most frequent of data set values.
        """

        if not self._most_frequent_values.has_value:
            self._most_frequent_values.set_value( self.get_most_frequent_values() )

        return self._most_frequent_values.value

    @property
    def unique_values( self ):
        """
        Gets the set of unique values in the data set.
        """

        if not self._unique_values.has_value:
            self._unique_values.set_value( frozenset( self.frequency_distribution ) )

        return self._unique_values.value

    @property
    def unique_value_count( self ):
        """
        Gets the number of unique values in the data set.
        """

        return len( self.unique_values )

    @property
    def total_range( self ):
        """
        Gets the total range of the data set.
        """

        if not self._total_range.has_value:
            self._total_range.set_value( self.maximum_value - self.minimum_value )

        return self._total_range.value

    @property
    def interquartile_range( self ):
        """
        Gets the interquartile range of the data set.
        """

        return self.quartiles.interquartile_range

    def get_quartile_information( self, **kwargs ):
        """
        Gets the quartile information for the data set.
        """

        return quartiles.DataSetQuartileInformation( *self._raw_data, **kwargs )

    @property
    def quartiles( self ):
        """
        Gets the quartiles of the data set.
        """

        if not self._quartiles.has_value:
            self._quartiles.set_value( self.get_quartile_information() )

        return self._quartiles.value

    @property
    def frequency_distribution( self ):
        """
        Gets the frequency distribution for the data set.
        """

        if not self._frequency_distribution.has_value:
            self._frequency_distribution.set_value( get_frequency_distribution( *self._raw_data ) )

        return self._frequency_distribution.value

    def get_arithmetic_mean( self, **kwargs ):
        """
        Gets the arithmetic mean for the data set.

        Keyword options:
        `weights`: list of weights to apply to the data set for the calculation.
        `normalize_weights`: True if the weights are to be normalized before the calculation, False otherwise.
        """

        return mean.compute_arithmetic_mean( *self._raw_data, **kwargs )

    @property
    def arithmetic_mean( self ):
        """
        Gets the unweighted arithmetic mean of the data set.
        """

        if not self._arithmetic_mean.has_value:
            self._arithmetic_mean.set_value( self.get_arithmetic_mean() )

        return self._arithmetic_mean.value

    def get_quadratic_mean( self, **kwargs ):
        """
        Gets the quadratic mean of the data set. It is sometimes also referred to as the root mean square value.

        Keyword options:
        `weights`: list of weights to apply to the data set for the calculation.
        `normalize_weights`: True if the weights are to be normalized before the calculation, False otherwise.
        """

        return mean.compute_quadratic_mean( *self._raw_data, **kwargs )

    @property
    def quadratic_mean( self ):
        """
        Gets the unweighted quadratic mean of the data set. It is sometimes also referred to as the root mean square value.
        """

        if not self._quadratic_mean.has_value:
            self._quadratic_mean.set_value( self.get_quadratic_mean() )

        return self._quadratic_mean.value

    def get_cubic_mean( self, **kwargs ):
        """
        Gets the cubic mean of the data set.

        Keyword options:
        `weights`: list of weights to apply to the data set for the calculation.
        `normalize_weights`: True if the weights are to be normalized before the calculation, False otherwise.
        """

        return mean.compute_cubic_mean( *self._raw_data, **kwargs )

    @property
    def cubic_mean( self ):
        """
        Gets the unweighted cubic mean of the data set.
        """

        if not self._cubic_mean.has_value:
            self._cubic_mean.set_value( self.get_cubic_mean() )

        return self._cubic_mean.value

    def get_geometric_mean( self, **kwargs ):
        """
        Gets the geometric mean of the data set.

        Keyword options:
        `weights`: list of weights to apply to the data set for the calculation.
        `normalize_weights`: True if the weights are to be normalized before the calculation, False otherwise.

        Note: the result of the geometric mean is a complex value.
        """

        return mean.compute_geometric_mean( *self._raw_data, **kwargs )

    @property
    def geometric_mean( self ):
        """
        Gets the unweighted geometric mean of the data set.
        """

        if not self._geometric_mean.has_value:
            self._geometric_mean.set_value( self.get_geometric_mean() )

        return self._geometric_mean.value

    def get_harmonic_mean( self, **kwargs ):
        """
        Gets the harmonic mean of the data set.

        Keyword options:
        `weights`: list of weights to apply to the data set for the calculation.
        `normalize_weights`: True if the weights are to be normalized before the calculation, False otherwise.
        """

        return mean.compute_harmonic_mean( *self._raw_data, **kwargs )

    @property
    def harmonic_mean( self ):
        """
        Gets the unweighted harmonic mean of the data set.
        """

        if not self._harmonic_mean.has_value:
            self._harmonic_mean.set_value( self.get_harmonic_mean() )

        return self._harmonic_mean.value

    def get_generalized_mean( self, power, **kwargs ):
        """
        Gets the generalized mean with the given power of the data set.

        Keyword options:
        `weights`: list of weights to apply to the data set for the calculation.
        `normalize_weights`: True if the weights are to be normalized before the calculation, False otherwise.

        Note: the result of the geometric mean is a complex value.
        """

        return mean.compute_generalized_mean( power, *self._raw_data, **kwargs )

    @property
    def modes( self ):
        """
        Gets the modes of the data set.
        """

        if not self._modes.has_value:
            self._modes.set_value( mode.get_modes( self.frequency_distribution ) )

        return self._modes.value

    @property
    def mode_frequency( self ):
        """
        Gets the frequency of the data set's mode.
        """

        if not self._mode_frequency.has_value:
            self._mode_frequency.set_value( self.frequency_distribution[ self.modes[ 0 ] ] )

        return self._mode_frequency.value

    @property
    def mode_count( self ):
        """
        Gets the number of modes in the data set.
        """

        return len( self.modes )

    @property
    def median( self ):
        """
        Gets the median of the data set. Note: depending on the size of the data set and the data present, the computed median may not exist in the data set.
        """

        return self.quartiles.q2_q3_fence.value

    @property
    def median_frequency( self ):
        """
        Gets the count of the data set's median. Note: if the high and low median are different, the count of the median will be zero.
        """

        if not self._median_frequency.has_value:
            self._median_frequency.set_value( self.frequency_distribution[ self.median ] )

        return self._median_frequency.value

    def _set_medians( self ):
        """
        Sets the low and high median values for the data set.
        """

        if not self._high_median.has_value: # self._low_median.has_value and self._median_count.has_value are equivalent values to check for existence.
            if self.quartiles.q2_q3_fence.value_in_dataset:
                high = low = self.quartiles.q2_q3_fence.value
                median_count = self.frequency_distribution[ high ]
            else:
                high = self.quartiles.q3_values[ 0 ]
                low = self.quartiles.q2_values[ -1 ]
                median_count = 0

            self._low_median.set_value( low )
            self._high_median.set_value( high )
            self._median_count.set_value( median_count )

    @property
    def high_median( self ):
        """
        Gets the high median of the data set.
        """

        if not self._high_median.has_value:
            self._set_medians()

        return self._high_median.value

    @property
    def high_median_frequency( self ):
        """
        Gets the count of the data set's high median.
        """

        if not self._high_median_frequency.has_value:
            self._high_median_frequency.set_value( self.frequency_distribution[ self.high_median ] )

        return self._high_median_frequency.value

    @property
    def low_median( self ):
        """
        Gets the low median of the data set.
        """

        if not self._low_median.has_value:
            self._set_medians()

        return self._low_median.value

    @property
    def low_median_frequency( self ):
        """
        Gets the count of the data set's low median.
        """

        if not self._low_median_frequency.has_value:
            self._low_median_frequency.set_value( self.frequency_distribution[ self.low_median ] )

        return self._low_median_frequency.value

    @property
    def median_count( self ):
        """
        Gets the number of modes in the data set.
        """

        if not self._median_count.has_value:
            self._set_medians()

        return self._median_count.value

    @property
    def is_median_in_data_set( self ):
        """
        True if the median is in the data set, False otherwise.
        """

        return self.median_count > 0

    @property
    def variance( self ):
        """
        Computes the variance of the data set.
        """

        if not self._variance.has_value:
            self._variance.set_value( moments.compute_variance( self.arithmetic_mean, *self._raw_data ) )

        return self._variance.value

    @property
    def standard_deviation( self ):
        """
        Computes the standard deviation of the data set.
        """

        if not self._standard_deviation.has_value:
            self._standard_deviation.set_value( moments.compute_standard_deviation( self.arithmetic_mean, *self._raw_data ) )

        return self._standard_deviation.value

    @property
    def skew( self ):
        """
        Computes the skew of the data set.
        """

        if not self._skew.has_value:
            self._skew.set_value( moments.compute_skew( self.arithmetic_mean, *self._raw_data ) )

        return self._skew.value

    @property
    def kurtosis_excess( self ):
        """
        Computes the kurtosis excess of the data set.
        """

        if not self._kurtosis_excess.has_value:
            self._kurtosis_excess.set_value( moments.compute_kurtosis_excess( self.arithmetic_mean, *self._raw_data ) )

        return self._kurtosis_excess.value

    @property
    def sum( self ):
        """
        Gets the sum of the data set values.
        """

        if not self._sum.has_value:
            self._sum.set_value( sum( self.data ) )

        return self._sum.value

    @property
    def standard_scores( self ):
        """
        Computes the standard scores of the data set.
        """

        if not self._standard_scores.has_value:
            self._standard_scores.set_value( self.transform( lambda x: scores.calculate_standard_score( x, self.arithmetic_mean, self.standard_deviation ) ) )

        return self._standard_scores.value

    def __enter__( self ):
        return self

    def __exit__( self, exc_type, exc_value, traceback ):
        pass

    def __hash__( self ):
        return get_hash( self.__class__.__name__, *self._raw_data )

    def transform( self, transformation, **kwargs ):
        """
        Uses the transformation callable to transform the data set items and place the transformed items into a new `StatisticsSet` (using the given keyword arguments).

        The transformation callable signature is ( element ).
        """

        if transformation is None:
            raise ValueError( "Transformation cannot be None." )
        else:
            return self.__class__( *[ transformation( item ) for item in self._raw_data ], **kwargs )

    def _apply_scalar_operation( self, other, operation, label, **kwargs ):
        if operation is None:
            raise ValueError( "Operation cannot be None." )
        else:
            try:
                o = float( other )
            except:
                raise ValueError( "Invalid type to apply {} operation to statistics set: value must a scalar.".format( label ) )
            else:
                return self.transform( lambda x: operation( x, o ), **kwargs )

    def vector_transform( self, transformation, *vector, **kwargs ):
        """
        Uses the transformation callable and the vector to transform the data set items and place the transformed items into a new `StatisticsSet` (using the given keyword arguments). The vector must be the same size as the data set.

        The transformation callable signature is ( element, vector value ).
        """

        return self._apply_element_vector_operation( vector, transformation, "user-provided transform", **kwargs )

    def _apply_element_vector_operation( self, vector, operation, label, **kwargs ):
        if operation is None:
            raise ValueError( "Operation cannot be None." )
        elif isinstance( vector, StatisticsSet ):
            vect = vector.data
        elif isinstance( vector, ( list, tuple ) ):
            vect = vector
        else:
            raise ValueError( "Invalid type to apply {} operation to statistics set: value must a vector.".format( label ) )

        if len( vect ) == self.size:
            values = [ operation( self._raw_data[ i ], o ) for i, o in enumerate( vect ) ]
            return self.__class__( *values, **kwargs )
        else:
            raise ValueError( "Input vector of values must be the same length as the data set({}): {}".format( self.size, len( vect ) ) )

    def _apply_operation( self, operand, operation, label, **kwargs ):
        if isinstance( operand, ( StatisticsSet, list, tuple ) ):
            result = self._apply_element_vector_operation( operand, operation, label, **kwargs )
        else:
            result = self._apply_scalar_operation( operand, operation, label, **kwargs )

        return result

    def __abs__( self ):
        return self.transform( lambda x: abs( x ) )

    def __pos__( self ):
        return self.transform( lambda x:+x )

    def __neg__( self ):
        return self.transform( lambda x:-x )

    def __add__( self, other ):
        return self._apply_operation( other, lambda a, b: a + b, "addition" )

    def __mod__( self, other ):
        return self._apply_operation( other, lambda a, b: a % b, "modulo" )

    def __mul__( self, other ):
        return self._apply_operation( other, lambda a, b: a * b, "multiplication" )

    def __div__( self, other ):
        return self._apply_operation( other, lambda a, b: a / b, "classic division" )

    def __floordiv__( self, other ):
        return self._apply_operation( other, lambda a, b: a // b, "floor division" )

    def __pow__( self, other ):
        return self._apply_operation( other, lambda a, b: a ** b, "exponentiation" )

    def __sub__( self, other ):
        return self._apply_operation( other, lambda a, b: a - b, "subtraction" )

    def __truediv__( self, other ):
        return self._apply_operation( other, lambda a, b: a / b, "true division" )
