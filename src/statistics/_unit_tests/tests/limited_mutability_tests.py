import unittest
from ...utilities.exceptions import NotSupportedException
from ...utilities.limited_mutability import LimitedMutabilityMixin

class TestLimitedMutability( unittest.TestCase ):
    def test_immutable( self ):
        class TestClass( LimitedMutabilityMixin ):
            pass

        test_class = TestClass()

        self.assertTrue( test_class._allow_initial_assignment )
        self.assertSequenceEqual( test_class._mutable_field_names, tuple(), seq_type = tuple )
        self.assertIsNone( test_class._mutability_exception_message )
        self.assertIs( test_class._mutability_exception_type, NotSupportedException )

    def test_mutable_field_names( self ):
        member_name = "_test_member"

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "mutable_field_names" ] = [ member_name ]

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

        test_class = TestClass()

        self.assertSequenceEqual( test_class._mutable_field_names, ( member_name, ), seq_type = tuple )

    def test_exception_message( self ):
        message = "Exception message"

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "exception_message" ] = message

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

        test_class = TestClass()

        self.assertEqual( test_class._mutability_exception_message, message )

    def test_exception_type( self ):
        class TestException( Exception ):
            pass

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "exception_type" ] = TestException

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

        test_class = TestClass()

        self.assertIs( test_class._mutability_exception_type, TestException )

    def test_allow_initial_assignment( self ):
        class TestClassA( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "allow_initial_assignment" ] = False

                return super( TestClassA, cls ).__new__( cls, *args, **kwargs )
        class TestClassB( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "allow_initial_assignment" ] = None

                return super( TestClassB, cls ).__new__( cls, *args, **kwargs )
        class TestClassC( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "allow_initial_assignment" ] = True

                return super( TestClassC, cls ).__new__( cls, *args, **kwargs )

        test_class_a = TestClassA()
        test_class_b = TestClassB()
        test_class_c = TestClassC()

        self.assertFalse( test_class_a._allow_initial_assignment )
        self.assertTrue( test_class_b._allow_initial_assignment )
        self.assertTrue( test_class_c._allow_initial_assignment )

    def test_member_initialization( self ):
        member_name = "_test_member"

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                def initialize( obj, **kwargs ):
                    setattr( obj, member_name, 10 )

                kwargs[ "mutable_field_names" ] = [ member_name ]
                kwargs[ "initialization" ] = initialize

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

        test_class = TestClass()

        self.assertEqual( getattr( test_class, member_name ), 10 )

    def test_validate_mutability_without_message( self ):
        class TestException( Exception ):
            pass

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "exception_type" ] = TestException

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

            def __init__( self ):
                self._immutable_member = 1

        self.assertRaises( TestException, TestClass )

    def test_validate_mutability_with_message( self ):
        message = "Exception message"

        class TestException( Exception ):
            pass

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):
                kwargs[ "exception_type" ] = TestException
                kwargs[ "exception_message" ] = message

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

            def __init__( self ):
                self._immutable_member = 1

        try:
            TestClass()
        except TestException as e:
            self.assertEqual( e.message, message )
        else:
            raise self.failureException( "Unable to test exception message; no '{}' raised".format( TestException.__name__ ) )

    def test_set_value( self ):
        member_name = "_test_member"

        class TestClass( LimitedMutabilityMixin ):
            def __new__( cls, *args, **kwargs ):

                kwargs[ "mutable_field_names" ] = [ member_name ]

                return super( TestClass, cls ).__new__( cls, *args, **kwargs )

        test_class = TestClass()
        setattr( test_class, member_name, 10 )

        self.assertEqual( getattr( test_class, member_name ), 10 )

if __name__ == "__main__":
    unittest.main()
