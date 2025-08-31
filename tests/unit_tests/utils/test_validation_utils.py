import pytest

from qpy.validation_utils import (
    validate_number_params_not_negative,
    validate_object_params_not_none,
    validate_number_params_not_negative_and_not_none
)


TEST_FUNCTION = "test_function"
STRING_TEST = "test"
VALID_VALUE = 10
ZERO_VALUE = 0
NEGATIVE_VALUE = -5


"""
Particionamento do espaço de entrada para função validate_number_params_not_negative() utilizando Each Choice Coverage:
    value: None | < 0 | = 0 | > 0 | NaN
"""

"""value None (Válido)"""
def test_validate_number_params_not_negative_when_value_is_none_should_not_raise_exception():
    validate_number_params_not_negative(function_name=TEST_FUNCTION, param=None)

"""value Número positivo (Válido)"""
def test_validate_number_params_not_negative_when_value_is_positive_should_not_raise_exception():
    validate_number_params_not_negative(function_name=TEST_FUNCTION, param=VALID_VALUE)

"""value Zero (Válido)"""
def test_validate_number_params_not_negative_when_value_is_zero_should_not_raise_exception():
    validate_number_params_not_negative(function_name=TEST_FUNCTION, param=ZERO_VALUE)

"""value Número negativo (Inválido)"""
def test_validate_number_params_not_negative_when_value_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        validate_number_params_not_negative(function_name=TEST_FUNCTION, param=NEGATIVE_VALUE)

"""value Tipo inválido (Inválido)"""
def test_validate_number_params_not_negative_when_value_is_invalid_type_should_raise_exception():
    with pytest.raises(TypeError):
        validate_number_params_not_negative(function_name=TEST_FUNCTION, param=STRING_TEST)


"""
Particionamento do espaço de entrada para função validate_object_params_not_none() utilizando Each Choice Coverage:
    value: None | Válido
"""

"""value None (Inválido)"""
def test_validate_object_params_not_none_when_value_is_none_should_raise_exception():
    with pytest.raises(TypeError):
        validate_object_params_not_none(function_name=TEST_FUNCTION, param=None)

"""value Válido (Válido)"""
def test_validate_object_params_not_none_when_value_is_valid_should_not_raise_exception():
    validate_object_params_not_none(function_name=TEST_FUNCTION, param=STRING_TEST)


"""
Particionamento do espaço de entrada para função validate_number_params_not_negative_and_not_none() utilizando Each Choice Coverage:
    value: None | < 0 | = 0 | > 0 | NaN
"""

"""value None (Inválido)"""
def test_validate_number_params_not_negative_and_not_none_when_value_is_none_should_raise_exception():
    with pytest.raises(TypeError):
        validate_number_params_not_negative_and_not_none(function_name=TEST_FUNCTION, param=None)

"""value Número positivo (Válido)"""
def test_validate_number_params_not_negative_and_not_none_when_value_is_positive_should_not_raise_exception():
    validate_number_params_not_negative_and_not_none(function_name=TEST_FUNCTION, param=VALID_VALUE)

"""value Zero (Válido)"""
def test_validate_number_params_not_negative_and_not_none_when_value_is_zero_should_not_raise_exception():
    validate_number_params_not_negative_and_not_none(function_name=TEST_FUNCTION, param=ZERO_VALUE)

"""value Número negativo (Inválido)"""
def test_validate_number_params_not_negative_and_not_none_when_value_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        validate_number_params_not_negative_and_not_none(function_name=TEST_FUNCTION, param=NEGATIVE_VALUE)

"""value Tipo inválido (Inválido)"""
def test_validate_number_params_not_negative_and_not_none_when_value_is_invalid_type_should_raise_exception():
    with pytest.raises(TypeError):
        validate_number_params_not_negative_and_not_none(function_name=TEST_FUNCTION, param=STRING_TEST)
