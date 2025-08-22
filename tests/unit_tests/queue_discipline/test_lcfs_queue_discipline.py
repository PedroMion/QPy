import pytest


from collections import deque
from qpy.job import Job
from qpy.queue_discipline import QueueDiscipline


FIRST_JOB_ARRIVAL_TIME = 0
FIRST_JOB_ID = 1
FIRST_JOB_SERVICE_TIME = 10

SECOND_JOB_ARRIVAL_TIME = 5
SECOND_JOB_ID = 2
SECOND_JOB_SERVICE_TIME = 5

THIRD_JOB_ARRIVAL_TIME = 10
THIRD_JOB_ID = 3
THIRD_JOB_SERVICE_TIME = 1

SERVER_ID = 1
PRIORITY = 1

FIRST_JOB = Job(FIRST_JOB_ID, FIRST_JOB_ARRIVAL_TIME, SERVER_ID, PRIORITY)
SECOND_JOB = Job(SECOND_JOB_ID, SECOND_JOB_ARRIVAL_TIME, SERVER_ID, PRIORITY)
THIRD_JOB = Job(THIRD_JOB_ID, THIRD_JOB_ARRIVAL_TIME, SERVER_ID, PRIORITY)

@pytest.fixture
def lcfs_empty_queue():
    return QueueDiscipline.lcfs()

@pytest.fixture
def lcfs_queue_with_jobs():
    queue = QueueDiscipline.lcfs()

    queue.insert(job=FIRST_JOB, service_time=FIRST_JOB_SERVICE_TIME)
    queue.insert(job=SECOND_JOB, service_time=SECOND_JOB_SERVICE_TIME)

    return queue


"""
Particionamento do espaço de entrada para função insert() da classe LastComeFirstServed utilizando Each Choice Coverage:
    job: Válido | None
    service_time: Válido | None
"""

"""job Válido | service_time Válido (Válido)"""
def test_insert_when_both_objects_are_valid_should_update_queue(lcfs_empty_queue):
    expected_queue = deque()
    expected_queue.append((FIRST_JOB_SERVICE_TIME, FIRST_JOB))

    lcfs_empty_queue.insert(job=FIRST_JOB, service_time=FIRST_JOB_SERVICE_TIME)

    assert lcfs_empty_queue.queue == expected_queue

"""job Inválido | service_time Válido (Inválido)"""
def test_insert_when_job_is_invalid_should_not_update_queue(lcfs_empty_queue):
    expected_queue = deque()

    lcfs_empty_queue.insert(job=None, service_time=FIRST_JOB_SERVICE_TIME)

    assert lcfs_empty_queue.queue == expected_queue

"""job Válido | service_time Inválido (Inválido)"""
def test_insert_when_service_time_is_invalid_should_not_update_queue(lcfs_empty_queue):
    expected_queue = deque()

    lcfs_empty_queue.insert(job=FIRST_JOB, service_time=None)

    assert lcfs_empty_queue.queue == expected_queue


"""
Particionamento do espaço de entrada para função first_in_line() da classe LastComeFirstServed utilizando Each Choice Coverage:
    queue: Empty | Not Empty
"""

"""queue Empty (Válido)"""
def test_first_in_line_when_queue_is_empty_should_return_none(lcfs_empty_queue):
    assert lcfs_empty_queue.first_in_line() == None

"""queue Not Empty (Válido)"""
def test_first_in_line_when_queue_is_not_empty_should_return_tuple(lcfs_queue_with_jobs):
    expected_response = (SECOND_JOB_SERVICE_TIME, SECOND_JOB)

    assert lcfs_queue_with_jobs.first_in_line() == expected_response


"""
Não há particionamento do espaço de entrada para função with_preemption() da classe LastComeFirstServed
"""
def test_with_preemption_should_return_false(lcfs_queue_with_jobs):
    assert lcfs_queue_with_jobs.with_preemption() == False