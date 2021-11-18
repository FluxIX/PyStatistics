__version__ = r"1.0"

from unittest import TestLoader, TestSuite, TextTestRunner
from . import linear_regression_tests

def run( argv = None, **kwargs ):
    # Adapted from: https://www.internalpointers.com/post/run-painless-test-suites-python-unittest
    test_loader = TestLoader()
    test_suite = TestSuite()

    test_suite.addTests( test_loader.loadTestsFromModule( linear_regression_tests ) )

    runner = TextTestRunner()
    result = runner.run( test_suite )

    return len( result.errors )
