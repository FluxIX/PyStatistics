__version__ = r"1.0"

def update_if_not_set( dictionary, *key_value_pairs, **kwargs ):
    """
    Updates the given dictionary with the given values if the associated keys don't already exist, otherwise the value is not changed. The changed dictionary is returned.

    Keyword Arguments:
    `in_place`: if True the updates are done in-place, otherwise the updates are made in a copy.
    """

    in_place = bool( kwargs.get( "in_place", True ) )

    if in_place:
        result = dictionary
    else:
        result = dictionary.copy()

    for key, value in key_value_pairs:
        if key not in result:
            result[ key ] = value

    return result
