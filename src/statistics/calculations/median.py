__version__ = r"1.0"

from ..utilities.dict import update_if_not_set
from ..utilities.sorting import get_values

def get_median( *values, **kwargs ):
    """
    Gets the median for the given values. Sorting is conditional given a keyword argument value and will use a `sort_cmp`, `sort_key`, and/or `sort_reverse` flag for sorting if they are provided.
    """

    medians = get_medians( *values, **kwargs )
    if len( medians ) > 1:
        low, high = medians
        result = float( low + high ) / 2
    else:
        result = medians[ 0 ]

    return result

def get_medians( *values, **kwargs ):
    """
    Gets the medians for the given values. Sorting is conditional given a keyword argument value and will use a `sort_cmp`, `sort_key`, and/or `sort_reverse` flag for sorting if they are provided.
    """

    low_index, high_index = get_median_positions( len( values ), **kwargs )

    data_length = len( values )

    if data_length == 1:
        result = ( values[ low_index ], )
    else:
        keyword_args = update_if_not_set( kwargs, ( "sort", True ), in_place = False )
        data = get_values( *values, **keyword_args )

        if low_index == high_index:
            result = ( data[ low_index ], )
        else:
            result = data[ low_index ], data[ high_index ]

    return result

def get_median_positions( value_count, **kwargs ):
    """
    Gets the positions of the medians for the given value count.
    """

    if value_count is None:
        raise ValueError( "Value count cannot be None." )
    else:
        data_length = int( value_count )

        if data_length <= 0:
            raise ValueError( "Data set must have at least one value in it." )
        elif data_length == 1:
            result = ( 0, )
        else:
            low_index = data_length // 2

            if data_length % 2 == 1:
                result = ( low_index, )
            else:
                high_index = low_index + 1

                result = low_index, high_index

        return result
