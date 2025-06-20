import random, numpy as np


from abc import ABC, abstractmethod
from enum import Enum


class IDistribution(ABC):
    @abstractmethod
    def sample(self):
        pass

class ConstantDistribution(IDistribution):
    def __init__(self, value: float):
        self.value = value
    
    def sample(self) -> float:
        return self.value

class ExponentialDistribution(IDistribution):
    def __init__(self, lambda_value: float):
        self.lambda_value = lambda_value
    
    def sample(self) -> float:
        return -np.log(1-random.random())/self.lambda_value

class UniformDistribution(IDistribution):
    def __init__(self, lower_bound: float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    
    def sample(self) -> float:
        return random.uniform(self.lower_bound, self.upper_bound)
    
class NormalDistribution(IDistribution):
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma
    
    def sample(self) -> float:
        return random.gauss(self.mu, self.sigma)
    
class Distribution():
    def __new__(cls, *args, **kwargs):
        if cls is Distribution:
            raise TypeError("Cannot instantiate this class directly.")
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def constant(value: float) -> ConstantDistribution:
        return ConstantDistribution(value)
    
    @staticmethod
    def exponential(lambda_value: float) -> ExponentialDistribution:
        return ExponentialDistribution(lambda_value)

    @staticmethod
    def uniform(lower_bound: float, upper_bound: float) -> UniformDistribution:
        if upper_bound >= lower_bound:
            return UniformDistribution(lower_bound, upper_bound)
        raise ValueError('Lower bound should be smaller than upper bound.')
    
    @staticmethod
    def normal(mu: float, sigma: float) -> NormalDistribution:
        return NormalDistribution(mu, sigma)