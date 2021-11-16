__version__ = r"1.0"

def calculate_standard_score( data_value, arithmetic_mean, standard_deviation, **kwargs ):
    """
    Computes the standard score for the given data value.

    The standard score is also known as the z-score.

    Adapted from: https://en.wikipedia.org/wiki/Standard_score
    """

    return ( float( data_value ) - arithmetic_mean ) / standard_deviation
