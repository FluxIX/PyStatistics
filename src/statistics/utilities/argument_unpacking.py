__version__ = r"1.0"

def unpack_arguments( args ):
    """
    Checks the input collection. If it contains a single item, the item is attempted to be unpacked and returned, otherwise the input collection is returned.
    """

    try:
        if len( args ) == 1:
            result = args[ 0 ]
        else:
            result = args
    except:
        result = args

    return result
