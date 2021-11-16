class CachedValue( object ):
    """
    Represents a cached value.
    """

    def __init__( self, **kwargs ):
        self.clear()

    @property
    def has_value( self ):
        """
        `True` if a value has been cached, `False` otherwise.
        """

        return self._has_value

    @property
    def value( self ):
        """
        If a value has been cached, the value is returned, otherwise a `ValueError` is raised.
        """

        if self.has_value:
            return self._value
        else:
            raise ValueError( "No value has been set." )

    def __call__( self ):
        """
        Retrieves the cached value.
        """

        return self.value

    def set_value( self, value, override = False ):
        """
        Sets the cached value with the given value if a value has not been set or the given `override` parameter is `True`, otherwise a `ValueError` is raised.
        """

        if not self.has_value or override:
            self._value = value
            self._has_value = True
        else:
            raise ValueError( "A value has already been cached." )

    def clear( self ):
        """
        Clears the cached value. The return value is a boolean indicating if a value was cleared.
        """

        try:
            result = self.has_value
        except AttributeError:
            result = False
        finally:
            self._has_value = False
            self._value = None

            return result

    def __repr__( self ):
        return "has value: '{}', value: {}".format( self.has_value, self._value )
