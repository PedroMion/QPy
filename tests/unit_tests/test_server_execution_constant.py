import pytest


from qpy.distribution import Distribution
from qpy.job import Job
from qpy.server import ServerExecution
from qpy.queue_discipline import QueueDiscipline


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

def test_reset_configuration_when_configuration_is_filled_should_clear_config():
    for test_object in get_all_test_objects():
        test_object.current_job_being_executed = Job(1, 1, 1, 1)
        test_object.current_job_size = 2
        test_object.time_current_execution_started = 1

        test_object.reset_execution_configuration()

        assert test_object.current_job_being_executed == None
        assert test_object.time_current_execution_started == 0
        assert test_object.current_job_size == 0

def test_execute_new_job_when_information_is_valid_should_update_variables():
    for test_object in get_all_test_objects():
        mock_job = Job(1, 1, 1, 1)
        mock_job_size = 2
        time = 1

        test_object.execute_new_job(mock_job, mock_job_size, time)

        assert test_object.current_job_being_executed == mock_job
        assert test_object.time_current_execution_started == time
        assert test_object.current_job_size == mock_job_size