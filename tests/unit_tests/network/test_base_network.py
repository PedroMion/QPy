import pytest

from qpy.distribution import Distribution
from qpy.network import BaseNetwork
from qpy.queue_discipline import QueueDiscipline
from qpy.server import Server


MOCK_DISTRIBUTION = Distribution.constant(value = 1)
TOTAL_SERVERS = 3
ROUTING_PROBABILITY = 0.5
INVALID_SERVER_ID = 99


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
Particionamento do espaço de entrada para função add_server() da classe BaseNetwork:
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