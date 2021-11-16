__version__ = r"1.0"

class NotSupportedException( NotImplementedError ):
    """
    An exception which represents a situation where the requested operation is not supported by the object.

    NOTE: this inherits from `NotImplementedError`.
    """

    pass
