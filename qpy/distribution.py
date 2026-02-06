import random, numpy as np


from abc import ABC, abstractmethod
from pydantic import validate_call


class IDistribution(ABC):
    @abstractmethod
    def sample(self):
        pass

class ConstantDistribution(IDistribution):
    def __init__(self, value: float):
        self._value = value
    
    def sample(self) -> float:
        return max(round(self._value, 4), 0.0001)

class ExponentialDistribution(IDistribution):
    def __init__(self, mean_time_between_events: float):
        self._mean_time_between_events = mean_time_between_events
    
    def sample(self) -> float:
        return max(round(-np.log(1 - random.random()) * self._mean_time_between_events, 4), 0.0001)

class UniformDistribution(IDistribution):
    def __init__(self, lower_bound: float, upper_bound: float):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
    
    def sample(self) -> float:
        return max(round(random.uniform(self._lower_bound, self._upper_bound), 4), 0.0001)
    
class NormalDistribution(IDistribution):
    def __init__(self, mu: float, sigma: float):
        self._mu = mu
        self._sigma = sigma
    
    def sample(self) -> float:
        return max(round(random.gauss(self._mu, self._sigma), 4), 0.0001)
    
class Distribution():
    def __new__(cls, *args, **kwargs):
        if cls is Distribution:
            raise TypeError("Cannot instantiate this class directly.")
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    @validate_call
    def constant(value: float) -> ConstantDistribution:
        """
        Returns a distribution of type constant.

        Parameters
        ----------
        value : float - Required
            The value to always be returned when this distribution is sampled.
        """
        if value < 0:
            raise ValueError('Negative values for distribution parameters are not allowed')
        
        return ConstantDistribution(value)
    
    @staticmethod
    @validate_call
    def exponential(mean_time_between_events: float) -> ExponentialDistribution:
        """
        Returns a distribution of type exponential.

        Parameters
        ----------
        mean_time_between_events : float - Required
            The expected time between consecutive events. This parameter represents the mean of an exponential distribution and corresponds to the inverse of the rate parameter (λ) of the associated Poisson process.
        """
        if mean_time_between_events < 0:
            raise ValueError('Negative values for distribution parameters are not allowed')
                
        return ExponentialDistribution(mean_time_between_events)

    @staticmethod
    @validate_call
    def uniform(lower_bound: float, upper_bound: float) -> UniformDistribution:
        """
        Returns a distribution of type uniform.

        Parameters
        ----------
        lower_bound : float - Required
            The lower bound of the uniform distribution.

        upper_bound : float - Required
            The upper bound of the uniform distribution. Must be greater than or equal to the lower bound.

        Raises
        ------
        ValueError
            If the lower bound is greater than the upper bound.
        """
        if lower_bound < 0 or upper_bound < 0:
            raise ValueError('Negative values for distribution parameters are not allowed')

        if upper_bound >= lower_bound:
            return UniformDistribution(lower_bound, upper_bound)
        raise ValueError('Lower bound should be smaller than upper bound.')
    
    @staticmethod
    @validate_call
    def normal(mu: float, sigma: float) -> NormalDistribution:
        """
        Returns a distribution of type normal.

        Parameters
        ----------
        mu : float - Required
            The mean (mu) of the normal distribution.

        sigma : float - Required
            The standard deviation (sigma) of the normal distribution.
        """
        if mu < 0 or sigma < 0:
            raise ValueError('Negative values for distribution parameters are not allowed')
                
        return NormalDistribution(mu, sigma)