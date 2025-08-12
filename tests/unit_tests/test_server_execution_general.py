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


"""
Não há particionamento do espaço de entrada para a função reset_configuration() da classe ServerExecution
"""
def test_reset_configuration_when_configuration_is_filled_should_clear_config():
    for test_object in get_all_test_objects():
        test_object.current_job_being_executed = MOCK_JOB
        test_object.current_job_size = JOB_SIZE
        test_object.time_current_execution_started = TIME

        test_object.reset_execution_configuration()

        assert test_object.current_job_being_executed == None
        assert test_object.time_current_execution_started == 0
        assert test_object.current_job_size == 0


"""
Particionamento do espaço de entrada para função execute_new_job() da classe ServerExecution utilizando Each Choice Coverage:
    job: None | Not None
    size: < 0 | >= 0
    time: < 0 | >= 0
"""

"""job Not None | size >= 0 | time >= 0 (Válido)"""
def test_execute_new_job_when_information_is_valid_should_update_variables():
    for test_object in get_all_test_objects():
        test_object.execute_new_job(MOCK_JOB, JOB_SIZE, TIME)

        assert test_object.current_job_being_executed == MOCK_JOB
        assert test_object.current_job_size == JOB_SIZE
        assert test_object.time_current_execution_started == TIME

"""job None | size >= 0 | time >= 0 (Inválido)"""
def test_execute_new_job_when_job_is_none_should_raise_exception():
    for test_object in get_all_test_objects():
        with pytest.raises(TypeError):
            test_object.execute_new_job(None, JOB_SIZE, TIME)

"""job Not None | size < 0 | time >= 0 (Inválido)"""
def test_execute_new_job_when_job_size_is_negative_should_raise_exception():
    for test_object in get_all_test_objects():
        with pytest.raises(ValueError):
            test_object.execute_new_job(MOCK_JOB, NEGATIVE_VALUE, TIME)

"""job Not None | size >= 0 | time < 0 (Inválido)"""
def test_execute_new_job_when_time_is_negative_should_raise_exception():
    for test_object in get_all_test_objects():
        with pytest.raises(ValueError):
            test_object.execute_new_job(MOCK_JOB, JOB_SIZE, NEGATIVE_VALUE)


"""
Particionamento do espaço de entrada para função remaining_time_for_current_job() da classe ServerExecution utilizando Each Choice Coverage:
    time: < 0 | >= 0
"""

"""time >= 0 (Válido)"""
def test_remaining_time_for_current_job_when_parameter_is_valid_should_return_remaining_time():
    for test_object in get_all_test_objects():
        test_object.current_job_being_executed = MOCK_JOB
        test_object.current_job_size = JOB_SIZE
        test_object.time_current_execution_started = ZERO

        response = test_object.remaining_time_for_current_job(TIME)

        assert response == test_object.current_job_size - TIME

"""time >= 0 (Inválido por regra de execução)"""
def test_remaining_time_for_current_job_when_time_is_invalid_should_raise_exception():
    for test_object in get_all_test_objects():
        test_object.current_job_being_executed = MOCK_JOB
        test_object.current_job_size = JOB_SIZE
        test_object.time_current_execution_started = TIME

        with pytest.raises(ValueError):
            test_object.remaining_time_for_current_job(ZERO)

"""time < 0 (Inválido)"""
def test_remaining_time_for_current_job_when_time_is_negative_should_raise_exception():
    for test_object in get_all_test_objects():
        test_object.current_job_being_executed = MOCK_JOB
        test_object.current_job_size = JOB_SIZE
        test_object.time_current_execution_started = TIME

        with pytest.raises(ValueError):
            test_object.remaining_time_for_current_job(NEGATIVE_VALUE)