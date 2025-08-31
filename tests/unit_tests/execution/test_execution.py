import heapq
import pytest


from unittest.mock import MagicMock
from qpy.distribution import Distribution
from qpy.execution import Execution
from qpy.network import OpenNetwork


TOTAL_TIME = 10
TIME_UNIT = 'seconds'
VALID_TIME = 5
ZERO_VALUE = 0

ARRIVAL_EVENT = "arrival"
DEPARTURE_EVENT = "departure"

CONSTANT_DISTRIBUTION_VALUE = 5
MOCK_DISTRIBUTION = Distribution.constant(value=CONSTANT_DISTRIBUTION_VALUE)
SERVER_ID = 0


@pytest.fixture
def mock_event():
    canceled_event = MagicMock()
    canceled_event.canceled = False
    canceled_event.current_time = VALID_TIME
    canceled_event.server_id = SERVER_ID
    canceled_event.type = ARRIVAL_EVENT

    return canceled_event

@pytest.fixture
def mock_execution_object():
    network = OpenNetwork()
    network.add_server(MOCK_DISTRIBUTION)
    network.add_entry_point(SERVER_ID, MOCK_DISTRIBUTION)
    
    execution = Execution(time=TOTAL_TIME, warmup=ZERO_VALUE, queue=[], network_configuration=network, time_unit=TIME_UNIT)

    execution._case_event_is_arrival = MagicMock()
    execution._case_event_is_departure_or_preemption = MagicMock()

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
    heapq.heappush(mock_execution_object.event_queue, (0, 0, mock_event))

    mock_execution_object.execute()

    mock_execution_object._case_event_is_arrival.assert_not_called()
    mock_execution_object._case_event_is_departure_or_preemption.assert_not_called()


"""current_time <= time | queue Not Empty (Válido)"""
def test_execute_when_event_is_arrival_should_call_case_arrival(mock_execution_object, mock_event):
    heapq.heappush(mock_execution_object.event_queue, (0, 0, mock_event))

    mock_execution_object.execute()

    mock_execution_object._case_event_is_arrival.assert_called_once_with(mock_event)
    assert mock_execution_object.current_time == VALID_TIME


"""current_time <= time | queue Not Empty (Válido)"""
def test_execute_when_event_is_departure_should_call_case_departure(mock_execution_object, mock_event):
    mock_event.type = DEPARTURE_EVENT
    heapq.heappush(mock_execution_object.event_queue, (0, 0, mock_event))

    mock_execution_object.execute()

    mock_execution_object._case_event_is_departure_or_preemption.assert_called_once_with(mock_event)
    assert mock_execution_object.current_time == VALID_TIME
