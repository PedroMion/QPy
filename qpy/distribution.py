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
        return self._value

class ExponentialDistribution(IDistribution):
    def __init__(self, lambda_value: float):
        self._lambda_value = lambda_value
    
    def sample(self) -> float:
        return -np.log(1-random.random())/self._lambda_value

class UniformDistribution(IDistribution):
    def __init__(self, lower_bound: float, upper_bound: float):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
    
    def sample(self) -> float:
        return random.uniform(self._lower_bound, self._upper_bound)
    
class NormalDistribution(IDistribution):
    def __init__(self, mu: float, sigma: float):
        self._mu = mu
        self._sigma = sigma
    
    def sample(self) -> float:
        return random.gauss(self._mu, self._sigma)
    
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
        return ConstantDistribution(value)
    
    @staticmethod
    @validate_call
    def exponential(lambda_value: float) -> ExponentialDistribution:
        """
        Returns a distribution of type exponential.

        Parameters
        ----------
        lambda_value : float - Required
            The rate parameter (lambda) of the exponential distribution.
        """
        return ExponentialDistribution(lambda_value)

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
        return NormalDistribution(mu, sigma)