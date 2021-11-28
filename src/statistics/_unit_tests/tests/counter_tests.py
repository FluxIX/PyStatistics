import unittest
from ...utilities.counter import Counter, FrozenCounter

class CounterTestCase( unittest.TestCase ):
    def assertDataEqual( self, counter_data, target_data, msg = None ):
        return self.assertSequenceEqual( sorted( counter_data ), sorted( target_data ), msg = msg )

class TestCounter( CounterTestCase ):
    def setUp( self ):
        self.counter_data = [ 1, 2, 3, 4, 4, 5, -3, -5, 1, 2, 3, 4, 5, -3 ]
        self.counter = Counter( *self.counter_data )

    def test_keys_abs( self ):
        c = abs( self.counter.key_values )
        self.assertIs( type( c ), Counter )
        self.assertDataEqual( c.keys(), { abs( key ) for key in self.counter_data } )

    def test_keys_pos( self ):
        c = +self.counter.key_values
        self.assertIs( type( c ), Counter )
        self.assertDataEqual( c.keys(), { +key for key in self.counter_data } )

    def test_keys_neg( self ):
        c = -self.counter.key_values
        self.assertIs( type( c ), Counter )
        self.assertDataEqual( c.keys(), { -key for key in self.counter_data } )

    def test_keys_inplace_addition_scalar( self ):
        bias = 2
        c = self.counter.copy()
        c.key_values += bias
        self.assertDataEqual( c.keys(), { key + bias for key in self.counter } )

    def test_keys_inplace_addition_counter( self ):
        pass

    def test_keys_inplace_subtraction_scalar( self ):
        bias = 2
        c = self.counter.copy()
        c.key_values -= bias
        self.assertDataEqual( c.keys(), { key - bias for key in self.counter } )

    def test_keys_inplace_subtraction_counter( self ):
        pass

    def test_keys_inplace_multiplication_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.key_values *= scale
        self.assertDataEqual( c.keys(), { key * scale for key in self.counter } )

    def test_keys_inplace_classic_division_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.key_values.__idiv__( scale )
        self.assertDataEqual( c.keys(), { key.__div__( scale ) for key in self.counter } )

    def test_keys_inplace_floor_division_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.key_values //= scale
        self.assertDataEqual( c.keys(), { key.__floordiv__( scale ) for key in self.counter } )

    def test_keys_inplace_true_division_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.key_values.__itruediv__( scale )
        self.assertDataEqual( c.keys(), { key.__truediv__( scale ) for key in self.counter } )

    def test_keys_inplace_modulo_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.key_values %= scale
        self.assertDataEqual( c.keys(), { key % scale for key in self.counter } )

    def test_keys_inplace_power_scalar( self ):
        power = 2
        c = self.counter.copy()
        c.key_values **= power
        self.assertDataEqual( c.keys(), { key ** power for key in self.counter } )

    def test_keys_addition_scalar( self ):
        bias = 2
        c = self.counter.key_values + bias
        self.assertDataEqual( c.keys(), { key + bias for key in self.counter } )

    def test_keys_addition_counter( self ):
        pass

    def test_keys_subtraction_scalar( self ):
        bias = 2
        c = self.counter.key_values - bias
        self.assertDataEqual( c.keys(), { key - bias for key in self.counter } )

    def test_keys_subtraction_counter( self ):
        pass

    def test_keys_multiplication_scalar( self ):
        scale = 2
        c = self.counter.key_values * scale
        self.assertDataEqual( c.keys(), { key * scale for key in self.counter } )

    def test_keys_classic_division_scalar( self ):
        scale = 2
        c = self.counter.key_values.__div__( scale )
        self.assertDataEqual( c.keys(), { key.__div__( scale ) for key in self.counter } )

    def test_keys_floor_division_scalar( self ):
        scale = 2
        c = self.counter.key_values.__floordiv__( scale )
        self.assertDataEqual( c.keys(), { key.__floordiv__( scale ) for key in self.counter } )

    def test_keys_true_division_scalar( self ):
        scale = 2
        c = self.counter.key_values.__truediv__( scale )
        self.assertDataEqual( c.keys(), { key.__truediv__( scale ) for key in self.counter } )

    def test_keys_modulo_scalar( self ):
        scale = 2
        c = self.counter.key_values % scale
        self.assertDataEqual( c.keys(), { key % scale for key in self.counter } )

    def test_keys_power_scalar( self ):
        power = 2
        c = self.counter.key_values ** power
        self.assertDataEqual( c.keys(), { key ** power for key in self.counter } )

    def test_to_tuple( self ):
        t = self.counter.to_tuple()
        self.assertIs( type( t ), tuple )
        self.assertDataEqual( t, self.counter_data )

    def test_get_immutable( self ):
        frozen_counter = self.counter.get_immutable()
        self.assertIs( type( frozen_counter ), FrozenCounter )
        self.assertDataEqual( frozen_counter.to_tuple(), self.counter.to_tuple() )

class TestFrozenCounter( CounterTestCase ):
    def setUp( self ):
        self.counter_data = [ 1, 2, 3, 4, 4, 5, -3, -5, 1, 2, 3, 4, 5, -3 ]
        self.counter = FrozenCounter( *self.counter_data )

    def test_get_mutable( self ):
        counter = self.counter.get_mutable()
        self.assertIs( type( counter ), Counter )
        self.assertDataEqual( counter.to_tuple(), self.counter.to_tuple() )

if __name__ == "__main__":
    unittest.main()
