import pytest
from qpy.queue_discipline import Discipline, FirstComeFirstServed, LastComeFirstServed, PriorityQueue, QueueDiscipline, RoundRobin, ShortestRemainingTime


INVALID_PREEMPTION_TIME = -1
ZERO_VALUE = 0
VALID_PREEMPTION_TIME = 1


"""
Não há particionamento do espaço de entrada para função fcfs() da classe QueueDiscipline
"""
def test_fcfs_generation_should_return_proper_object():
    queue = QueueDiscipline.fcfs()

    assert isinstance(queue, FirstComeFirstServed)
    assert queue.discipline == Discipline.FCFS


"""
Não há particionamento do espaço de entrada para função lcfs() da classe QueueDiscipline
"""
def test_lcfs_generation_should_return_proper_object():
    queue = QueueDiscipline.lcfs()

    assert isinstance(queue, LastComeFirstServed)
    assert queue.discipline == Discipline.LCFS


"""
Particionamento do espaço de entrada para função srt() da classe QueueDiscipline utilizando Each Choice Coverage:
    with_preemption: True | False
"""

"""with_preemption True (Válido)"""
def test_srt_generation_when_preemption_is_true_should_return_proper_object():
    queue = QueueDiscipline.srt(with_preemption=True)

    assert isinstance(queue, ShortestRemainingTime)
    assert queue.discipline == Discipline.SRT
    assert queue.with_preemption()

"""with_preemption False (Válido)"""
def test_srt_generation_when_preemption_is_false_should_return_proper_object():
    queue = QueueDiscipline.srt(with_preemption=False)

    assert isinstance(queue, ShortestRemainingTime)
    assert queue.discipline == Discipline.SRT
    assert queue.with_preemption() == False


"""
Particionamento do espaço de entrada para função round_robin() da classe QueueDiscipline utilizando Each Choice Coverage:
    preemption_time: 0 | < 0 | > 0
"""

"""preemption_time = 0 (Inválido)"""
def test_round_robin_generation_when_preemption_time_is_zero_should_raise_exception():
    with pytest.raises(ValueError):
        QueueDiscipline.round_robin(preemption_time=ZERO_VALUE)

"""preemption_time < 0 (Inválido)"""
def test_round_robin_generation_when_preemption_time_is_negative_should_raise_exception():
    with pytest.raises(ValueError):
        QueueDiscipline.round_robin(preemption_time=INVALID_PREEMPTION_TIME)

"""preemption_time > 0 (Válido)"""
def test_round_robin_generation_when_preemption_time_is_valid_should_return_proper_object():
    queue = QueueDiscipline.round_robin(preemption_time=VALID_PREEMPTION_TIME)

    assert isinstance(queue, RoundRobin)
    assert queue.discipline == Discipline.RR


"""
Particionamento do espaço de entrada para função priority_queue() da classe QueueDiscipline utilizando Each Choice Coverage:
    with_preemption: True | False
"""

"""with_preemption True (Válido)"""
def test_priority_queue_generation_when_preemption_is_true_should_return_proper_object():
    queue = QueueDiscipline.priority_queue(with_preemption=True)

    assert isinstance(queue, PriorityQueue)
    assert queue.discipline == Discipline.PRIORITY
    assert queue.with_preemption()

"""with_preemption False (Válido)"""
def test_priority_queue_generation_when_preemption_is_false_should_return_proper_object():
    queue = QueueDiscipline.priority_queue(with_preemption=False)

    assert isinstance(queue, PriorityQueue)
    assert queue.discipline == Discipline.PRIORITY
    assert queue.with_preemption() == False