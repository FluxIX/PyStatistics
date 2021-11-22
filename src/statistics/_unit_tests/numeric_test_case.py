import math
import unittest
from ..calculations.error import compute_relative_difference, compute_relative_error
from ..utilities.math import floating_point_equal, floating_point_less, floating_point_less_equal, floating_point_greater, floating_point_greater_equal

class NumericTestCase( unittest.TestCase ):
    # Note: this test case class uses parameters for the tolerances. This code structure is one way to do pass the parameters; another approach is described at: https://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases.

    def __init__( self, method_name = "runTest", **kwargs ):
        super( NumericTestCase, self ).__init__( method_name )

        self.value_tolerance = self._get_tolerance( "value_tolerance", 0.0, "Value", **kwargs )
        self.percent_tolerance = self._get_tolerance( "percent_tolerance", 0.0, "Percent", **kwargs )

    def _get_tolerance( self, key, default_value, label, **kwargs ):
        tolerance = kwargs.get( key, None )
        if tolerance is None:
            tolerance = default_value

        tolerance = float( tolerance )

        if tolerance < 0.0:
            raise ValueError( "{} tolerance ({}) must be non-negative.".format( label, tolerance ) )
        else:
            return tolerance

    def _compute_difference( self, actual_value, expected_value ):
        difference = math.fabs( actual_value - expected_value )
        percent_difference = compute_relative_difference( actual_value, expected_value, scale = 100 )
        percent_error = compute_relative_error( actual_value, expected_value, scale = 100 )

        return difference, percent_difference, percent_error

    def _assertFloatingPointValueOperation( self, operation, actual_value, expected_value, **kwargs ):
        msg = kwargs.get( "msg", None )

        tolerance = self._get_tolerance( "tolerance", self.value_tolerance, "Value", **kwargs )

        return self.assertTrue( operation( actual_value, expected_value, tolerance ), msg )

    def assertFloatingPointPercentEqual( self, actual_value, expected_value, **kwargs ):
        msg = kwargs.get( "msg", None )

        tolerance = self._get_tolerance( "tolerance", self.percent_tolerance, "Value", **kwargs )

        value_difference, percent_difference, percent_error = self._compute_difference( actual_value, expected_value )

        return self.assertTrue( floating_point_less_equal( percent_difference, tolerance ), msg )

    def assertFloatingPointPercentNotEqual( self, actual_value, expected_value, **kwargs ):
        return not self.assertFloatingPointPercentEqual( actual_value, expected_value, **kwargs )

    def assertFloatingPointValueEqual( self, actual_value, expected_value, **kwargs ):
        return self._assertFloatingPointValueOperation( floating_point_equal, actual_value, expected_value, **kwargs )

    def assertFloatingPointValueNotEqual( self, actual_value, expected_value, **kwargs ):
        return not self.assertFloatingPointValueEqual( actual_value, expected_value, **kwargs )

    def assertFloatingPointValueLess( self, actual_value, expected_value, **kwargs ):
        return self._assertFloatingPointValueOperation( floating_point_less, actual_value, expected_value, **kwargs )

    def assertFloatingPointValueLessEqual( self, actual_value, expected_value, **kwargs ):
        return self._assertFloatingPointValueOperation( floating_point_less_equal, actual_value, expected_value, **kwargs )

    def assertFloatingPointValueGreater( self, actual_value, expected_value, **kwargs ):
        return self._assertFloatingPointValueOperation( floating_point_greater, actual_value, expected_value, **kwargs )

    def assertFloatingPointValueGreaterEqual( self, actual_value, expected_value, **kwargs ):
        return self._assertFloatingPointValueOperation( floating_point_greater_equal, actual_value, expected_value, **kwargs )
