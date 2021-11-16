def iterable_any( collection, predicate = None ):
    """
    Returns True if any item in the given collection evaluate to True using the given predicate, False otherwise. If the predicate is None, the returns True if an item in the collection is not None, False otherwise.
    """

    if predicate is None:
        predicate = lambda x: x is not None

    result = False
    for item in collection:
        result = predicate( item )
        if result:
            break

    return result

def iterable_count( collection, predicate = None ):
    """
    Returns the count of items in the given collection which evaluate to True using the given predicate. If the predicate is None, the returns the count of items in the collection are not None.
    """

    if predicate is None:
        predicate = lambda x: x is not None

    result = 0
    for item in collection:
        if predicate( item ):
            result += 1

    return result

def iterable_all( collection, predicate = None ):
    """
    Returns True if all items in the given collection evaluate to True using the given predicate, False otherwise. If the predicate is None, the returns True if all items in the collection are not None, False otherwise.
    """

    return iterable_count( collection, predicate = predicate ) == len( collection )
