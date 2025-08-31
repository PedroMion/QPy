import pytest

from qpy.distribution import Distribution
from qpy.network import BaseNetwork
from qpy.queue_discipline import QueueDiscipline
from qpy.server import Server


MOCK_DISTRIBUTION = Distribution.constant(value = 1)
TOTAL_SERVERS = 3
ROUTING_PROBABILITY = 0.5
INVALID_ROUTING_PROBABILITY = 2
ORIGIN_SERVER_ID = 0
DESTINATION_SERVER_ID = 1
INVALID_SERVER_ID = 99
ZERO_VALUE = 0
NEGATIVE_VALUE = -1


@pytest.fixture
def base_network_empty():
    return BaseNetwork()


@pytest.fixture
def base_network_with_servers():
    network = BaseNetwork()
    for _ in range(TOTAL_SERVERS):
        network.add_server(service_distribution=MOCK_DISTRIBUTION)
    return network


"""
Particionamento do espaço de entrada para função add_server() da classe BaseNetwork utilizando Each Choice Coverage:
    queue_discipline: None | Válido
"""

"""queue_discipline = None (Válido)"""
def test_add_server_when_queue_discipline_is_none_should_use_fcfs(base_network_empty):
    server_id = base_network_empty.add_server(service_distribution=MOCK_DISTRIBUTION, queue_discipline=None)

    assert server_id == 0
    assert isinstance(base_network_empty.servers[server_id], Server)
    assert base_network_empty.servers[server_id].server_execution.queue.discipline == QueueDiscipline.fcfs().discipline


"""queue_discipline Válido (Válido)"""
def test_add_server_when_queue_discipline_is_provided_should_use_it(base_network_empty):
    custom_queue = QueueDiscipline.srt()
    server_id = base_network_empty.add_server(service_distribution=MOCK_DISTRIBUTION, queue_discipline=custom_queue)

    assert base_network_empty.servers[server_id].server_execution.queue.discipline == custom_queue.discipline


"""
Particionamento do espaço de entrada para função add_servers_connection() da classe BaseNetwork utilizando Each Choice Coverage:
    origin_server_id: < 0 | >= 0
    destination_server_id: < 0 | >= 0
    routing_probability: < 0 | 0 | > 0
"""

"""origin_server_id >= 0 | destination_server_id >= 0 | routing_probability > 0 (Válido)"""
def test_add_servers_connection_when_parameters_are_valid_should_add_server(base_network_with_servers):
    base_network_with_servers.add_servers_connection(ORIGIN_SERVER_ID, DESTINATION_SERVER_ID, ROUTING_PROBABILITY)

    assert base_network_with_servers.servers[ORIGIN_SERVER_ID].destinations[DESTINATION_SERVER_ID] == ROUTING_PROBABILITY

"""origin_server_id >= 0 | destination_server_id >= 0 | routing_probability = 0 (Válido)"""
def test_add_servers_connection_when_routing_probability_is_zero_should_do_nothing(base_network_with_servers):
    base_network_with_servers.add_servers_connection(ORIGIN_SERVER_ID, DESTINATION_SERVER_ID, routing_probability=ZERO_VALUE)

    assert base_network_with_servers.servers[ORIGIN_SERVER_ID].destinations[DESTINATION_SERVER_ID] == ZERO_VALUE

"""origin_server_id < 0 | destination_server_id >= 0 | routing_probability > 0 (Inválido)"""
def test_add_servers_connection_when_origin_server_id_is_negative_should_raise_exception(base_network_with_servers):
    with pytest.raises(ValueError):
        base_network_with_servers.add_servers_connection(origin_server_id=NEGATIVE_VALUE, destination_server_id=DESTINATION_SERVER_ID, routing_probability=ROUTING_PROBABILITY)

"""origin_server_id >= 0 | destination_server_id < 0 | routing_probability > 0 (Inválido)"""
def test_add_servers_connection_when_destination_server_id_is_negative_should_raise_exception(base_network_with_servers):
    with pytest.raises(ValueError):
        base_network_with_servers.add_servers_connection(origin_server_id=ORIGIN_SERVER_ID, destination_server_id=NEGATIVE_VALUE, routing_probability=ROUTING_PROBABILITY)

"""origin_server_id >= 0 | destination_server_id >= 0 | routing_probability < 0 (Inválido)"""
def test_add_servers_connection_when_routing_probability_is_negative_should_raise_exception(base_network_with_servers):
    with pytest.raises(ValueError):
        base_network_with_servers.add_servers_connection(origin_server_id=ORIGIN_SERVER_ID, destination_server_id=DESTINATION_SERVER_ID, routing_probability=NEGATIVE_VALUE)