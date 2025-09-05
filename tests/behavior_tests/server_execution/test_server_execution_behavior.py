import pytest


from qpy.distribution import Distribution
from qpy.event import Event
from qpy.job import Job
from qpy.server import Server
from qpy.queue_discipline import QueueDiscipline


JOB_ID = 1
JOB_PRIORITY = 2
JOB_SIZE = 3
JOB_ARRIVAL_TIME = 1

JOB_ID_2 = 2
JOB_ARRIVAL_TIME_2 = 1.5

SERVER_ID = 0
DISTRIBUTION_TIME = 2
PREEMPTION_TIME = 1

TIME = 1
SECOND_TIME = 1.5
EVENT_ID = 0


@pytest.fixture
def job_test_object_1():
    return Job(JOB_ID, JOB_ARRIVAL_TIME, SERVER_ID, JOB_PRIORITY)

@pytest.fixture
def job_test_object_2():
    return Job(JOB_ID_2, JOB_ARRIVAL_TIME_2, SERVER_ID, JOB_PRIORITY)

@pytest.fixture
def round_robin_test_object():
    return Server(SERVER_ID, Distribution.constant(DISTRIBUTION_TIME), QueueDiscipline.round_robin(PREEMPTION_TIME))


def test_round_robin_preemption_when_two_jobs_in_server_should_switch_jobs(round_robin_test_object, job_test_object_1, job_test_object_2):
    event = Event(TIME, EVENT_ID, 'arrival', job_test_object_1, SERVER_ID)
    second_event = Event(SECOND_TIME, EVENT_ID + 1, 'arrival', job_test_object_2, SERVER_ID)

    round_robin_test_object.job_arrival(event=event)
    round_robin_test_object.job_arrival(event=second_event)
    round_robin_test_object.finish_execution(TIME + PREEMPTION_TIME, is_preemption=True)

    assert round_robin_test_object.server_execution.current_job_being_executed == job_test_object_2
    assert round_robin_test_object.server_execution.current_job_size == 2
    assert round_robin_test_object.server_execution.queue.first_in_line() == (DISTRIBUTION_TIME - PREEMPTION_TIME, job_test_object_1)