__version__ = r"1.0"

from functools import reduce
from ..utilities.iterable import iterable_all

def _validate_statistic_sets( *statistics_sets, **kwargs ):
    if len( statistics_sets ) <= 1:
        raise ValueError( "Insufficient number of statistic sets ({}) to calculate.".format( len( statistics_sets ) ) )
    elif iterable_all( statistics_sets ) and len( set( [ stat_set.size for stat_set in statistics_sets ] ) ) == 1:
        result = True

        check_type = kwargs.get( "check_type", None )
        if check_type is None:
            check_type = False
        else:
            check_type = bool( check_type )

        if check_type:
            result = len( set( [ stat_set.is_sample for stat_set in statistics_sets ] ) ) == 1

            if not result:
                raise ValueError( "Data set types are different." )
    else:
        raise ValueError( "Data set sizes are not equal." )

def calculate_covariance( *statistics_sets, **kwargs ):
    """
    Calculates the covariance of the provided statistics sets.
    
    Adapted from: https://en.wikipedia.org/wiki/Covariance
    """

    # if statistics_set_a.size != statistics_set_b.size:
    #     raise ValueError( "Data set sizes are not equal." )
    # else:
    #     raw_expected_value_a = kwargs.get( "expected_value_a", None )
    #     if raw_expected_value_a is None:
    #         expected_value_a = statistics_set_a.arithmetic_mean
    #     else:
    #         expected_value_a = float( raw_expected_value_a )
    #
    #     raw_expected_value_b = kwargs.get( "expected_value_b", None )
    #     if raw_expected_value_b is None:
    #         expected_value_b = statistics_set_b.arithmetic_mean
    #     else:
    #         expected_value_b = float( raw_expected_value_b )
    #
    #     return ( ( statistics_set_a - expected_value_a ) * ( statistics_set_b - expected_value_b ) ).sum() / statistics_set_a.size

    _validate_statistic_sets( *statistics_sets, **kwargs )

    data_size = statistics_sets[ 0 ].size

    raw_expected_values = kwargs.get( "expected_values", None )
    if raw_expected_values is None:
        expected_values = [ stat_set.arithmetic_mean for stat_set in statistics_sets ]
    elif len( raw_expected_values ) != data_size:
        raise ValueError( "Expected values were provided, ({}), but are not the same size as the number of data sets ({}).".format( len( expected_values ), data_size ) )
    else:
        expected_values = []
        for index_, value in enumerate( raw_expected_values ):
            stat_set = statistics_sets[ index_ ]

            if value is None:
                expected_value = stat_set.arithmetic_mean
            else:
                expected_value = value

            expected_values.append( expected_value )

    stat_data = zip( statistics_sets, expected_values )

    return reduce( lambda x, y: x * y, [ stat_set - expected_value for stat_set, expected_value in stat_data ] ).sum / data_size

def calculate_population_pearson_product_moment_correlation_coefficient( *statistics_sets, **kwargs ):
    """
    Calculates the centered Pearson product-moment correlation coefficient for the given population statistics sets.
    
    This metric is also known as the Pearson correlation coefficient or bivariate correlation, and is the assumed metric for "correlation coefficient" when no qualifiers are provided.
    
    Adapted from: https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
    """

    _validate_statistic_sets( *statistics_sets, **kwargs )

    return calculate_covariance( *statistics_sets, **kwargs ) / reduce( lambda x, y: x * y, [ stat_set.standard_deviation for stat_set in statistics_sets ] )

def calculate_sample_pearson_product_moment_correlation_coefficient( *statistics_sets, **kwargs ):
    """
    Calculates the centered Pearson product-moment correlation coefficient for the given sample statistics sets.
    
    This metric is also known as the Pearson correlation coefficient or bivariate correlation, and is the assumed metric for "correlation coefficient" when no qualifiers are provided.
    
    Adapted from: https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
    """

    # if statistics_set_a.size != statistics_set_b.size:
    #     raise ValueError( "Data set sizes are not equal." )
    # else:
    #     return ( statistics_set_a.standard_scores * statistics_set_b.standard_scores ).sum() / ( statistics_set_a.size - 1 )

    _validate_statistic_sets( *statistics_sets, **kwargs )

    data_size = statistics_sets[ 0 ].size
    return reduce( lambda x, y: x * y, [ stat_set.standard_scores for stat_set in statistics_sets ] ).sum() / ( data_size - 1 )

def calculate_pearson_product_moment_correlation_coefficient( *statistics_sets, **kwargs ):
    """
    Calculates the centered Pearson product-moment correlation coefficient for the given statistics sets. The type of calculation (sample or population) is determined from the given statistic sets and all set need to be the same.

    This metric is also known as the Pearson correlation coefficient or bivariate correlation, and is the assumed metric for "correlation coefficient" when no qualifiers are provided.

    Adapted from: https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
    """

    keyword_args = kwargs.copy()
    keyword_args.update( check_type = True )

    _validate_statistic_sets( *statistics_sets, **keyword_args )

    is_sample = statistics_sets[ 0 ].is_sample

    if is_sample:
        result = calculate_sample_pearson_product_moment_correlation_coefficient( *statistics_sets, **kwargs )
    else:
        result = calculate_population_pearson_product_moment_correlation_coefficient( *statistics_sets, **kwargs )

    return result
