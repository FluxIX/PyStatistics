__version__ = r"1.0"

from collections import Counter as SimpleCounter
from .cached_value import CachedValue
from .exceptions import NotSupportedException
from .hashing import get_hash
from .limited_mutability import LimitedMutabilityMixin

class CounterManipulator( object ):
    def __init__( self, counter, **kwargs ):
        self._counter = counter

    @property
    def counter( self ):
        """
        The counter whose values are to the manipulated.
        """

        return self._counter

    @property
    def values( self ):
        """
        Gets the values to be manipulated.
        """

        return self._get_values()

    def _get_values( self ):
        raise NotImplementedError( "Child must implement." )

    def _unary_value_transform( self, data, transform ):
        return [ transform( value ) for value in data ]

    def _get_current_manipulator( self, counter ):
        raise NotImplementedError( "Child must implement." )

class MutableCounterManipulator( CounterManipulator ):
    def _classic_division( self, a, b ):
        # TODO: have a mechanism to dispatch to the logical a.__div__ operation.

        # return a / b
        return a.__div__( b )

    def _floor_division( self, a, b ):
        # TODO: have a mechanism to dispatch to the logical a.__floordiv__ operation.
        return a // b

    def _true_division( self, a, b ):
        # TODO: have a mechanism to dispatch to the logical a.__truediv__ operation.

        # return a / b
        return a.__truediv__( b )

    def _transform_values( self, transform ):
        raise NotImplementedError( "Child must implement." )

    def _apply_scalar_operation( self, other, operation, label ):
        self._transform_values( lambda x: operation( x, other ) )

    def __iadd__( self, other ):
        """
        In-place scalar addition with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: a + b, "addition" )
        return self

    def __imul__( self, other ):
        """
        In-place scalar multiplication with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: a * b, "multiplication" )
        return self

    def __idiv__( self, other ):
        """
        In-place scalar classic addition with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: self._classic_division( a, b ), "classic division" )
        return self

    def __ifloordiv__( self, other ):
        """
        In-place scalar floor division with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: self._floor_division( a, b ), "floor division" )
        return self

    def __imod__( self, other ):
        """
        In-place scalar modulo with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: a % b, "modulo" )
        return self

    def __ipow__( self, other ):
        """
        In-place scalar exponentiation with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: a ** b, "exponentiation" )
        return self

    def __isub__( self, other ):
        """
        In-place scalar subtraction with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: a - b, "subtraction" )
        return self

    def __itruediv__( self, other ):
        """
        In-place scalar true division with the keys.
        """

        self._apply_scalar_operation( other, lambda a, b: self._true_division( a, b ), "true division" )
        return self

    def __add__( self, other ):
        """
        Scalar addition with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__iadd__( other )
        return result

    def __radd__( self, other ):
        return self.__add__( other )

    def __mul__( self, other ):
        """
        Scalar multiplication with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__imul__( other )
        return result

    def __rmul__( self, other ):
        return self.__mul__( other )

    def __div__( self, other ):
        """
        Scalar classic division with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__idiv__( other )
        return result

    def __floordiv__( self, other ):
        """
        Scalar floor division with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__ifloordiv__( other )
        return result

    def __mod__( self, other ):
        """
        Scalar modulo with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__imod__( other )
        return result

    def __pow__( self, other ):
        """
        Scalar exponentiation with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__ipow__( other )
        return result

    def __sub__( self, other ):
        """
        Scalar subtraction with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__isub__( other )
        return result

    def __truediv__( self, other ):
        """
        Scalar true division with the keys with the result going to a new Counter.
        """

        result = self.counter.copy()
        self._get_current_manipulator( result ).__itruediv__( other )
        return result

    def _get_unary_transformed_values( self, transform ):
        raise NotImplementedError( "Child must implement." )

    def _build_new_counter_with_data( self, data ):
        raise NotImplementedError( "Child must implement." )

    def __abs__( self ):
        """
        Returns a new counter with the absolute values of the counter values.
        """

        return self._build_new_counter_with_data( self._get_unary_transformed_values( abs ) )

    def __pos__( self ):
        """
        Returns a new counter with the positive values of the counter values.
        """

        return self._build_new_counter_with_data( self._get_unary_transformed_values( lambda x:+x ) )

    def __neg__( self ):
        """
        Returns a new counter with the negated values of the counter values.
        """

        return self._build_new_counter_with_data( self._get_unary_transformed_values( lambda x:-x ) )

class CounterKeyManipulator( MutableCounterManipulator ):
    def _get_current_manipulator( self, counter ):
        return counter.key_values

    def _transform_values( self, transform ):
        remapping = {}
        for key in self.counter:
            new_key = transform( key )

            if new_key not in remapping:
                remapping[ new_key ] = 0

            remapping[ new_key ] += self.counter[ key ]

        self.counter.clear()
        self.counter.update( remapping )

    def _get_unary_transformed_values( self, transform ):
        return self._unary_value_transform( self.counter.to_tuple(), transform )

    def _build_new_counter_with_data( self, data ):
        return self.counter.__class__( *data )

    def _get_values( self ):
        return self.counter.keys()

class CounterFrequencyManipulator( MutableCounterManipulator ):
    def _get_current_manipulator( self, counter ):
        return counter.frequency_values

    def _transform_values( self, transform ):
        for key in self.counter:
            self.counter[ key ] = transform( self.counter[ key ] )

    def _get_unary_transformed_values( self, transform ):
        return { key: transform( self.counter[ key ] ) for key in self.counter }

    def _build_new_counter_with_data( self, data ):
        return self.counter.__class__( data )

    def _get_values( self ):
        return self.counter.values()

class Counter( SimpleCounter ):
    """
    Represents a mutable collection of items with their associated counts.
    """

    def __init__( self, *args, **kwargs ):
        if len( args ) == 1:
            container = args[ 0 ]
            if isinstance( container, dict ):
                args = container
            elif isinstance( container, ( list, tuple ) ):
                args = tuple( container )
            else:
                raise ValueError( "Unsupported item container for the Counter: {}".format( str( type( container ) ) ) )

        self._key_values = CounterKeyManipulator( self )
        self._frequency_values = CounterFrequencyManipulator( self )

        super( Counter, self ).__init__( args, **kwargs )

    @property
    def key_values( self ):
        """
        Provides a means to manipulate the counter's key values.
        """

        return self._key_values

    @property
    def frequency_values( self ):
        """
        Provides a means to manipulate the counter's frequency values.
        """

        return self._frequency_values

    def __del__( self ):
        del self._key_values
        del self._frequency_values

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

    @classmethod
    def convert_to_tuple( cls, counter ):
        """
        Gets a tuple which contains all of the values found in the given counter with the frequencies as they are represented in the counter.
        """

        container = []

        for key in counter:
            for _ in range( counter[ key ] ):
                container.append( key )

        result = tuple( container )

        return result

    def to_tuple( self ):
        """
        Gets a tuple which contains all of the values found in the counter with the frequencies as they are represented in the counter.
        """

        return self.convert_to_tuple( self )

    def get_immutable( self ):
        """
        Gets an immutable copy of the current counter,
        """

        return FrozenCounter( self )

    def __xor__( self, other ):
        """
        Gets a new Counter containing the items in either this Counter or the given Counter, but not both.
        """

        if other is None:
            raise ValueError( "`other` parameter cannot be None." )
        elif not isinstance( other, dict ):
            raise ValueError( "XOR operation requires another `dict` (or child thereof) as a parameter." )
        else:
            data = {}
            for reference_counter, other_counter in ( self, other ), ( other, self ):
                for key in reference_counter:
                    if key not in other_counter:
                        data[ key ] = reference_counter[ key ]

            return self.__class__( data )

    def __rxor__( self, other ):
        return self.__xor__( other )

    def unique_from( self, *others, **kwargs ):
        """
        Gets a new Counter containing the keys found in this Counter, but not the given items; the values are from this Counter.
        """

        other = set( others )
        keys = [ key for key in self.counter if key not in other ]
        return self.__class__( { self[ key ] for key in keys } )

    def __repr__( self ):
        return super( SimpleCounter, self ).__repr__()

class FrozenCounter( LimitedMutabilityMixin, Counter ):
    """
    Represents an immutable collection of items with their associated counts.
    """

    def __new__( cls, *args, **kwargs ):
        mutable_field_names = [ "_initialized", "_hash", "_tuple_view", "_key_values", "_frequency_values" ]

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
