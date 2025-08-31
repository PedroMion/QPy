import pytest


from unittest.mock import MagicMock
from qpy.distribution import Distribution
from qpy.job import Job
from qpy.server import ServerExecution
from qpy.queue_discipline import QueueDiscipline


MOCK_JOB = MagicMock()
PREEMPTION_TIME = 1.5
JOB_SIZE = 2
CURRENT_TIME = 1
ZERO_VALUE = 0
NEGATIVE_VALUE = -1

NEW_JOB_SIZE = 1
HIGHER_PRIORITY = 3
LOWER_PRIORITY = 1


@pytest.fixture
def fcfs_test_object():
    return ServerExecution(service_distribution=Distribution.constant(value=1), queue=QueueDiscipline.fcfs())

@pytest.fixture
def lcfs_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.lcfs())

@pytest.fixture
def srt_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.srt(with_preemption=True))

@pytest.fixture
def round_robin_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.round_robin(PREEMPTION_TIME))

@pytest.fixture
def priority_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.priority_queue(with_preemption=True))


"""
Particionamento do espaço de entrada para função _remaining_time_for_current_job() da classe ServerExecution utilizando Each Choice Coverage:
    time: < time_current_execution_started | > time_current_execution_started
"""

"""time < time_current_execution_started (Válido)"""
def test_remaining_time_for_current_job_when_time_is_invalid_should_raise_exception(fcfs_test_object):
    fcfs_test_object.time_current_execution_started = CURRENT_TIME

    with pytest.raises(ValueError):
        fcfs_test_object._remaining_time_for_current_job(ZERO_VALUE)

"""time >= time_current_execution_started (Válido)"""
def test_remaining_time_for_current_job_when_time_is_valid_should_return_remaining_time(fcfs_test_object):
    fcfs_test_object.time_current_execution_started = ZERO_VALUE
    fcfs_test_object.current_job_size = JOB_SIZE

    expected_value = JOB_SIZE - (CURRENT_TIME - ZERO_VALUE)

    response = fcfs_test_object._remaining_time_for_current_job(CURRENT_TIME)

    assert expected_value == response


"""
Particionamento do espaço de entrada para função _should_preempt() da classe ServerExecution utilizando Each Choice Coverage:
    queue_discipline: SRT caso com preempção | SRT caso sem preempção | Priority caso com preempção | Priority caso sem preempção | Outra
"""

"""queue_discipline = SRT caso com preempção (Válido)"""
def test_should_preempt_when_queue_discipline_is_srt_and_new_job_is_smaller_should_return_true(srt_test_object):
    srt_test_object._remaining_time_for_current_job = MagicMock()
    srt_test_object._remaining_time_for_current_job.return_value = JOB_SIZE
    
    result = srt_test_object._should_preempt(MOCK_JOB, NEW_JOB_SIZE, CURRENT_TIME)
    
    assert result is True

"""queue_discipline = SRT caso sem preempção (Válido)"""
def test_should_preempt_when_queue_discipline_is_srt_and_new_job_is_not_smaller_should_return_false(srt_test_object):
    srt_test_object._remaining_time_for_current_job = MagicMock()
    srt_test_object._remaining_time_for_current_job.return_value = NEW_JOB_SIZE
    
    result = srt_test_object._should_preempt(MOCK_JOB, JOB_SIZE, CURRENT_TIME)
    
    assert result is False

"""queue_discipline = Priority caso com preempção (Válido)"""
def test_should_preempt_when_queue_discipline_is_priority_and_new_job_has_greater_priority_should_return_true(priority_test_object):
    MOCK_JOB.priority = HIGHER_PRIORITY
    priority_test_object.current_job_being_executed = MagicMock()
    priority_test_object.current_job_being_executed.priority = LOWER_PRIORITY
    
    result = priority_test_object._should_preempt(MOCK_JOB, JOB_SIZE, CURRENT_TIME)

    assert result == True

"""queue_discipline = Priority caso sem preempção (Válido)"""
def test_should_preempt_when_queue_discipline_is_priority_and_new_job_has_smaller_priority_should_return_true(priority_test_object):
    MOCK_JOB.priority = LOWER_PRIORITY
    priority_test_object.current_job_being_executed = MagicMock()
    priority_test_object.current_job_being_executed.priority = HIGHER_PRIORITY
    
    result = priority_test_object._should_preempt(MOCK_JOB, JOB_SIZE, CURRENT_TIME)

    assert result == False

"""queue_discipline = Outra (Válido)"""
def test_should_preempt_when_queue_discipline_is_not_srt_and_priority_should_return_false(fcfs_test_object):    
    result = fcfs_test_object._should_preempt(MOCK_JOB, JOB_SIZE, CURRENT_TIME)

    assert result == False


"""
Particionamento do espaço de entrada para função is_next_event_departure() da classe ServerExecution utilizando Each Choice Coverage:
    Disciplina: RR quando próximo evento não é preempção | RR quando próximo evento é preempção | Outra
"""

"""queue_discipline = RR quando próximo evento não é preempção (Válido)"""
def test_is_next_event_departure_when_queue_discipline_is_rr_and_next_event_is_not_preemption_should_return_true(round_robin_test_object):
    round_robin_test_object._execute_new_job(MOCK_JOB, NEW_JOB_SIZE, PREEMPTION_TIME)

    assert round_robin_test_object.is_next_event_departure() is True

"""queue_discipline = RR quando próximo evento é preempção (Válido)"""
def test_is_next_event_departure_when_queue_discipline_is_rr_and_next_event_is_preemption_should_return_false(round_robin_test_object):
    round_robin_test_object._execute_new_job(MOCK_JOB, JOB_SIZE, PREEMPTION_TIME)

    assert round_robin_test_object.is_next_event_departure() is False

"""queue_discipline = Outra (Válido)"""
def test_is_next_event_departure_when_queue_discipline_is_not_rr_should_return_true(fcfs_test_object):
    fcfs_test_object._execute_new_job(MOCK_JOB, JOB_SIZE, CURRENT_TIME)
    
    assert fcfs_test_object.is_next_event_departure() is True