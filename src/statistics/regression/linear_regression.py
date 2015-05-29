__version__ = r"1.0"

from .. import utilities
from .regression_technique import RegressionTechnique

class LinearRegression( RegressionTechnique ):
    """
    Adapted from: https://en.wikipedia.org/wiki/Simple_regression
    """
    def __init__( self, independent_stat_set, dependent_stat_set, lazy_computation = True ):
        RegressionTechnique.__init__( self, independent_stat_set, dependent_stat_set, lazy_computation )

        self.clear_results()
        if not lazy_computation:
            self.compute_results()

    def clear_results( self ):
        self.__covariance = None
        self.__sum_of_products = None
        self.__slope = None
        self.__intercept = None
        self.__correlation_coefficient = None
        self.__standard_error = None
        self.__standard_error_squared = None
        self.__slope_error = None
        self.__slope_error_squared = None
        self.__intercept_error = None
        self.__intercept_error_squared = None

    def compute_results( self ):
        self.covariance
        self.sum_of_products
        self.slope
        self.intercept
        self.correlation_coefficient
        self.standard_error_squared
        self.standard_error
        self.slope_error_squared
        self.slope_error
        self.intercept_error_squared
        self.intercept_error

    @property
    def covariance( self ):
        if self.__covariance is None:
            self.__covariance = self._compute_covariance( self.independent_stat_set, self.dependent_stat_set )

        return self.__covariance

    @property
    def sum_of_products( self ):
        if self.__sum_of_products is None:
            self.__sum_of_products = self._compute_sum_of_products( self.independent_stat_set, self.dependent_stat_set )

        return self.__sum_of_products

    @property
    def slope( self ):
        if self.__slope is None:
            self.__slope = float( self.covariance ) / self.independent_stat_set.variance

        return self.__slope

    @property
    def intercept( self ):
        if self.__intercept is None:
            self.__intercept = self.dependent_stat_set.mean - self.slope * self.independent_stat_set.mean

        return self.__intercept

    @property
    def correlation_coefficient( self ):
        if self.__correlation_coefficient is None:
            self.__correlation_coefficient = self.slope * self.independent_stat_set.standard_deviation / self.dependent_stat_set.standard_deviation

        return self.__correlation_coefficient

    @property
    def standard_error( self ):
        if self.__standard_error is None:
            import math
            self.__standard_error = math.sqrt( self.standard_error_squared )

        return self.__standard_error

    @property
    def standard_error_squared( self ):
        if self.__standard_error_squared is None:
            dataSize = self.independent_stat_set.size
            slopeTerm = utilities.integer_power( self.slope, 2 ) * ( dataSize * self.independent_stat_set.sum_of_squares - self.independent_stat_set.sum_squared )
            numerator = dataSize * self.dependent_stat_set.sum_of_squares - self.dependent_stat_set.sum_squared - slopeTerm
            denominator = dataSize * ( dataSize - 2 )

            self.__standard_error_squared = float( numerator ) / denominator

        return self.__standard_error_squared

    @property
    def slope_error( self ):
        if self.__slope_error is None:
            import math
            self.__slope_error = math.sqrt( self.slope_error_squared )

        return self.__slope_error

    @property
    def slope_error_squared( self ):
        if self.__slope_error_squared is None:
            dataSize = self.independent_stat_set.size
            numerator = dataSize * self.standard_error_squared
            denominator = dataSize * self.independent_stat_set.sum_of_squares - self.independent_stat_set.sum_squared
            self.__slope_error_squared = float( numerator ) / denominator

        return self.__slope_error_squared

    @property
    def intercept_error( self ):
        if self.__intercept_error is None:
            import math
            self.__intercept_error = math.sqrt( self.intercept_error_squared )

        return self.__intercept_error

    @property
    def intercept_error_squared( self ):
        if self.__intercept_error_squared is None:
            self.__intercept_error_squared = self.slope_error_squared * float( self.independent_stat_set.sum_of_squares ) / self.independent_stat_set.size

        return self.__intercept_error_squared
