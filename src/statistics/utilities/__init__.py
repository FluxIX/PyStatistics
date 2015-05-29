__version__ = r"1.0"

def integer_power( base, exponent ):
    result = 1

    processed = 0
    while processed < exponent:
        result *= base
        processed += 1

    return result
    #return base ** exponent

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
        return left - right < tolerance

def floating_point_not_equal( left, right, tolerance = 0.0 ):
    return not floating_point_equal( left, right, tolerance )
