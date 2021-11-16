__version__ = r"1.0"

from .argument_unpacking import unpack_arguments

def sort_values( *values, **kwargs ):
    """
    Sorts the given values using the `sort_cmp`, `sort_key`, and/or `sort_reverse` flag for sorting if they are provided.
    """

    comparator = kwargs.get( "sort_cmp", None )
    key = kwargs.get( "sort_key", None )
    reverse = bool( kwargs.get( "sort_reverse", False ) )

    return sorted( values, cmp = comparator, key = key, reverse = reverse )

def get_values( *values, **kwargs ):
    """
    Conditionally sorts the given values as determined by the `sort` flag using the `sort_cmp`, `sort_key`, and/or `sort_reverse` flag for sorting if they are provided, otherwise returns the input values.

    Values are not sorted by default.
    """

    sort_data = bool( kwargs.get( "sort", False ) )

    values = unpack_arguments( values )

    if sort_data:
        result = sort_values( *values, **kwargs )
    else:
        result = values

    return result
