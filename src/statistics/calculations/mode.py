from .frequency.frequency import get_frequency_distribution
from .frequency.counter import Counter

def get_modes( *values ):
    """
    Gets the modes for the given data set or Counter.
    """

    if len( values ) == 1 and type( values[ 0 ] ) == Counter:
        counter = values[ 0 ]
    else:
        counter = get_frequency_distribution( *values )

    if len( counter ) > 0:
        mode_frequency = counter.get_most_common_frequencies( 1 )
        return tuple( counter.get_values_with_frequencies( lambda freq: freq in mode_frequency ) )
    else:
        raise ValueError( "The frequency distribution has no values." )
