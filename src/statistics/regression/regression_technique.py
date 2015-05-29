__version__ = r"1.0"

class RegressionTechnique( object ):
    def __init__( self, independent_stat_set, dependent_stat_set, lazy_computation = True ):
        if independent_stat_set.size != dependent_stat_set.size:
            raise ValueError( "Data set sizes are not equal." )
        else:
            self.__independent_stat_set = independent_stat_set
            self.__dependent_stat_set = dependent_stat_set

    @property
    def independent_stat_set( self ):
        return self.__independent_stat_set

    @property
    def dependent_stat_set( self ):
        return self.__dependent_stat_set

    def _compute_covariance( self, independent_stat_set, dependent_stat_set ):
        if independent_stat_set.size != dependent_stat_set.size:
            raise ValueError( "Data set sizes are not equal." )
        else:
            dataSize = independent_stat_set.size

            result = 0

            processed = 0
            while processed < dataSize:
                a = independent_stat_set.data[ processed ] - independent_stat_set.mean
                b = dependent_stat_set.data[ processed ] - dependent_stat_set.mean
                result += float( a * b ) / dataSize
                processed += 1

            return result

    def _compute_sum_of_products( self, stat_set_a, stat_set_b ):
        if stat_set_a.size != stat_set_b.size:
            raise ValueError( "Data set sizes are not equal." )
        else:
            result = 0

            processed = 0
            while processed < stat_set_a.size:
                result += stat_set_a.data[ processed ] * stat_set_b.data[ processed ]
                processed += 1

            return result
