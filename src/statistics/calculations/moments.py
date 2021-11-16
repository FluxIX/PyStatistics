import math
from ..utilities.math import integer_power

def compute_variance( mean, *values, **kwargs ):
    """
    Computes the variance of the given values using the given mean.
    """

    moment = compute_central_moment( 2, mean, *values, **kwargs )

    return float( moment ) / len( values )

def compute_standard_deviation( mean, *values, **kwargs ):
    """
    Computes the variance of the given values using the given mean.
    """

    return math.sqrt( compute_variance( mean, *values, **kwargs ) )

def compute_skew( mean, *values, **kwargs ):
    """
    Computes the variance of the given values using the given mean.
    """

    moment = compute_central_moment( 3, mean, *values, **kwargs )
    variance = compute_variance( mean, *values, **kwargs )
    standard_deviation = math.sqrt( variance )

    return float( moment ) / ( variance * standard_deviation ) / len( values )

def compute_kurtosis_excess( mean, *values, **kwargs ):
    """
    Computes the variance of the given values using the given mean.

    References: https://en.wikipedia.org/wiki/Kurtosis
    """

    moment = compute_central_moment( 4, mean, *values, **kwargs )
    variance = compute_variance( mean, *values, **kwargs )

    return float( moment ) / integer_power( variance, 2 ) / len( values ) - 3

def compute_item_central_moment( ordinal, mean, value, **kwargs ):
    """
    Computes the central moment with the given ordinal for a single value using the given mean.
    """

    if ordinal is None:
        raise ValueError( "Ordinal cannot be None." )
    elif ordinal <= 0:
        raise ValueError( "Ordinal ({}) must be positive,".format( ordinal ) )
    else:
        return ( value - mean ) ** ordinal

def compute_central_moment( ordinal, mean, *values, **kwargs ):
    """
    Computes the central moment with the given ordinal for the given values using the given mean.

    References: https://en.wikipedia.org/wiki/Central_moment
    """

    if ordinal is None:
        raise ValueError( "Ordinal cannot be None." )
    elif ordinal <= 0:
        raise ValueError( "Ordinal ({}) must be positive,".format( ordinal ) )
    elif mean is None:
        raise ValueError( "Mean cannot be None." )
    else:
        return sum( map( lambda value: compute_item_central_moment( ordinal, mean, value, **kwargs ), values ) )
