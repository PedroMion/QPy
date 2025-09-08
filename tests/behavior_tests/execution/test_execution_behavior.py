import pytest
import heapq


from unittest.mock import MagicMock
from qpy.distribution import Distribution
from qpy.execution import Execution
from qpy.event import Event
from qpy.job import Job
from qpy.network import OpenNetwork
from qpy.results import SimulationResults
from qpy.queue_discipline import QueueDiscipline


TIME = 10
WARMUP = 0
TIME_UNIT = "seconds"

JOB_ID = 1
JOB_PRIORITY = 1
JOB_ARRIVAL_TIME = 1

JOB_ID_2 = 2
JOB_ARRIVAL_TIME_2 = 1.5
JOB_PRIORITY_2 = 2

JOB_ID_3 = 3
JOB_ARRIVAL_TIME_3 = 2
JOB_PRIORITY_3 = 1

SERVER_ID = 0
EVENT_ID = 0
SERVICE_TIME = 2

PREEMPTION_TIME = 1


@pytest.fixture
def job_test_object_1():
    return Job(JOB_ID, JOB_ARRIVAL_TIME, SERVER_ID, JOB_PRIORITY)

@pytest.fixture
def job_test_object_2():
    return Job(JOB_ID_2, JOB_ARRIVAL_TIME_2, SERVER_ID, JOB_PRIORITY_2)

@pytest.fixture
def job_test_object_3():
    return Job(JOB_ID_3, JOB_ARRIVAL_TIME_3, SERVER_ID, JOB_PRIORITY_3)

@pytest.fixture
def mock_network_priority():
    network = OpenNetwork()
    network.add_server(Distribution.constant(SERVICE_TIME), QueueDiscipline.priority_queue(with_preemption=True))

    return network

@pytest.fixture
def mock_network_round_robin():
    network = OpenNetwork()
    network.add_server(Distribution.constant(SERVICE_TIME), QueueDiscipline.round_robin(preemption_time=PREEMPTION_TIME))

    return network

@pytest.fixture
def execution_with_priority_test_object(mock_network_priority):
    queue = []

    return Execution(time=TIME, warmup=WARMUP, queue=queue, network_configuration=mock_network_priority, time_unit=TIME_UNIT)

@pytest.fixture
def execution_with_round_robin_test_object(mock_network_round_robin):
    queue = []

    return Execution(time=TIME, warmup=WARMUP, queue=queue, network_configuration=mock_network_round_robin, time_unit=TIME_UNIT)


"""Testando preempção quando caso é prioridade"""
def test_execute_behavior_when_queue_is_priority(execution_with_priority_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(JOB_ARRIVAL_TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(JOB_ARRIVAL_TIME_2, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(JOB_ARRIVAL_TIME_3, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)

    heapq.heappush(execution_with_priority_test_object.event_queue, (JOB_ARRIVAL_TIME, EVENT_ID, event))
    heapq.heappush(execution_with_priority_test_object.event_queue, (JOB_ARRIVAL_TIME_2, EVENT_ID + 1, second_event))
    heapq.heappush(execution_with_priority_test_object.event_queue, (JOB_ARRIVAL_TIME_3, EVENT_ID + 2, third_event))

    results = execution_with_priority_test_object.execute()

    assert results.priority_metrics[2].get_number_of_processed_jobs() == 1
    assert results.priority_metrics[2].get_mean_queue_time() == 0
    assert results.priority_metrics[2].get_mean_time_in_system() == SERVICE_TIME

    assert results.priority_metrics[1].get_number_of_processed_jobs() == 2

"""Testando round robin quando há preempção"""
def test_execute_behavior_when_queue_is_round_robin(execution_with_round_robin_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(JOB_ARRIVAL_TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(JOB_ARRIVAL_TIME_2, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(JOB_ARRIVAL_TIME_3, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)
    execution_with_round_robin_test_object.event_count = 3

    heapq.heappush(execution_with_round_robin_test_object.event_queue, (JOB_ARRIVAL_TIME, EVENT_ID, event))
    heapq.heappush(execution_with_round_robin_test_object.event_queue, (JOB_ARRIVAL_TIME_2, EVENT_ID + 1, second_event))
    heapq.heappush(execution_with_round_robin_test_object.event_queue, (JOB_ARRIVAL_TIME_3, EVENT_ID + 2, third_event))

    results = execution_with_round_robin_test_object.execute()

    assert results.jobs[JOB_ID].queue_times_per_server[SERVER_ID] == 2
    assert results.jobs[JOB_ID].total_time_per_server[SERVER_ID] == 4

    assert results.jobs[JOB_ID_2].queue_times_per_server[SERVER_ID] == 2.5
    assert results.jobs[JOB_ID_2].total_time_per_server[SERVER_ID] == 4.5

    assert results.jobs[JOB_ID_3].queue_times_per_server[SERVER_ID] == 3
    assert results.jobs[JOB_ID_3].total_time_per_server[SERVER_ID] == 5