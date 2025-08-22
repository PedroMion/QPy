from qpy.job import Job
from qpy.queue_discipline import QueueDiscipline


FIRST_JOB_ARRIVAL_TIME = 0
FIRST_JOB_ID = 1
FIRST_JOB_SERVICE_TIME = 10
FIRST_JOB_PRIORITY = 1

SECOND_JOB_ARRIVAL_TIME = 5
SECOND_JOB_ID = 2
SECOND_JOB_SERVICE_TIME = 1
SECOND_JOB_PRIORITY = 2

THIRD_JOB_ARRIVAL_TIME = 10
THIRD_JOB_ID = 3
THIRD_JOB_SERVICE_TIME = 5
THIRD_JOB_PRIORITY = 1

SERVER_ID = 1
PRIORITY = 1

FIRST_JOB = Job(FIRST_JOB_ID, FIRST_JOB_ARRIVAL_TIME, SERVER_ID, FIRST_JOB_PRIORITY)
FIRST_JOB_EXPECTED_RESULT = (FIRST_JOB_SERVICE_TIME, FIRST_JOB)

SECOND_JOB = Job(SECOND_JOB_ID, SECOND_JOB_ARRIVAL_TIME, SERVER_ID, SECOND_JOB_PRIORITY)
SECOND_JOB_EXPECTED_RESULT = (SECOND_JOB_SERVICE_TIME, SECOND_JOB)

THIRD_JOB = Job(THIRD_JOB_ID, THIRD_JOB_ARRIVAL_TIME, SERVER_ID, THIRD_JOB_PRIORITY)
THIRD_JOB_EXPECTED_RESULT = (THIRD_JOB_SERVICE_TIME, THIRD_JOB)


"""Testando comportamento da classe que implementa fila FCFS"""
def test_fcfs_queue():
    fcfs_queue = QueueDiscipline.fcfs()

    fcfs_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)
    fcfs_queue.insert(SECOND_JOB, SECOND_JOB_SERVICE_TIME)
    fcfs_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert fcfs_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    assert fcfs_queue.first_in_line() == SECOND_JOB_EXPECTED_RESULT
    
    fcfs_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)

    assert fcfs_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    assert fcfs_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    assert fcfs_queue.first_in_line() == None

"""Testando comportamento da classe que implementa fila LCFS"""
def test_lcfs_queue():
    lcfs_queue = QueueDiscipline.lcfs()

    lcfs_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)
    lcfs_queue.insert(SECOND_JOB, SECOND_JOB_SERVICE_TIME)
    lcfs_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert lcfs_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    assert lcfs_queue.first_in_line() == SECOND_JOB_EXPECTED_RESULT
    
    lcfs_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert lcfs_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    assert lcfs_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    assert lcfs_queue.first_in_line() == None

"""Testando comportamento da classe que implementa fila SRT"""
def test_srt_queue():
    srt_queue = QueueDiscipline.srt()

    srt_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)
    srt_queue.insert(SECOND_JOB, SECOND_JOB_SERVICE_TIME)
    srt_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert srt_queue.first_in_line() == SECOND_JOB_EXPECTED_RESULT
    assert srt_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    
    srt_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert srt_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    assert srt_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    assert srt_queue.first_in_line() == None

    srt_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)
    srt_queue.insert(SECOND_JOB, FIRST_JOB_SERVICE_TIME)

    assert srt_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT

"""Testando comportamento da classe que implementa fila RoundRobin"""
def test_round_robin_queue():
    round_robin_queue = QueueDiscipline.round_robin(preemption_time=5)

    round_robin_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)
    round_robin_queue.insert(SECOND_JOB, SECOND_JOB_SERVICE_TIME)
    round_robin_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert round_robin_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    assert round_robin_queue.first_in_line() == SECOND_JOB_EXPECTED_RESULT
    
    round_robin_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)

    assert round_robin_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    assert round_robin_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    assert round_robin_queue.first_in_line() == None

"""Testando comportamento da classe que implementa fila de prioridade"""
def test_priority_queue():
    priority_queue = QueueDiscipline.priority_queue()

    priority_queue.insert(FIRST_JOB, FIRST_JOB_SERVICE_TIME)
    priority_queue.insert(SECOND_JOB, SECOND_JOB_SERVICE_TIME)
    priority_queue.insert(THIRD_JOB, THIRD_JOB_SERVICE_TIME)

    assert priority_queue.first_in_line() == SECOND_JOB_EXPECTED_RESULT
    assert priority_queue.first_in_line() == FIRST_JOB_EXPECTED_RESULT
    
    priority_queue.insert(SECOND_JOB, SECOND_JOB_SERVICE_TIME)

    assert priority_queue.first_in_line() == SECOND_JOB_EXPECTED_RESULT
    assert priority_queue.first_in_line() == THIRD_JOB_EXPECTED_RESULT
    assert priority_queue.first_in_line() == None