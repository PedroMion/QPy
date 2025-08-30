import pytest


from qpy.event import Event
from qpy.distribution import ConstantDistribution

from qpy.utils import (
    randomly_draw_from_dictionary,
    transform_input_closed_network,
    validate_priority_input,
)


EVENT_COUNT = 1
CURRENT_TIME = 5.0
SERVER_ID = 1
PRIORITY = 1


@pytest.fixture
def constant_distribution():
    return ConstantDistribution(1.0)


@pytest.fixture
def empty_queue():
    return []


"""
Particionamento do espaço de entrada para função randomly_draw_from_dictionary:
    probabilities: Válido | Vazio | None
"""

"""probabilities Válido (Válido)"""
def test_randomly_draw_from_dictionary_when_distribution_is_valid_should_return_key():
    probabilities = {"a": 0.5, "b": 0.5}

    result = randomly_draw_from_dictionary(probabilities)

    assert result in probabilities.keys()

"""probabilities Válido (Válido)"""
def test_randomly_draw_from_dictionary_when_distribution_is_not_normalized_should_return_key():
    probabilities = {"x": 2, "y": 3}

    result = randomly_draw_from_dictionary(probabilities)

    assert result in probabilities.keys()

"""probabilities Vazio (Válido)"""
def test_randomly_draw_from_dictionary_when_dict_is_empty_should_return_none():
    probabilities = {}

    result = randomly_draw_from_dictionary(probabilities)

    assert result is None

"""probabilities None (Inválido)"""
def test_randomly_draw_from_dictionary_when_parameter_is_none_should_raise_exception():
    with pytest.raises(TypeError):
        randomly_draw_from_dictionary(None)


"""
Particionamento do espaço de entrada para função transform_input_closed_network:
    input: Somente com 'end' | Contém 'end' | Não contém 'end' | None
"""

"""input Somente com 'end'"""
def test_transform_input_closed_network_when_there_are_no_routes_should_raise_exception():
    input_data = {'end': 1}

    with pytest.raises(ValueError):
        transform_input_closed_network(input_data)

"""input Contém 'end' (Válido)"""
def test_transform_input_closed_network_when_end_key_is_present_should_return_normalized_dict():
    expected_a_probability = 0.6
    expected_b_probability = 0.4
    
    input_data = {"A": 0.3, "B": 0.2, "end": 0.5}

    result = transform_input_closed_network(input_data)

    assert "end" not in result
    assert round(sum(result.values()), 4) == 1.0
    assert result["A"] == expected_a_probability
    assert result["B"] == expected_b_probability

"""input Não contém 'end' (Válido)"""
def test_transform_input_closed_network_when_end_key_is_not_present_should_return_same_ratios():
    expected_a_probability = 0.4
    expected_b_probability = 0.6
    
    input_data = {"A": 0.4, "B": 0.6}

    result = transform_input_closed_network(input_data)

    assert result["A"] == expected_a_probability
    assert result["B"] == expected_b_probability

"""input None (Inválido)"""
def test_transform_input_closed_network_when_input_is_none_should_raise_exception():
    with pytest.raises(TypeError):
        transform_input_closed_network(input=None)


"""
Particionamento do espaço de entrada para função validate_priority_input:
    input: None | Válido (soma = 1) | Válido (soma != 1) | Inválido (elementos não numéricos) | Inválido (prioridade negativa)
    with_priority: True | False
"""

"""input None | with_priority = True (Válido)"""
def test_validate_priority_input_when_input_is_none_should_return_none():
    assert validate_priority_input(input=None) is None

"""input Válido | with_priority = False (Válido)"""
def test_validate_priority_input_when_priority_is_disabled_should_return_none():
    input_data = {"0": 1.0}
    assert validate_priority_input(input_data, with_priority=False) is None

"""input Válido (soma = 1) | with_priority = True (Válido)"""
def test_validate_priority_input_when_distribution_is_valid_should_return_same_input():
    input_data = {"0": 0.5, "1": 0.5}

    result = validate_priority_input(input_data)

    assert result == input_data

"""input Válido (soma != 1) | with_priority = True (Válido)"""
def test_validate_priority_input_when_distribution_is_not_normalized_should_normalize():
    expected_zero_probability = 0.5
    expected_one_probability = 0.5
    
    input_data = {"0": 2, "1": 2}

    result = validate_priority_input(input_data)

    assert round(sum(result.values()), 4) == 1.0
    assert result["0"] == expected_zero_probability
    assert result["1"] == expected_one_probability

"""input Inválido (prioridade negativa) | with_priority = True (Inválido)"""
def test_validate_priority_input_when_priority_is_negative_should_raise_exception():
    input_data = {"-1": 1.0}

    with pytest.raises(ValueError):
        validate_priority_input(input_data)

"""input Inválido (elementos não numéricos) | with_priority = True (Inválido)"""
def test_validate_priority_input_when_priority_is_invalid_should_raise_exception():
    input_data = {"a": 1.0}

    with pytest.raises(ValueError):
        validate_priority_input(input_data)