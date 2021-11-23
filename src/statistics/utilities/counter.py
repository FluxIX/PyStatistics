__version__ = r"1.0"

from collections import Counter as SimpleCounter
from .cached_value import CachedValue
from .exceptions import NotSupportedException
from .hashing import get_hash
from .limited_mutability import LimitedMutabilityMixin

class Counter( SimpleCounter ):
    """
    Represents a mutable collection of items with their associated counts.
    """

    def __init__( self, *args, **kwargs ):
        if len( args ) == 1:
            container = args[ 0 ]
            if isinstance( container, ( dict, SimpleCounter ) ):
                args = container.to_tuple()
            elif isinstance( container, ( list, tuple ) ):
                args = tuple( container )
            else:
                raise ValueError( "Unsupported item container for the Counter: {}".format( str( type( container ) ) ) )

        super( Counter, self ).__init__( args, **kwargs )

    def _transform_values( self, transform ):
        for key in self:
            self[ key ] = transform( self[ key ] )

    def _apply_scalar_operation( self, other, operation, label ):
        try:
            o = float( other )
        except:
            raise ValueError( "Invalid type to apply {} operation to counter values: value must a scalar.".format( label ) )
        else:
            self._transform_values( lambda x: operation( x, o ) )

    def __abs__( self ):
        self._transform_values( lambda x: abs( x ) )
        return self

    def __iadd__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a + b, "addition" )
        return self

    def __imul__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a * b, "multiplication" )
        return self

    def __idiv__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a / b, "classic division" )
        return self

    def __ifloordiv__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a // b, "floor division" )
        return self

    def __ipow__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a ** b, "exponentiation" )
        return self

    def __isub__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a - b, "subtraction" )
        return self

    def __itruediv__( self, other ):
        self._apply_scalar_operation( other, lambda a, b: a / b, "true division" )
        return self

    def __add__( self, other ):
        result = self.copy()
        result += other
        return result

    def __mul__( self, other ):
        result = self.copy()
        result *= other
        return result

    def __div__( self, other ):
        result = self.copy()
        result /= other
        return result

    def __floordiv__( self, other ):
        result = self.copy()
        result //= other
        return result

    def __pow__( self, other ):
        result = self.copy()
        result **= other
        return result

    def __sub__( self, other ):
        result = self.copy()
        result -= other
        return result

    def __truediv__( self, other ):
        result = self.copy()
        result /= other
        return result

    def least_common( self, n = None ):
        """
        List the n least common elements and their counts from the most common to the least.  If n is None, then list all element counts.
        """

        lc = reversed( self.most_common() )

        if n is not None:
            result = lc[: n ]
        else:
            result = lc

        return result

    def get_most_common_frequencies( self, quantity = 1 ):
        """
        Gets the given quantity's most common frequencies.
        """

        if quantity <= 0:
            raise ValueError( "Quantity ({}) must be positive.".format( quantity ) )
        else:
            return tuple( sorted( set( self.values() ), reverse = True )[: quantity ] )

    def get_least_common_frequencies( self, quantity = 1 ):
        """
        Gets the given quantity's least common frequencies.
        """

        if quantity <= 0:
            raise ValueError( "Quantity ({}) must be positive.".format( quantity ) )
        else:
            return tuple( sorted( set( self.values() ), reverse = False )[: quantity ] )

    def get_values_with_frequencies( self, frequency_predicate ):
        """
        Gets the values with frequencies which conform with the given predicate.
        """

        return frozenset( [ key for key in self if frequency_predicate( self[ key ] ) ] )

    def to_tuple( self ):
        """
        Gets a tuple which contains all of the values found in the counter with the correct frequencies.
        """

        container = []

        for key in self:
            for _ in range( self[ key ] ):
                container.append( key )

        result = tuple( container )

        return result

    def get_immutable( self ):
        """
        Gets an immutable copy of the current counter,
        """

        return FrozenCounter( self )

    def __repr__( self ):
        return super( SimpleCounter, self ).__repr__()

class FrozenCounter( LimitedMutabilityMixin, Counter ):
    """
    Represents an immutable collection of items with their associated counts.
    """

    def __new__( cls, *args, **kwargs ):
        mutable_field_names = [ "_initialized", "_hash", "_tuple_view" ]

        keyword_args = kwargs.copy()
        if "mutable_field_names" in keyword_args:
            mutable_field_names.extend( keyword_args[ "mutable_field_names" ] )

        keyword_args[ "mutable_field_names" ] = mutable_field_names

        def initialize_members( obj, **kwargs ):
            obj._initialized = False

        keyword_args[ "initialization" ] = initialize_members

        result = super( FrozenCounter, cls ).__new__( cls, *args, **keyword_args )

        return result

    def __init__( self, *args, **kwargs ):
        self._hash = CachedValue()
        self._tuple_view = CachedValue()

        self._super().__init__( *args, **kwargs )

        self._initialized = True

    def _super( self ):
        return super( FrozenCounter, self )

    def _invoke_then_freeze( self, call ):
        return self.__class__( call() )

    def subtract( self, *args, **kwargs ):
        raise NotSupportedException( "Cannot alter item values." )

    def update( self, *args, **kwargs ):
        # The SimpleCounter uses the `update` method during initialization.
        if self._validate_mutability( "_initialized", lambda: not self._initialized, **kwargs ):
            return self._super().update( *args, **kwargs )

    def __ior__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __iand__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __delattr__( self, name ):
        raise NotSupportedException( "Cannot remove items." )

    def __setattr__( self, name, value ):
        if self._validate_mutability( name, lambda: not self._initialized ):
            super( Counter, self ).__setattr__( name, value )

    def __pos__( self ):
        return self._invoke_then_freeze( lambda: self._super().__pos__() )

    def __neg__( self ):
        return self._invoke_then_freeze( lambda: self._super().__neg__() )

    def __or__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__or__( other ) )

    def __and__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__and__( other ) )

    def __abs__( self ):
        return self._invoke_then_freeze( lambda: self._super().__abs__() )

    def __iadd__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __imul__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __idiv__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __ifloordiv__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __ipow__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __isub__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __itruediv__( self, other ):
        raise NotSupportedException( "Cannot alter item values." )

    def __add__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__add__( other ) )

    def __mul__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__mul__( other ) )

    def __div__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__div__( other ) )

    def __floordiv__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__floordiv__( other ) )

    def __pow__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__pow__( other ) )

    def __sub__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__sub__( other ) )

    def __truediv__( self, other ):
        return self._invoke_then_freeze( lambda: self._super().__truediv__( other ) )

    def clear( self ):
        raise NotSupportedException( "Cannot remove items." )

    def pop( self, key, default_value = None ):
        raise NotSupportedException( "Cannot remove items." )

    def popitem( self ):
        raise NotSupportedException( "Cannot remove items." )

    def setdefault( self, key, default_value = None ):
        """
        Retrieves the value associated with the given `key`. If the `key` is not present, the `default_value` is associated with the given `key` and returned.
        """

        if key in self:
            return self[ key ]
        else:
            # If the counter were mutable, we would set the key's value using the default value and then return, but since the container is immutable, we instead raise an exception.
            raise NotSupportedException( "Cannot alter items." )

    def get_mutable( self ):
        """
        Gets a mutable copy of the current counter.
        """

        return Counter( self )

    def to_tuple( self ):
        """
        Gets a tuple which contains all of the values found in the counter with the correct frequencies.
        """

        if not self._tuple_view.has_value:
            self._tuple_view.set_value( self._super().to_tuple() )

        return self._tuple_view.value

    def __hash__( self ):
        if not self._hash.has_value:
            self._hash.set_value( get_hash( self.__class___.__name__, *self.viewitems() ) )

        return self._hash.value
