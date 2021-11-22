def compute_relative_error( experimental_value, oracle_value, **kwargs ):
    """
    Computes the relative error of the experimental value with regards to the oracle value.
    
    Note: the relative error can also be referred to as the relative change.
    
    Keyword args:
    `positive_error`: Boolean flag which forces the error to be non-negative; defaults to True.
    `scale`: Multiplies the raw error by the scale; defaults to 1.
    
    Adapted from: https://en.wikipedia.org/wiki/Relative_difference
    """

    if experimental_value is None:
        raise ValueError( "Experimental value cannot be None." )
    elif oracle_value is None:
        raise ValueError( "Oracle value cannot be None." )
    elif oracle_value == 0:
        raise ValueError( "Oracle value cannot be zero." )
    else:
        positive_error = bool( kwargs.get( "positive_error", True ) )

        scale = kwargs.get( "scale", None )
        if scale is None:
            scale = 1
        else:
            scale = float( scale )

        difference = oracle_value - experimental_value
        result = float( difference ) / oracle_value

        if positive_error:
            result = abs( result )

        if scale != 1:
            result *= scale

        return result

def compute_relative_difference( value_1, value_2, **kwargs ):
    """
    Computes the relative difference of the given values.
    
    Keyword args:
    `positive_difference`: Boolean flag which forces the difference to be non-negative; defaults to True.
    `scale`: Multiplies the raw difference by the scale; defaults to 1.
    
    Adapted from: https://en.wikipedia.org/wiki/Relative_difference
    """

    if value_1 is None:
        raise ValueError( "Value 1 cannot be None." )
    elif value_2 is None:
        raise ValueError( "Value 2 cannot be None." )
    else:
        positive_difference = bool( kwargs.get( "positive_difference", True ) )

        scale = kwargs.get( "scale", None )
        if scale is None:
            scale = 1
        else:
            scale = float( scale )

        difference = value_2 - value_1
        denominator = abs( value_1 ) + abs( value_2 )
        result = 2 * float( difference ) / denominator

        if positive_difference:
            result = abs( result )

        if scale != 1:
            result *= scale

        return result
