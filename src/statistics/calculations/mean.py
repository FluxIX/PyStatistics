__version__ = r"1.0"

import math
from ..utilities.argument_unpacking import unpack_arguments
from ..utilities.math import compute_real_root

def _validate_values( *values, **kwargs ):
    if len( values ) == 0:
        raise ValueError( "No values provided." )

def _get_weights( value_count, **kwargs ):
    weights_equal = None

    weights = kwargs.get( "weights", None )
    if weights is not None:
        if type( weights ) != list:
            raise ValueError( "Given weights are not in a valid structure: a list is required." )
        elif len( weights ) != value_count:
            raise ValueError( "Invalid number of weights provided: {}; {} weights expected.".format( len( weights ), value_count ) )
        else:
            has_weights = True
    else:
        has_weights = False

        default_weight_override = kwargs.get( "default_weight_override", None )
        if default_weight_override is None:
            # weight of an unweighted mean value is 1/n; this is described in the generalized mean references.
            weights = [ 1.0 / value_count ] * value_count
            weights_equal = True
        else:
            weights = default_weight_override

    if weights_equal is None:
        weight = None
        weights_equal = True
        for w in weights:
            if weight is None:
                weight = w
            elif weight != w:
                weights_equal = False
                break

    if not weights_equal:
        normalize_weights = bool( kwargs.get( "normalize_weights", False ) )
        if normalize_weights:
            weights = [ float( weight ) / value_count for weight in weights ]

    return has_weights, weights_equal, weights

def _get_weighted_summation( weights, values ):
    return sum( map( lambda t: t[ 0 ] * t[ 1 ], zip( weights, values ) ) )

def compute_harmonic_mean( *values, **kwargs ):
    """
    Computes the harmonic mean for the given values.

    Note: The return result is a complex value.
    Note: if value weights are provided, the sequence aggregation is *not* divided by the number of values in the sequence; the given weights are assumed to include that factor if it applies.

    References: https://en.wikipedia.org/wiki/Harmonic_mean
    """

    return compute_generalized_mean( -1, *values, **kwargs )

def compute_geometric_mean( *values, **kwargs ):
    """
    Computes the geometric mean for the given values.

    Note: The return result is a complex value.
    References: https://en.wikipedia.org/wiki/Geometric_mean, https://en.wikipedia.org/wiki/Weighted_geometric_mean
    """

    values = unpack_arguments( values )

    _validate_values( *values, **kwargs )

    value_count = len( values )

    if value_count > 1:
        if "default_weight_override" not in kwargs:
            keyword_args = kwargs.copy()
            keyword_args[ "default_weight_override" ] = [ 1 ] * value_count
        else:
            keyword_args = kwargs

        has_weights, weights_equal, weights = _get_weights( value_count, **keyword_args )

        # if all weights are equal, the effect of the weights would be negated, so we save ourselves the potential error and performance cost.
        has_weights = has_weights and not weights_equal

        if has_weights:
            # TODO: add parameter checking: ln( x ) is only valid on x > 0, forbid division by 0

            value_summation = _get_weighted_summation( weights, map( lambda x: math.log( x ), values ) )
            weight_summation = sum( weights )
            result = math.exp( float( value_summation ) / weight_summation )
        else:
            value_product = reduce( lambda x, y: x * y, values )
            result = compute_real_root( value_product, value_count )
    else:
        result = complex( values[ 0 ], 0 )

    return result

def compute_arithmetic_mean( *values, **kwargs ):
    """
    Computes the arithmetic mean for the given values.

    Note: if value weights are provided, the sequence aggregation is *not* divided by the number of values in the sequence; the given weights are assumed to include that factor if it applies.

    References: https://en.wikipedia.org/wiki/Arithmetic_mean
    """

    values = unpack_arguments( values )

    _validate_values( *values, **kwargs )

    value_count = len( values )

    if value_count > 1:
        has_weights, weights_equal, weights = _get_weights( value_count, **kwargs )

        # if all weights are equal, the effect of the weights would be negated, so we save ourselves the potential error and performance cost.
        has_weights = has_weights and not weights_equal

        if has_weights:
            result = _get_weighted_summation( weights, values )
        else:
            result = float( sum( values ) ) / value_count
    else:
        result = values[ 0 ]

    return result

def compute_quadratic_mean( *values, **kwargs ):
    """
    Computes the quadratic mean for the given values.

    Note: if value weights are provided, the sequence aggregation is *not* divided by the number of values in the sequence; the given weights are assumed to include that factor if it applies.

    References: https://en.wikipedia.org/wiki/Root_mean_square
    """

    raw_result = compute_geometric_mean( 2, *values, **kwargs )
    if raw_result.imag != 0:
        raise ValueError( "The weights provided for the quadratic mean resulted in an imaginary mean." )
    else:
        return raw_result.real

def compute_cubic_mean( *values, **kwargs ):
    """
    Computes the cubic mean for the given values.

    Note: if value weights are provided, the sequence aggregation is *not* divided by the number of values in the sequence; the given weights are assumed to include that factor if it applies.

    References: https://en.wikipedia.org/wiki/Cubic_mean
    """

    return compute_geometric_mean( 3, *values, **kwargs ).real

def compute_generalized_mean( power, *values, **kwargs ):
    """
    Computes the generalized mean with the given power for the given values.

    Note: The return result is a complex value.
    Note: if value weights are provided, the sequence aggregation is *not* divided by the number of values in the sequence; the given weights are assumed to include that factor if it applies.

    References: https://en.wikipedia.org/wiki/Generalized_mean
    """

    values = unpack_arguments( values )

    _validate_values( *values, **kwargs )

    value_count = len( values )

    if value_count > 1:
        order = int( power )
        if float( order ) != float( power ):
            raise ValueError( "Generalized mean power must be an integer." )
        elif order == 1:
            result = compute_arithmetic_mean( *values, **kwargs )
        elif order == 0:
            result = compute_geometric_mean( *values, **kwargs )
        else:
            value_count = len( values )

            has_weights, weights_equal, weights = _get_weights( value_count, **kwargs )

            # if all weights are equal, the effect of the weights would be negated, so we save ourselves the potential error and performance cost.
            has_weights = has_weights and not weights_equal

            if has_weights:
                value_sum = _get_weighted_summation( weights, map( lambda x: pow( x, order ), values ) )
                result = compute_real_root( value_sum, order )
            else:
                value_sum = sum( map( lambda x: pow( x, order ), values ) )
                result = compute_real_root( float( value_sum ) / value_count, order )
    else:
        result = complex( values[ 0 ], 0 )

    return result
