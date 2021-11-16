__version__ = r"1.0"

class RegressionTechnique( object ):
    def __init__( self, independent_stat_set, dependent_stat_set, **kwargs ):
        if independent_stat_set.size != dependent_stat_set.size:
            raise ValueError( "Data set sizes are not equal." )
        else:
            self._independent_stat_set = independent_stat_set
            self._dependent_stat_set = dependent_stat_set

        lazy_computation = bool( kwargs.get( "lazy_computation", True ) )

        self.clear_results()
        if not lazy_computation:
            self.compute_results()

    def clear_results( self, **kwargs ):
        return self._clear_results( **kwargs )

    def compute_results( self, **kwargs ):
        return self._compute_results( **kwargs )

    def _clear_results( self, **kwargs ):
        raise NotImplementedError( "Child must implement." )

    def _compute_results( self ):
        raise NotImplementedError( "Child must implement." )

    @property
    def independent_stat_set( self ):
        return self._independent_stat_set

    @property
    def dependent_stat_set( self ):
        return self._dependent_stat_set

    def _compute_sum_of_squares( self, stat_set ):
        return ( stat_set ** 2 ).sum

    def _compute_sum_of_products( self, stat_set_a, stat_set_b ):
        if stat_set_a.size != stat_set_b.size:
            raise ValueError( "Data set sizes are not equal." )
        else:
            return ( stat_set_a * stat_set_b ).sum
