import heapq
import pytest


from unittest.mock import MagicMock
from qpy.distribution import Distribution
from qpy.job import Job
from qpy.execution import Execution
from qpy.network import OpenNetwork


TOTAL_TIME = 10
TIME_UNIT = 'seconds'
VALID_TIME = 5
ZERO_VALUE = 0
EVENT_COUNT = 0

ARRIVAL_EVENT = "arrival"
DEPARTURE_EVENT = "departure"

CONSTANT_DISTRIBUTION_VALUE = 5
MOCK_DISTRIBUTION = Distribution.constant(value=CONSTANT_DISTRIBUTION_VALUE)
SERVER_ID = 0
JOB_SERVICE_TIME = 2
MOCK_NEW_JOB_BEING_EXECUTED = (JOB_SERVICE_TIME, MagicMock())


@pytest.fixture
def mock_event():
    event = MagicMock()
    event.canceled = False
    event.current_time = VALID_TIME
    event.server_id = SERVER_ID
    event.type = ARRIVAL_EVENT
    event.job = MagicMock()

    return event

@pytest.fixture
def mock_execution_object():
    network = OpenNetwork()
    network.add_server(MOCK_DISTRIBUTION)
    network.add_entry_point(SERVER_ID, MOCK_DISTRIBUTION)
    
    execution = Execution(time=TOTAL_TIME, warmup=ZERO_VALUE, queue=[], network_configuration=network, time_unit=TIME_UNIT)

    return execution


"""
Particionamento do espaço de entrada para função execute() da classe Execution utilizando Each Choice Coverage:
    current_time: <= time | > time
    queue: Empty | Not Empty
"""

"""current_time <= time | queue Empty (Válido)"""
def test_execute_when_event_queue_is_empty_should_return_results(mock_execution_object):
    result = mock_execution_object.execute()

    assert result == mock_execution_object.results

"""current_time > time | queue Empty (Válido)"""
def test_execute_when_time_limit_was_reached_should_return_results(mock_execution_object):
    mock_execution_object.current_time = TOTAL_TIME * 2

    result = mock_execution_object.execute()

    assert result == mock_execution_object.results

"""current_time <= time | queue Not Empty (Válido)"""
def test_execute_when_event_is_canceled_should_ignore(mock_execution_object, mock_event):
    mock_event.canceled = True
    mock_execution_object._case_event_is_arrival = MagicMock()
    mock_execution_object._case_event_is_departure_or_preemption = MagicMock()

    heapq.heappush(mock_execution_object.event_queue, (0, 0, mock_event))

    mock_execution_object.execute()

    mock_execution_object._case_event_is_arrival.assert_not_called()
    mock_execution_object._case_event_is_departure_or_preemption.assert_not_called()

"""current_time <= time | queue Not Empty (Válido)"""
def test_execute_when_event_is_arrival_should_call_case_arrival(mock_execution_object, mock_event):
    heapq.heappush(mock_execution_object.event_queue, (0, 0, mock_event))
    mock_execution_object._case_event_is_arrival = MagicMock()

    mock_execution_object.execute()

    mock_execution_object._case_event_is_arrival.assert_called_once_with(mock_event)
    assert mock_execution_object.current_time == VALID_TIME

"""current_time <= time | queue Not Empty (Válido)"""
def test_execute_when_event_is_departure_should_call_case_departure(mock_execution_object, mock_event):
    mock_event.type = DEPARTURE_EVENT
    heapq.heappush(mock_execution_object.event_queue, (0, 0, mock_event))
    mock_execution_object._case_event_is_departure_or_preemption = MagicMock()

    mock_execution_object.execute()

    mock_execution_object._case_event_is_departure_or_preemption.assert_called_once_with(mock_event)
    assert mock_execution_object.current_time == VALID_TIME


"""
Particionamento do espaço de entrada para função _add_next_departure_event() da classe Execution utilizando Each Choice Coverage:
    event: 'departure' | 'preemption'
"""

"""event = 'departure' (Válido)"""
def test_add_next_departure_event_when_event_is_departure_should_serve_job(mock_execution_object, mock_event):
    mock_execution_object._add_next_departure_event(SERVER_ID, mock_event.job, VALID_TIME, JOB_SERVICE_TIME, event='departure')

    assert mock_execution_object.event_count == EVENT_COUNT + 1
    assert len(mock_execution_object.event_queue) == 1
    mock_event.job.serve.assert_called_once_with(VALID_TIME)

"""event = 'preemption' (Válido)"""
def test_add_next_departure_event_when_event_is_preemption_should_not_serve_job(mock_execution_object, mock_event):
    mock_execution_object._add_next_departure_event(SERVER_ID, mock_event.job, VALID_TIME, JOB_SERVICE_TIME, event='preemption')

    assert mock_execution_object.event_count == EVENT_COUNT + 1
    assert len(mock_execution_object.event_queue) == 1
    mock_event.job.serve.assert_not_called()


"""
Particionamento do espaço de entrada para função _route_job_after_event() da classe Execution utilizando Each Choice Coverage:
    route: = 'end' | != 'end'
"""

"""route = 'end' (Válido)"""
def test_route_job_after_event_when_route_is_end_should_end_job_and_compute_results(mock_execution_object, mock_event):
    mock_event.server.route_job = MagicMock()
    mock_event.server.route_job.return_value = 'end'
    mock_event.job.arrival_time = ZERO_VALUE
    
    mock_execution_object._route_job_after_event(mock_event)

    mock_event.job.reroute.assert_called_once_with(ZERO_VALUE)

"""route != 'end' (Válido)"""
def test_route_job_after_event_when_route_is_not_end_should_end_job_and_compute_results(mock_execution_object, mock_event):
    mock_event.server.route_job = MagicMock()
    mock_event.server.route_job.return_value = ZERO_VALUE
    mock_event.job.arrival_time = ZERO_VALUE
    mock_execution_object._add_next_departure_event = MagicMock()
    
    mock_execution_object._route_job_after_event(mock_event)

    mock_event.job.reroute.assert_called_once_with(ZERO_VALUE, ZERO_VALUE)
    mock_execution_object._add_next_departure_event.assert_called_once()


"""
Particionamento do espaço de entrada para função _case_event_is_arrival() da classe Execution utilizando Each Choice Coverage:
    service_time: None | Not None
"""

"""service_time None (Válido)"""
def test_case_event_is_arrival_when_job_is_not_being_executed_should_not_add_departure_event(mock_execution_object, mock_event):
    mock_event.server.job_arrival = MagicMock()
    mock_event.server.job_arrival.return_value = None

    mock_execution_object._add_next_departure_event = MagicMock()

    mock_execution_object._case_event_is_arrival(mock_event)

    mock_event.job.reroute.assert_called_once_with(ZERO_VALUE)
    mock_execution_object._add_next_departure_event.assert_not_called()

"""service_time Not None (Válido)"""
def test_case_event_is_arrival_when_job_is_being_executed_should_add_departure_event(mock_execution_object, mock_event):
    mock_event.server.job_arrival = MagicMock()
    mock_event.server.job_arrival.return_value = JOB_SERVICE_TIME

    mock_execution_object._add_next_departure_event = MagicMock()

    mock_execution_object._case_event_is_arrival(mock_event)

    mock_event.job.reroute.assert_called_once_with(ZERO_VALUE)
    mock_execution_object._add_next_departure_event.assert_called_once()


"""
Particionamento do espaço de entrada para função _case_event_is_departure_or_preemption() da classe Execution utilizando Each Choice Coverage:
    new_job_being_executed: None | Not None
"""

"""new_job_being_executed None (Válido)"""
def test_case_event_is_departure_or_preemption_when_new_job_is_not_being_executed_should_not_add_departure_event(mock_execution_object, mock_event):
    mock_event.server.finish_execution = MagicMock()
    mock_event.server.finish_execution.return_value = None

    mock_execution_object._add_next_departure_event = MagicMock()
    mock_execution_object._route_job_after_event = MagicMock()

    mock_execution_object._case_event_is_departure_or_preemption(mock_event)

    mock_execution_object._route_job_after_event.assert_called_once_with(mock_event)
    mock_execution_object._add_next_departure_event.assert_not_called()

"""new_job_being_executed Not None (Válido)"""
def test_case_event_is_departure_or_preemption_when_new_job_is_being_executed_should_add_departure_event(mock_execution_object, mock_event):
    mock_event.server.finish_execution = MagicMock()
    mock_event.server.finish_execution.return_value = MOCK_NEW_JOB_BEING_EXECUTED

    mock_execution_object._add_next_departure_event = MagicMock()
    mock_execution_object._route_job_after_event = MagicMock()

    mock_execution_object._case_event_is_departure_or_preemption(mock_event)

    mock_execution_object._route_job_after_event.assert_called_once_with(mock_event)
    mock_execution_object._add_next_departure_event.assert_called_once()