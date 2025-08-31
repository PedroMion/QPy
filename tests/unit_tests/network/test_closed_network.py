import pytest

from qpy.network import ClosedNetwork
from qpy.distribution import Distribution


MOCK_DISTRIBUTION = Distribution.constant(value=1)
TOTAL_SERVERS = 2
VALID_SERVER_ID = 0
INVALID_SERVER_ID = 99
VALID_PRIORITY = {1: 0.5, 2: 0.5}
VALID_PRIORITY2 = {1: 2, 2: 2}
INVALID_PRIORITY = {1: 'banana'}
PROBABILITY = 0.3
INVALID_PROBABILITY = 2
NUMBER_OF_TERMINALS = 3
ZERO_VALUE = 0
NEGATIVE_VALUE = -1


@pytest.fixture
def closed_network_empty():
    return ClosedNetwork(think_time_distribution=MOCK_DISTRIBUTION, number_of_terminals=NUMBER_OF_TERMINALS)


@pytest.fixture
def closed_network_with_servers():
    network = ClosedNetwork(think_time_distribution=MOCK_DISTRIBUTION, number_of_terminals=NUMBER_OF_TERMINALS)
    for _ in range(TOTAL_SERVERS):
        network.add_server(service_distribution=MOCK_DISTRIBUTION)
    return network


"""
Particionamento do espaço de entrada para função add_priorities() da classe ClosedNetwork utilizando Each Choice Coverage:
    priorities: Válido | Inválido
"""

"""priorities Válido (Válido)"""
def test_add_priorities_when_input_is_valid_should_store_priorities(closed_network_empty):
    closed_network_empty.add_priorities(VALID_PRIORITY)

    assert closed_network_empty.priorities == VALID_PRIORITY

"""priorities Válido (Válido)"""
def test_add_priorities_when_input_isnt_properly_formatted_should_store_priorities(closed_network_empty):
    closed_network_empty.add_priorities(VALID_PRIORITY2)

    assert closed_network_empty.priorities == VALID_PRIORITY

"""priorities Inválido (Inválido)"""
def test_add_priorities_when_input_is_invalid_should_raise_exception(closed_network_empty):
    with pytest.raises(ValueError):
        closed_network_empty.add_priorities(INVALID_PRIORITY)


"""
Particionamento do espaço de entrada para função add_terminals_routing_probability() da classe ClosedNetwork utilizando Each Choice Coverage:
    destination_server_id: < 0 | >= 0
    probability: < 0 | >= 0
"""

"""destination_server_id >= 0 | probability >= 0 (Válido)"""
def test_add_terminals_routing_probability_when_both_parameters_are_valid_should_update_probability(closed_network_with_servers):
    closed_network_with_servers.add_terminals_routing_probability(destination_server_id=VALID_SERVER_ID, probability=PROBABILITY)

    assert closed_network_with_servers.entry_point_routing[VALID_SERVER_ID] == PROBABILITY
    assert closed_network_with_servers.entry_point_routing['end'] == 1 - PROBABILITY

"""destination_server_id >= 0 | probability >= 0 (Inválido)"""
def test_add_terminals_routing_probability_when_priority_is_invalid_should_raise_exception(closed_network_with_servers):
    with pytest.raises(ValueError):
        closed_network_with_servers.add_terminals_routing_probability(destination_server_id=VALID_SERVER_ID, probability=INVALID_PROBABILITY)

"""destination_server_id >= 0 | probability >= 0 (Inválido)"""
def test_add_terminals_routing_probability_when_server_is_invalid_should_raise_exception(closed_network_with_servers):
    with pytest.raises(ValueError):
        closed_network_with_servers.add_terminals_routing_probability(destination_server_id=INVALID_SERVER_ID, probability=PROBABILITY)

"""destination_server_id < 0 | probability >= 0 (Inválido)"""
def test_add_terminals_routing_probability_when_server_is_negative_should_raise_exception(closed_network_with_servers):
    with pytest.raises(ValueError):
        closed_network_with_servers.add_terminals_routing_probability(destination_server_id=NEGATIVE_VALUE, probability=PROBABILITY)

"""destination_server_id >= 0 | probability < 0 (Inválido)"""
def test_add_terminals_routing_probability_when_probability_is_negative_should_raise_exception(closed_network_with_servers):
    with pytest.raises(ValueError):
        closed_network_with_servers.add_terminals_routing_probability(destination_server_id=VALID_SERVER_ID, probability=NEGATIVE_VALUE)


"""
Particionamento do espaço de entrada para função generate_jobs() da classe ClosedNetwork utilizando Each Choice Coverage:
    number_of_terminals: 0 | > 0
"""

"""number_of_terminals = 0"""
def test_generate_jobs_when_there_are_no_terminals_should_return_nothing():
    expected_result = []
    mock_network = ClosedNetwork(think_time_distribution=MOCK_DISTRIBUTION, number_of_terminals=ZERO_VALUE)

    mock_network.add_server(service_distribution=MOCK_DISTRIBUTION)
    mock_network.add_terminals_routing_probability(destination_server_id=ZERO_VALUE, probability=0.5)

    assert mock_network.generate_jobs() == expected_result

"""number_of_terminals > 0"""
def test_generate_jobs_when_there_are_terminals_should_return_jobs(closed_network_with_servers):
    expected_number_of_jobs = NUMBER_OF_TERMINALS

    closed_network_with_servers.add_terminals_routing_probability(destination_server_id=ZERO_VALUE, probability=0.5)

    generated_jobs = closed_network_with_servers.generate_jobs()

    assert len(generated_jobs) == expected_number_of_jobs