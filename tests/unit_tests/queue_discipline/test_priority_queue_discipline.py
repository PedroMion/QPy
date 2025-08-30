import heapq, pytest


from qpy.job import Job
from qpy.queue_discipline import QueueDiscipline


FIRST_JOB_ARRIVAL_TIME = 0
FIRST_JOB_ID = 1
FIRST_JOB_SERVICE_TIME = 10
FIRST_JOB_PRIORITY = 1

SECOND_JOB_ARRIVAL_TIME = 5
SECOND_JOB_ID = 2
SECOND_JOB_SERVICE_TIME = 5
SECOND_JOB_PRIORITY = 2

THIRD_JOB_ARRIVAL_TIME = 10
THIRD_JOB_ID = 3
THIRD_JOB_SERVICE_TIME = 1
THIRD_JOB_PRIORITY = 1

SERVER_ID = 1

FIRST_JOB = Job(FIRST_JOB_ID, FIRST_JOB_ARRIVAL_TIME, SERVER_ID, FIRST_JOB_PRIORITY)
SECOND_JOB = Job(SECOND_JOB_ID, SECOND_JOB_ARRIVAL_TIME, SERVER_ID, SECOND_JOB_PRIORITY)
THIRD_JOB = Job(THIRD_JOB_ID, THIRD_JOB_ARRIVAL_TIME, SERVER_ID, THIRD_JOB_PRIORITY)

@pytest.fixture
def priority_empty_queue():
    return QueueDiscipline.priority_queue()

@pytest.fixture
def priority_queue_with_jobs_with_preemption():
    queue = QueueDiscipline.priority_queue(with_preemption = True)

    queue.insert(job=FIRST_JOB, service_time=FIRST_JOB_SERVICE_TIME)
    queue.insert(job=SECOND_JOB, service_time=SECOND_JOB_SERVICE_TIME)

    return queue

@pytest.fixture
def priority_queue_with_jobs_without_preemption():
    queue = QueueDiscipline.priority_queue(with_preemption = False)

    queue.insert(job=FIRST_JOB, service_time=FIRST_JOB_SERVICE_TIME)
    queue.insert(job=SECOND_JOB, service_time=SECOND_JOB_SERVICE_TIME)

    return queue


"""
Particionamento do espaço de entrada para função insert() da classe PriorityQueue utilizando Each Choice Coverage:
    job: Válido | None
    service_time: Válido | None
"""

"""job Válido | service_time Válido (Válido)"""
def test_insert_when_both_objects_are_valid_should_update_queue(priority_empty_queue):
    expected_queue = []
    heapq.heappush(expected_queue, (-FIRST_JOB_PRIORITY, FIRST_JOB.arrival_time_at_current_server, FIRST_JOB_SERVICE_TIME, FIRST_JOB))

    priority_empty_queue.insert(job=FIRST_JOB, service_time=FIRST_JOB_SERVICE_TIME)

    assert priority_empty_queue._queue == expected_queue

"""job Inválido | service_time Válido (Inválido)"""
def test_insert_when_job_is_invalid_should_not_update_queue(priority_empty_queue):
    expected_queue = []

    priority_empty_queue.insert(job=None, service_time=FIRST_JOB_SERVICE_TIME)

    assert priority_empty_queue._queue == expected_queue

"""job Válido | service_time Inválido (Inválido)"""
def test_insert_when_service_time_is_invalid_should_not_update_queue(priority_empty_queue):
    expected_queue = []

    priority_empty_queue.insert(job=FIRST_JOB, service_time=None)

    assert priority_empty_queue._queue == expected_queue


"""
Particionamento do espaço de entrada para função first_in_line() da classe PriorityQueue utilizando Each Choice Coverage:
    queue: Empty | Not Empty
"""

"""queue Empty (Válido)"""
def test_first_in_line_when_queue_is_empty_should_return_none(priority_empty_queue):
    assert priority_empty_queue.first_in_line() == None

"""queue Not Empty (Válido)"""
def test_first_in_line_when_queue_is_not_empty_should_return_tuple(priority_queue_with_jobs_without_preemption):
    expected_response = (SECOND_JOB_SERVICE_TIME, SECOND_JOB)

    assert priority_queue_with_jobs_without_preemption.first_in_line() == expected_response


"""
Particionamento do espaço de entrada para função with_preemption() da classe PriorityQueue utilizando Each Choice Coverage:
    with_preemption: False | True"""

"""with_preemption = False"""
def test_with_preemption_when_preemption_is_not_being_used_should_return_false(priority_queue_with_jobs_without_preemption):
    assert priority_queue_with_jobs_without_preemption.with_preemption() == False

"""with_preemption = True"""
def test_with_preemption_when_preemption_is_being_used_should_return_true(priority_queue_with_jobs_with_preemption):
    assert priority_queue_with_jobs_with_preemption.with_preemption() == True