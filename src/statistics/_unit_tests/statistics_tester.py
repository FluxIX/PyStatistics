__version__ = r"1.0"

from unittest import TestLoader, TestSuite, TextTestRunner
from .tests import linear_regression_tests, statistics_set_tests, error_tests, counter_tests, mode_tests, frequency_tests

def run( argv = None, **kwargs ):
    # Adapted from: https://www.internalpointers.com/post/run-painless-test-suites-python-unittest
    test_loader = TestLoader()
    test_suite = TestSuite()

    test_modules = [ error_tests, counter_tests, frequency_tests, mode_tests, statistics_set_tests, linear_regression_tests ]

    for module in test_modules:
        test_suite.addTests( test_loader.loadTestsFromModule( module ) )

    runner = TextTestRunner()
    result = runner.run( test_suite )

    return len( result.errors )
