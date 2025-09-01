import pytest


from qpy.distribution import Distribution
from qpy.server import Server
from qpy.queue_discipline import QueueDiscipline


SERVER_ID = 0
MOCK_DISTRIBUTION = Distribution.constant(value=1)
MOCK_QUEUE = QueueDiscipline.fcfs()

DESTINATION_SERVER_ID = 1
VALID_PROBABILITY = 0.5
INVALID_PROBABILITY = 2
ZERO_VALUE = 0
NEGATIVE_VALUE = -1


@pytest.fixture
def server_mock_object():
    return Server(SERVER_ID, MOCK_DISTRIBUTION, MOCK_QUEUE)

"""
Particionamento do espaço de entrada para função add_destination() da classe Server utilizando Each Choice Coverage:
    destination_server_id: < 0 | >= 0
    probability: < 0 | >= 0
"""

"""destination_server_id >= 0 | probability >= 0 (Válido)"""
def test_add_destination_when_both_parameters_are_valid_should_add_destination(server_mock_object):
    server_mock_object.add_destination(DESTINATION_SERVER_ID, VALID_PROBABILITY)

    assert server_mock_object.destinations['end'] == 1 - VALID_PROBABILITY
    assert server_mock_object.destinations[DESTINATION_SERVER_ID] == VALID_PROBABILITY

"""destination_server_id >= 0 | probability >= 0 (Inválido)"""
def test_add_destination_when_probability_is_greater_than_one_should_raise_exception(server_mock_object):
    with pytest.raises(ValueError):
        server_mock_object.add_destination(DESTINATION_SERVER_ID, INVALID_PROBABILITY)

"""destination_server_id < 0 | probability >= 0 (Inválido)"""
def test_add_destination_when_destination_server_is_negative_should_raise_exception(server_mock_object):
    with pytest.raises(ValueError):
        server_mock_object.add_destination(NEGATIVE_VALUE, VALID_PROBABILITY)

"""destination_server_id >= 0 | probability < 0 (Inválido)"""
def test_add_destination_when_probability_is_negative_should_raise_exception(server_mock_object):
    with pytest.raises(ValueError):
        server_mock_object.add_destination(DESTINATION_SERVER_ID, NEGATIVE_VALUE)