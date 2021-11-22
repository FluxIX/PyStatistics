__version__ = r"2.0"

def integer_power( base, exponent ):
    result = 1

    processed = 0
    while processed < exponent:
        result *= base
        processed += 1

    return result

def compute_real_root( value, power ):
    """
    Computes the given power of root for the given value.

    NOTE: this returns a complex value.
    """

    if power == 0:
        raise ValueError( "Power of root cannot be zero." )
    elif power < 0 and value == 0:
        raise ValueError( "Power of root ({}) cannot be less than zero with a zero-value base.".format( power ) )
    elif value == 0 or power == 1:
        result = value
    else:
        # If the `value` is negative, the root will either be a negative, real value or a positive, imaginary value.
        # In both of these cases, pow will not let us compute the root (due to implementation limitations).
        # As a work around, compute the root using the absolute value of the `value` and assign the result to the appropriate value; an even-power root is assigned to the positive, imaginary value and an odd-power root is assigned to the negative, real value.

        calc_value = abs( float( value ) )
        calc_power = abs( power )

        intermediate_result = pow( calc_value, 1.0 / calc_power )

        if value < 0:
            power_is_odd = calc_power % 2 == 1

            if power_is_odd:
                result = complex( -intermediate_result, 0 )
            else:
                result = complex( 0, intermediate_result )
        else:
            result = complex( intermediate_result, 0 )

    return result

def floating_point_less( left, right, tolerance = 0.0 ):
    if tolerance < 0.0:
        raise ValueError( "Tolerance cannot be less than 0.0." )
    else:
        return left < right + tolerance

def floating_point_less_equal( left, right, tolerance = 0.0 ):
    if tolerance < 0.0:
        raise ValueError( "Tolerance cannot be less than 0.0." )
    else:
        return left <= right + tolerance

def floating_point_greater( left, right, tolerance = 0.0 ):
    return floating_point_less_equal( right, left, tolerance )

def floating_point_greater_equal( left, right, tolerance = 0.0 ):
    return floating_point_less( right, left, tolerance )

def floating_point_equal( left, right, tolerance = 0.0 ):
    if tolerance < 0.0:
        raise ValueError( "Tolerance cannot be less than 0.0." )
    else:
        return abs( left - right ) < tolerance

def floating_point_not_equal( left, right, tolerance = 0.0 ):
    return not floating_point_equal( left, right, tolerance )
