import pytest


from pydantic_core import ValidationError
from qpy.distribution import Distribution
from qpy.environment import Environment
from qpy.network import ClosedNetwork, OpenNetwork


VALID_DISTRIBUTION = Distribution.constant(value=10)
VALID_INTEGER = 10
ZERO_VALUE = 0
NEGATIVE_VALUE = -5
STRING_OBJECT = "teste"


"""
Particionamento do espaço de entrada para a função __init__() da classe Environment
    number_of_terminals: <= 0 | > 0 | None | Inválido
    think_time_distribution: None | Válido | Inválido
"""

"""number_of_terminals > 0 | think_time_distribution Válido (Válido)"""
def test_init_when_both_parameters_are_valid_should_create_closed_network():
    env = Environment(number_of_terminals=VALID_INTEGER, think_time_distribution=VALID_DISTRIBUTION)

    assert env._is_closed

"""number_of_terminals <= 0 | think_time_distribution Válido (Válido)"""
def test_init_when_number_of_terminals_is_zero_should_create_open_network():
    env = Environment(number_of_terminals=ZERO_VALUE, think_time_distribution=VALID_DISTRIBUTION)

    assert not env._is_closed

"""number_of_terminals None | think_time_distribution Válido (Válido)"""
def test_init_when_number_of_terminals_is_none_should_create_open_network():
    env = Environment(number_of_terminals=None, think_time_distribution=VALID_DISTRIBUTION)

    assert not env._is_closed

"""number_of_terminals Inválido | think_time_distribution Válido (Inválido)"""
def test_init_when_number_of_terminals_is_invalid_should_raise_exception():
    with pytest.raises(ValidationError):
        env = Environment(number_of_terminals=STRING_OBJECT, think_time_distribution=VALID_DISTRIBUTION)

"""number_of_terminals > 0 | think_time_distribution None (Válido)"""
def test_init_when_think_time_distribution_is_none_should_create_open_network():
    env = Environment(number_of_terminals=VALID_INTEGER, think_time_distribution=None)

    assert not env._is_closed

"""number_of_terminals > 0 | think_time_distribution Inválido (Inválido)"""
def test_init_when_think_time_distribution_is_invalid_should_raise_exception():
    with pytest.raises(ValidationError):
        env = Environment(number_of_terminals=VALID_INTEGER, think_time_distribution=STRING_OBJECT)