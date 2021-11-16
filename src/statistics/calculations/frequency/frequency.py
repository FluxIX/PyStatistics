__version__ = r"1.0"

from .counter import Counter

def get_frequency_distribution( *values, **kwargs ):
    """
    Gets the frequency distribution of the given values.

    Keyword Arguments:
    `mutable`: if True the distribution object will be mutable, otherwise the distribution object will be immutable.
    """

    mutable = bool( kwargs.get( "mutable", False ) )

    result = Counter( *values )

    if not mutable:
        result = result.get_immutable()

    return result
