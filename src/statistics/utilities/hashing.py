__version__ = r"1.0"

_prime_sequence = tuple( [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31 ] )
_num_primes = len( _prime_sequence )

def get_hash( initial_item, *subsequent_items, **kwargs ):
    """
    Gets the 32-bit hash value of the given items.
    """

    result = hash( initial_item )

    for item_index, item in enumerate( subsequent_items ):
        prime_index = item_index % _num_primes
        shift_higher_quantity = _prime_sequence[ prime_index ]
        shift_lower_quantity = 32 - shift_higher_quantity

        # We rotate the current value higher (with the overflow going into the lower bits) to ensure distribution of the bit-data in a loss-less fashion.
        result = ( ( result << shift_higher_quantity ) & 0xFFFFFFFF ) | ( result >> shift_lower_quantity )
        result ^= hash( item )

    return result
