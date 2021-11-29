import unittest
from ...utilities.counter import Counter, FrozenCounter

class CounterTestCase( unittest.TestCase ):
    def assertDataEqual( self, counter_data, target_data, msg = None ):
        return self.assertSequenceEqual( sorted( counter_data ), sorted( target_data ), msg = msg )

class TestCounter( CounterTestCase ):
    def _get_frequencies( self, test_counter, source_counter, operation ):
        test_frequencies = []
        source_frequencies = []

        for key in source_counter:
            test_frequencies.append( test_counter[ key ] )
            source_frequencies.append( operation( source_counter[ key ] ) )

        return test_frequencies, source_frequencies

    def assertCounterFrequenciesEqual( self, test_counter, oracle_counter, operation ):
        self.assertDataEqual( test_counter.keys(), oracle_counter.keys() )
        test_data, oracle_data = self._get_frequencies( test_counter, oracle_counter, operation )
        self.assertDataEqual( test_data, oracle_data )

    def setUp( self ):
        self.counter_data = [ 1, 2, 3, 4, 4, 5, -3, -5, 1, 2, 3, 4, 5, -3 ]
        self.counter = Counter( *self.counter_data )

    def test_keys_inplace_addition_scalar( self ):
        bias = 2
        c = self.counter.copy()
        c.key_values += bias
        self.assertDataEqual( c.keys(), { key + bias for key in self.counter } )

    def test_keys_inplace_subtraction_scalar( self ):
        bias = 2
        c = self.counter.copy()
        c.key_values -= bias
        self.assertDataEqual( c.keys(), { key - bias for key in self.counter } )

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

    def test_keys_abs( self ):
        c = abs( self.counter.key_values )
        self.assertIs( type( c ), Counter )
        self.assertDataEqual( c.keys(), { abs( key ) for key in self.counter } )

    def test_keys_pos( self ):
        c = +self.counter.key_values
        self.assertIs( type( c ), Counter )
        self.assertDataEqual( c.keys(), { +key for key in self.counter } )

    def test_keys_neg( self ):
        c = -self.counter.key_values
        self.assertIs( type( c ), Counter )
        self.assertDataEqual( c.keys(), { -key for key in self.counter } )

    def test_keys_addition_scalar( self ):
        bias = 2
        c = self.counter.key_values + bias
        self.assertDataEqual( c.keys(), { key + bias for key in self.counter } )

    def test_keys_subtraction_scalar( self ):
        bias = 2
        c = self.counter.key_values - bias
        self.assertDataEqual( c.keys(), { key - bias for key in self.counter } )

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
        c = self.counter.key_values // scale
        self.assertDataEqual( c.keys(), { key // scale for key in self.counter } )

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

    def test_frequency_inplace_addition_scalar( self ):
        bias = 2
        c = self.counter.copy()
        c.frequency_values += bias
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x + bias )

    def test_frequency_inplace_subtraction_scalar( self ):
        bias = 2
        c = self.counter.copy()
        c.frequency_values -= bias
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x - bias )

    def test_frequency_inplace_multiplication_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.frequency_values *= scale
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x * scale )

    def test_frequency_inplace_classic_division_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.frequency_values.__idiv__( scale )
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x.__div__( scale ) )

    def test_frequency_inplace_floor_division_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.frequency_values //= scale
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x // scale )

    def test_frequency_inplace_true_division_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.frequency_values.__itruediv__( scale )
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x.__itruediv__( scale ) )

    def test_frequency_inplace_modulo_scalar( self ):
        scale = 2
        c = self.counter.copy()
        c.frequency_values %= scale
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x % scale )

    def test_frequency_inplace_power_scalar( self ):
        power = 2
        c = self.counter.copy()
        c.frequency_values **= power
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x ** power )

    def test_frequency_abs( self ):
        oracle_counter = self.counter.copy()
        for key in oracle_counter:
            oracle_counter[ key ] = -abs( oracle_counter[ key ] )

        c = abs( oracle_counter.frequency_values )
        self.assertIs( type( c ), Counter )
        self.assertCounterFrequenciesEqual( c, oracle_counter, abs )

    def test_frequency_pos( self ):
        c = abs( self.counter.frequency_values )
        self.assertIs( type( c ), Counter )
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x:+x )

    def test_frequency_neg( self ):
        c = abs( self.counter.frequency_values )
        self.assertIs( type( c ), Counter )
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x:-x )

    def test_frequency_addition_scalar( self ):
        bias = 2
        c = self.counter.frequency_values + bias
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x + bias )

    def test_frequency_subtraction_scalar( self ):
        bias = 2
        c = self.counter.frequency_values - bias
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x - bias )

    def test_frequency_multiplication_scalar( self ):
        scale = 2
        c = self.counter.frequency_values * scale
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x * scale )

    def test_frequency_classic_division_scalar( self ):
        scale = 2
        c = self.counter.frequency_values.__div__( scale )
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x.__div__( scale ) )

    def test_frequency_floor_division_scalar( self ):
        scale = 2
        c = self.counter.frequency_values // scale
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x // scale )

    def test_frequency_true_division_scalar( self ):
        scale = 2
        c = self.counter.frequency_values.__truediv__( scale )
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x.__truediv__( scale ) )

    def test_frequency_modulo_scalar( self ):
        scale = 2
        c = self.counter.frequency_values % scale
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x % scale )

    def test_frequency_power_scalar( self ):
        power = 2
        c = self.counter.frequency_values ** power
        self.assertCounterFrequenciesEqual( c, self.counter, lambda x: x ** power )

    def test_counter_inplace_addition( self ):
        pass

    def test_counter_inplace_subtraction( self ):
        pass

    def test_counter_addition( self ):
        pass

    def test_counter_subtraction( self ):
        pass

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
