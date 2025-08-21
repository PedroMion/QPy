import pytest


from qpy.distribution import Distribution
from qpy.job import Job
from qpy.server import ServerExecution
from qpy.queue_discipline import QueueDiscipline


MOCK_JOB = Job(1, 1, 1, 1)
JOB_SIZE = 2
TIME = 1
ZERO = 0
NEGATIVE_VALUE = -1


def fcfs_test_object():
    return ServerExecution(service_distribution=Distribution.constant(value=1), queue=QueueDiscipline.fcfs())

def lcfs_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.lcfs())

def srt_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.srt(with_preemption=True))

def round_robin_test_object():
    return ServerExecution(service_distribution=Distribution.constant(1), queue=QueueDiscipline.round_robin(0.5))

def get_all_test_objects():
    return [fcfs_test_object(), lcfs_test_object(), srt_test_object(), round_robin_test_object()]