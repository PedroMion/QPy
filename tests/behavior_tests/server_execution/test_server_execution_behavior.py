import pytest


from unittest.mock import MagicMock
from qpy.distribution import Distribution
from qpy.event import Event
from qpy.job import Job
from qpy.server import Server
from qpy.queue_discipline import QueueDiscipline


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
DISTRIBUTION_TIME = 2
PREEMPTION_TIME = 1

TIME = 1
SECOND_TIME = 1.5
THIRD_TIME = 2
EVENT_ID = 0

SRT_FIRST_TIME = 3
SRT_SECOND_TIME = 1
SRT_THIRD_TIME = 1


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
def round_robin_test_object():
    return Server(SERVER_ID, Distribution.constant(DISTRIBUTION_TIME), QueueDiscipline.round_robin(PREEMPTION_TIME))

@pytest.fixture
def priority_with_preemption_test_object():
    return Server(SERVER_ID, Distribution.constant(DISTRIBUTION_TIME), QueueDiscipline.priority_queue(with_preemption=True))

@pytest.fixture
def priority_without_preemption_test_object():
    return Server(SERVER_ID, Distribution.constant(DISTRIBUTION_TIME), QueueDiscipline.priority_queue(with_preemption=False))

@pytest.fixture
def srt_with_preemption_test_object():
    return Server(SERVER_ID, Distribution.constant(DISTRIBUTION_TIME), QueueDiscipline.srt(with_preemption=True))

@pytest.fixture
def srt_without_preemption_test_object():
    return Server(SERVER_ID, Distribution.constant(DISTRIBUTION_TIME), QueueDiscipline.srt(with_preemption=False))


"""Testando preempção Round Robin"""
def test_round_robin_preemption_when_three_jobs_in_server_should_switch_jobs(round_robin_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(SECOND_TIME, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(THIRD_TIME, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)

    round_robin_test_object.job_arrival(event=event)
    round_robin_test_object.job_arrival(event=second_event)
    round_robin_test_object.job_arrival(event=third_event)
    round_robin_test_object.finish_execution(TIME + PREEMPTION_TIME, is_preemption=True)

    assert round_robin_test_object.server_execution.current_job_being_executed == job_test_object_2
    assert round_robin_test_object.server_execution.current_job_size == DISTRIBUTION_TIME
    assert round_robin_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME, job_test_object_3)
    assert round_robin_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME - PREEMPTION_TIME, job_test_object_1)

"""Testando fila de prioridade com preempção"""
def test_priority_preemption_when_second_job_has_higher_priority_should_switch(priority_with_preemption_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(SECOND_TIME, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(THIRD_TIME, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)

    priority_with_preemption_test_object.job_arrival(event=event)
    priority_with_preemption_test_object.job_arrival(event=second_event)
    priority_with_preemption_test_object.job_arrival(event=third_event)

    assert priority_with_preemption_test_object.server_execution.current_job_being_executed == job_test_object_2
    assert priority_with_preemption_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME - (SECOND_TIME - TIME), job_test_object_1)
    assert priority_with_preemption_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME, job_test_object_3)

"""Tetando fila de prioridade sem preempção"""
def test_priority_without_preemption_when_second_job_has_higher_priority_should_not_switch(priority_without_preemption_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(SECOND_TIME, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(THIRD_TIME, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)

    priority_without_preemption_test_object.job_arrival(event=event)
    priority_without_preemption_test_object.job_arrival(event=second_event)
    priority_without_preemption_test_object.job_arrival(event=third_event)

    assert priority_without_preemption_test_object.server_execution.current_job_being_executed == job_test_object_1
    assert priority_without_preemption_test_object.server_execution._remaining_time_for_current_job(THIRD_TIME) == (THIRD_TIME - TIME)
    assert priority_without_preemption_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME, job_test_object_2)
    assert priority_without_preemption_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME, job_test_object_3)

"""Testando SRT com preempção"""
def test_srt_with_preemption_when_second_job_has_smaller_time_should_preempt(srt_with_preemption_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(SECOND_TIME, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(THIRD_TIME, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)

    srt_with_preemption_test_object.server_execution.service_distribution = MagicMock()

    srt_with_preemption_test_object.server_execution.service_distribution.sample.return_value = SRT_FIRST_TIME
    srt_with_preemption_test_object.job_arrival(event=event)

    srt_with_preemption_test_object.server_execution.service_distribution.sample.return_value = SRT_SECOND_TIME
    srt_with_preemption_test_object.job_arrival(event=second_event)

    assert srt_with_preemption_test_object.server_execution.current_job_being_executed == job_test_object_2

    srt_with_preemption_test_object.server_execution.service_distribution.sample.return_value = SRT_THIRD_TIME
    srt_with_preemption_test_object.job_arrival(event=third_event)

    assert srt_with_preemption_test_object.server_execution.current_job_being_executed == job_test_object_2
    assert srt_with_preemption_test_object.server_execution.queue.first_in_line() == (SRT_THIRD_TIME, job_test_object_3)
    assert srt_with_preemption_test_object.server_execution.queue.first_in_line() == (SRT_FIRST_TIME - (SECOND_TIME - TIME), job_test_object_1)

"""Testando SRT sem preempção"""
def test_srt_without_preemption_when_second_job_has_smaller_time_should_not_preempt(srt_without_preemption_test_object, job_test_object_1, job_test_object_2, job_test_object_3):
    event = Event(TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(SECOND_TIME, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)
    third_event = Event(THIRD_TIME, EVENT_ID + 2, 'arrival', job_test_object_3, SERVER_ID)

    srt_without_preemption_test_object.server_execution.service_distribution = MagicMock()

    srt_without_preemption_test_object.server_execution.service_distribution.sample.return_value = SRT_FIRST_TIME
    srt_without_preemption_test_object.job_arrival(event=event)

    srt_without_preemption_test_object.server_execution.service_distribution.sample.return_value = SRT_SECOND_TIME
    srt_without_preemption_test_object.job_arrival(event=second_event)

    assert srt_without_preemption_test_object.server_execution.current_job_being_executed == job_test_object_1

    srt_without_preemption_test_object.server_execution.service_distribution.sample.return_value = SRT_THIRD_TIME
    srt_without_preemption_test_object.job_arrival(event=third_event)

    assert srt_without_preemption_test_object.server_execution.queue.first_in_line() == (SRT_SECOND_TIME, job_test_object_2)
    assert srt_without_preemption_test_object.server_execution.queue.first_in_line() == (SRT_THIRD_TIME, job_test_object_3)