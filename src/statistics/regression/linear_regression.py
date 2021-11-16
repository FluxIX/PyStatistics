__version__ = r"1.0"

import math
from ..utilities.math import integer_power
from ..calculations import regression
from .regression_technique import RegressionTechnique

class LinearRegression( RegressionTechnique ):
    """
    Computes the linear regression between one independent and one dependent statistic set.

    Adapted from: https://en.wikipedia.org/wiki/Simple_regression
    """
    def __init__( self, independent_stat_set, dependent_stat_set, **kwargs ):
        super( LinearRegression, self ).__init__( independent_stat_set, dependent_stat_set, **kwargs )

    def _clear_results( self, **kwargs ):
        self._covariance = None
        self._sum_of_products = None
        self._slope = None
        self._intercept = None
        self._correlation_coefficient = None
        self._standard_error = None
        self._standard_error_squared = None
        self._slope_error = None
        self._slope_error_squared = None
        self._intercept_error = None
        self._intercept_error_squared = None

    def _compute_results( self, **kwargs ):
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
        """
        Computes the covariance of the statistic sets used in the regression.
        """

        if self._covariance is None:
            self._covariance = regression.calculate_covariance( self.independent_stat_set, self.dependent_stat_set )

        return self._covariance

    @property
    def sum_of_products( self ):
        """
        Computes the sum of the element-wise products of the statistic sets used in the regression.
        """

        if self._sum_of_products is None:
            self._sum_of_products = self._compute_sum_of_products( self.independent_stat_set, self.dependent_stat_set )

        return self._sum_of_products

    @property
    def slope( self ):
        """
        Computes the slope of the line of regression.
        """

        if self._slope is None:
            self._slope = float( self.covariance ) / self.independent_stat_set.variance

        return self._slope

    @property
    def intercept( self ):
        """
        Computes the intercept of the line of regression.
        """

        if self._intercept is None:
            self._intercept = self.dependent_stat_set.arithmetic_mean - self.slope * self.independent_stat_set.arithmetic_mean

        return self._intercept

    @property
    def correlation_coefficient( self ):
        """
        Computes the correlation coefficient of the regression.
        """

        if self._correlation_coefficient is None:
            self._correlation_coefficient = self.slope * self.independent_stat_set.standard_deviation / self.dependent_stat_set.standard_deviation

        return self._correlation_coefficient

    @property
    def coefficient_of_determination( self ):
        """
        Computes the coefficient of determination of the regression.
        """

        if self._coefficient_of_determination is None:
            self._coefficient_of_determination = integer_power( self.correlation_coefficient, 2 )

        return self._coefficient_of_determination

    @property
    def standard_error( self ):
        """
        Computes the standard error of the regression.
        """

        if self._standard_error is None:
            self._standard_error = math.sqrt( self.standard_error_squared )

        return self._standard_error

    @property
    def standard_error_squared( self ):
        if self._standard_error_squared is None:
            dataSize = self.independent_stat_set.size
            slopeTerm = integer_power( self.slope, 2 ) * ( dataSize * ( self.independent_stat_set ** 2 ).sum - integer_power( self.independent_stat_set.sum, 2 ) )
            numerator = dataSize * self._compute_sum_of_squares( self.dependent_stat_set ) - integer_power( self.dependent_stat_set.sum, 2 ) - slopeTerm
            denominator = dataSize * ( dataSize - 2 )

            self._standard_error_squared = float( numerator ) / denominator

        return self._standard_error_squared

    @property
    def slope_error( self ):
        if self._slope_error is None:
            self._slope_error = math.sqrt( self.slope_error_squared )

        return self._slope_error

    @property
    def slope_error_squared( self ):
        if self._slope_error_squared is None:
            dataSize = self.independent_stat_set.size
            numerator = dataSize * self.standard_error_squared
            denominator = dataSize * self._compute_sum_of_squares( self.independent_stat_set ) - integer_power( self.independent_stat_set.sum, 2 )
            self._slope_error_squared = float( numerator ) / denominator

        return self._slope_error_squared

    @property
    def intercept_error( self ):
        if self._intercept_error is None:
            self._intercept_error = math.sqrt( self.intercept_error_squared )

        return self._intercept_error

    @property
    def intercept_error_squared( self ):
        if self._intercept_error_squared is None:
            self._intercept_error_squared = self.slope_error_squared * float( self._compute_sum_of_squares( self.independent_stat_set ) ) / self.independent_stat_set.size

        return self._intercept_error_squared
