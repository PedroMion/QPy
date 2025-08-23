import pytest

from qpy.network import ClosedNetwork
from qpy.distribution import Distribution


MOCK_DISTRIBUTION = Distribution.constant(value=1)
TOTAL_SERVERS = 2
VALID_SERVER_ID = 0
VALID_PRIORITY = {1: 0.5, 2: 0.5}
VALID_PRIORITY2 = {1: 2, 2: 2}
INVALID_PRIORITY = {1: 'banana'}
PROBABILITY = 0.3
NUMBER_OF_TERMINALS = 3


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
Particionamento do espaço de entrada para função add_priorities() da classe ClosedNetwork:
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