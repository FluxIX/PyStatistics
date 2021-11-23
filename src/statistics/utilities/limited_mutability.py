from .exceptions import NotSupportedException

class LimitedMutabilityMixin( object ):
    """
    Prevents the values of members from changing unless the field names are explicitly allowed to change.
    """

    def __new__( cls, *args, **kwargs ):
        """
        Keyword Arguments:
        `allow_initial_assignment`: if `True` the value can be set if the parameter has a mutable field name and didn't exist regardless of other criteria, otherwise the existence check is ignored. Parameter values defaults to `True`.
        `mutable_field_names`: iterable of the member field names to grant mutability to.
        `exception_message`: exception message to be raised if mutability validation fails.
        `exception_type`: exception type raised if mutability fails.
        `initialization`: initialization callable which takes a single positional parameter, the target instance, and the keyword argument dictionary.
        """

        allow_initial_assignment = kwargs.get( "allow_initial_assignment", None )
        if allow_initial_assignment is None:
            allow_initial_assignment = True
        else:
            allow_initial_assignment = bool( allow_initial_assignment )

        mutable_field_names = kwargs.get( "mutable_field_names", None )
        if mutable_field_names is None:
            mutable_field_names = []

        exception_message = kwargs.get( "exception_message", None )

        exception_type = kwargs.get( "exception_type", None )
        if exception_type is None:
            exception_type = NotSupportedException

        initialization = kwargs.get( "initialization", None )

        result = super( LimitedMutabilityMixin, cls ).__new__( cls, *args )

        result._allow_initial_assignment = allow_initial_assignment
        result._mutable_field_names = tuple( mutable_field_names )
        result._mutability_exception_message = exception_message
        result._mutability_exception_type = exception_type

        if initialization is not None:
            initialization( result, **kwargs )

        return result

    def __setattr__( self, name, value ):
        if self._validate_mutability( name ):
            super( LimitedMutabilityMixin, self ).__setattr__( name, value )

    def _raise_mutability_exception( self ):
        """
        Raises an exception to indicate the mutability validation failed.
        """

        if self._mutability_exception_message is not None:
            exception = self._mutability_exception_type( self._mutability_exception_message )
        else:
            exception = self._mutability_exception_type()

        raise exception

    def _validate_mutability( self, field_name, operation = None, **kwargs ):
        """
        Validates if the field name can be modified. If the given operation is not None, then the operation must also return `True` for the field name to validate.
        
        `operation`: callable predicate with no parameters used to determine if the field name can be modified. If the predicate is `None`, the operation does not factor into validation.
        """

        is_internal_name = field_name in ( "_allow_initial_assignment", "_mutable_field_names", "_mutability_exception_message", "_mutability_exception_type" )

        if is_internal_name: # internal names are unconditionally mutable
            result = True
        else:
            name_allowed = field_name in self._mutable_field_names
            if name_allowed and ( ( self._allow_initial_assignment and not hasattr( self, field_name ) ) or ( operation is None or operation() ) ):
                result = True
            else:
                self._raise_mutability_exception()

        return result
