import pytest
from qpy.distribution import Distribution, ConstantDistribution, ExponentialDistribution, NormalDistribution, UniformDistribution


NEGATIVE_VALUE = -1
ZERO_VALUE = 0
POSITIVE_VALUE = 1


"""
Particionamento do espaço de entrada para função constant() da classe Distribution utilizando Each Choice Coverage:
    value: 0 | < 0 | > 0
"""

"""value < 0 (Inválido)"""
def test_constant_distribution_generation_when_value_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.constant(NEGATIVE_VALUE)

"""value = 0 (Válido)"""
def test_constant_distribution_generation_when_value_is_zero_should_return_proper_object():
    distribution = Distribution.constant(ZERO_VALUE)

    assert isinstance(distribution, ConstantDistribution)
    assert distribution._value == ZERO_VALUE

"""value > 0 (Válido)"""
def test_constant_distribution_generation_when_value_is_valid_should_return_proper_object():
    distribution = Distribution.constant(POSITIVE_VALUE)

    assert isinstance(distribution, ConstantDistribution)
    assert distribution._value == POSITIVE_VALUE


"""
Particionamento do espaço de entrada para função exponential() da classe Distribution utilizando Each Choice Coverage:
    lambda_value: 0 | < 0 | > 0
"""

"""lambda_value < 0 (Inválido)"""
def test_exponential_distribution_generation_when_lambda_value_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.exponential(NEGATIVE_VALUE)

"""lambda_value = 0 (Válido)"""
def test_exponential_distribution_generation_when_lambda_value_is_zero_should_return_proper_object():
    distribution = Distribution.exponential(ZERO_VALUE)

    assert isinstance(distribution, ExponentialDistribution)
    assert distribution._lambda_value == ZERO_VALUE

"""lambda_value > 0 (Válido)"""
def test_exponential_distribution_generation_when_lambda_value_is_valid_should_return_proper_object():
    distribution = Distribution.exponential(POSITIVE_VALUE)

    assert isinstance(distribution, ExponentialDistribution)
    assert distribution._lambda_value == POSITIVE_VALUE


"""
Particionamento do espaço de entrada para função uniform() da classe Distribution utilizando Each Choice Coverage:
    lower_bound: <= 0 | > 0
    upper_bound: <= 0 | > 0
"""

"""lower_bound <= 0 | upper_bound > 0 (Inválido)"""
def test_uniform_distribution_generation_when_lower_bound_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.uniform(lower_bound=NEGATIVE_VALUE, upper_bound=POSITIVE_VALUE)

"""lower_bound > 0 | upper_bound <= 0 (Inválido)"""
def test_uniform_distribution_generation_when_upper_bound_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.uniform(lower_bound=POSITIVE_VALUE, upper_bound=NEGATIVE_VALUE)

"""lower_bound > 0 | upper_bound > 0 (Inválido)"""
def test_uniform_distribution_generation_when_lower_bound_is_higher_than_upper_bound_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.uniform(lower_bound=POSITIVE_VALUE * 2, upper_bound=POSITIVE_VALUE)

"""lower_bound > 0 | upper_bound > 0 (Válido)"""
def test_uniform_distribution_generation_when_both_parameters_are_valid_should_return_proper_object():
    distribution = Distribution.uniform(lower_bound=POSITIVE_VALUE, upper_bound=POSITIVE_VALUE*2)

    assert isinstance(distribution, UniformDistribution)
    assert distribution._lower_bound == POSITIVE_VALUE
    assert distribution._upper_bound == POSITIVE_VALUE * 2


"""
Particionamento do espaço de entrada para função normal() da classe Distribution utilizando Each Choice Coverage:
    mu: <= 0 | > 0
    sigma: <= 0 | > 0
"""

"""mu <= 0 | sigma > 0 (Inválido)"""
def test_normal_distribution_generation_when_mu_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.normal(mu=NEGATIVE_VALUE, sigma=POSITIVE_VALUE)

"""mu > 0 | sigma <= 0 (Inválido)"""
def test_normal_distribution_generation_when_sigma_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        Distribution.normal(mu=POSITIVE_VALUE, sigma=NEGATIVE_VALUE)

"""mu > 0 | sigma > 0 (Válido)"""
def test_normal_distribution_generation_when_both_parameters_are_valid_should_return_proper_object():
    distribution = Distribution.normal(mu=POSITIVE_VALUE, sigma=POSITIVE_VALUE)

    assert isinstance(distribution, NormalDistribution)
    assert distribution._mu == POSITIVE_VALUE
    assert distribution._sigma == POSITIVE_VALUE