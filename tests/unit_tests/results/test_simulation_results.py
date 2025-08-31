import pytest


from qpy.job import Job
from qpy.results import SimulationResults


NUMBER_OF_SERVERS = 3
SIMULATION_TIME = 100
CURRENT_TIME = 70
TIME_UNIT = 'seconds'
NEGATIVE_VALUE = -1
JOB_ID = 1
JOB_ARRIVAL_TIME = 55
JOB_CURRENT_SERVER = 1
JOB_PRIORITY = 1


@pytest.fixture
def simulation_results_empty_object():
    return SimulationResults(NUMBER_OF_SERVERS, SIMULATION_TIME, TIME_UNIT)

@pytest.fixture
def job_mock_object():
    job = Job(JOB_ID, JOB_ARRIVAL_TIME, JOB_CURRENT_SERVER, JOB_PRIORITY)

    job.queue_times_per_server[JOB_CURRENT_SERVER] = 2

    return job


"""
Particionamento do espaço de entrada para função compute_departure() da classe SimulationResults utilizando Each Choice Coverage:
    job: Válido | None
    current_time: < 0 | >= 0
"""

"""job Válido | current_time >= 0 (Válido)"""
def test_compute_departure_when_both_inputs_are_valid_should_update_results(simulation_results_empty_object, job_mock_object):
    simulation_results_empty_object.compute_departure(job=job_mock_object, current_time=CURRENT_TIME)

    assert simulation_results_empty_object.jobs[JOB_ID] != None

"""job Inválido | current_time >= 0 (Inválido)"""
def test_compute_departure_when_job_is_invalid_should_raise_exception(simulation_results_empty_object):
    with pytest.raises(TypeError):
        simulation_results_empty_object.compute_departure(job=None, current_time=CURRENT_TIME)

"""job Válido | current_time < 0 (Inválido)"""
def test_compute_departure_when_time_is_negative_should_raise_exception(simulation_results_empty_object, job_mock_object):
    with pytest.raises(ValueError):
        simulation_results_empty_object.compute_departure(job=job_mock_object, current_time=NEGATIVE_VALUE)