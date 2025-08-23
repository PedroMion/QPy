import pytest

from qpy.network import OpenNetwork
from qpy.distribution import Distribution


MOCK_DISTRIBUTION = Distribution.constant(value=1)
TOTAL_SERVERS = 2
VALID_SERVER_ID = 0
INVALID_SERVER_ID = 99
TIME_LIMIT = 5.0
VALID_PRIORITY_DISTRIBUTION = {1: 0.7, 2: 0.3}
ZERO_VALUE = 0
NEGATIVE_VALUE = -1


@pytest.fixture
def open_network_empty():
    return OpenNetwork()


@pytest.fixture
def open_network_with_servers():
    network = OpenNetwork()
    for _ in range(TOTAL_SERVERS):
        network.add_server(service_distribution=MOCK_DISTRIBUTION)
    return network


"""
Particionamento do espaço de entrada para função add_entry_point() da classe OpenNetwork:
    server_id: < 0 | >= 0 Válido | >= 0 Inválido
    arrival_distribution: None | Válido
    priority_distribution: None | Válido
"""

"""server_id >= 0 Válido | arrival_distribution Válido | priority_distribution = None (Válido)"""
def test_add_entry_point_when_server_and_distribution_are_valid_and_priority_is_none_should_add_arrival(open_network_with_servers):
    open_network_with_servers.add_entry_point(VALID_SERVER_ID, arrival_distribution=MOCK_DISTRIBUTION, priority_distribution=None)

    assert VALID_SERVER_ID in open_network_with_servers.arrivals
    assert len(open_network_with_servers.arrivals[VALID_SERVER_ID]) == 1
    assert open_network_with_servers.priorities[VALID_SERVER_ID] == None

"""server_id >= 0 Válido | arrival_distribution Válido | priority_distribution Válido (Válido)"""
def test_add_entry_point_when_server_id_and_distribution_are_valid_and_priority_is_provided_should_add_arrival_and_priority(open_network_with_servers):
    open_network_with_servers.add_entry_point(VALID_SERVER_ID, arrival_distribution=MOCK_DISTRIBUTION, priority_distribution=VALID_PRIORITY_DISTRIBUTION)

    assert VALID_SERVER_ID in open_network_with_servers.arrivals
    assert len(open_network_with_servers.arrivals[VALID_SERVER_ID]) == 1
    assert open_network_with_servers.priorities[VALID_SERVER_ID] == VALID_PRIORITY_DISTRIBUTION

"""server_id >= 0 Inválido | arrival_distribution Válido | priority_distribution = None (Inválido)"""
def test_add_entry_point_when_server_id_is_invalid_should_raise_exception(open_network_with_servers):
    with pytest.raises(ValueError):
        open_network_with_servers.add_entry_point(INVALID_SERVER_ID, arrival_distribution=MOCK_DISTRIBUTION)

"""server_id >= 0 Válido | arrival_distribution = None | priority_distribution = None (Inválido)"""
def test_add_entry_point_when_distribution_is_invalid_should_raise_exception(open_network_with_servers):
    with pytest.raises(TypeError):
        open_network_with_servers.add_entry_point(VALID_SERVER_ID, arrival_distribution=None)

"""server_id < 0 | arrival_distribution Válido | priority_distribution = None (Inválido)"""
def test_add_entry_point_when_server_id_is_negative_should_raise_exception(open_network_with_servers):
    with pytest.raises(ValueError):
        open_network_with_servers.add_entry_point(NEGATIVE_VALUE, arrival_distribution=MOCK_DISTRIBUTION)


"""
Particionamento do espaço de entrada para função generate_jobs() da classe OpenNetwork:
    arrivals: Vazio | Não vazio
    time_limit: < 0 | 0 | > 0
"""

"""arrivals Vazio | time_limit > 0 (Válido)"""
def test_generate_jobs_when_no_arrivals_were_configured_should_return_empty_list(open_network_with_servers):
    jobs = open_network_with_servers.generate_jobs(time_limit=TIME_LIMIT)

    assert jobs == []

"""arrivals Não vazio | time_limit > 0 (Válido)"""
def test_generate_jobs_when_arrivals_exist_should_generate_jobs(open_network_with_servers):
    open_network_with_servers.add_entry_point(VALID_SERVER_ID, arrival_distribution=MOCK_DISTRIBUTION)

    jobs = open_network_with_servers.generate_jobs(time_limit=TIME_LIMIT)

    assert len(jobs) > 0

"""arrivals Não vazio | time_limit = 0 (Válido)"""
def test_generate_jobs_when_time_limit_is_zero_should_return_empty(open_network_with_servers):
    open_network_with_servers.add_entry_point(VALID_SERVER_ID, arrival_distribution=MOCK_DISTRIBUTION)

    jobs = open_network_with_servers.generate_jobs(time_limit=ZERO_VALUE)

    assert jobs == []

"""arrivals Não vazio | time_limit < 0 (Inválido)"""
def test_generate_jobs_when_time_limit_is_negative_should_raise_exception(open_network_with_servers):
    open_network_with_servers.add_entry_point(VALID_SERVER_ID, arrival_distribution=MOCK_DISTRIBUTION)

    with pytest.raises(ValueError):
        open_network_with_servers.generate_jobs(time_limit=NEGATIVE_VALUE)