import pytest


from qpy.job import Job
from qpy.metrics import EnvironmentMetrics


TOTAL_SIMULATION_TIME = 200
NUMBER_OF_PROCESSED_JOBS = 10
CURRENT_NUMBER_OF_JOBS = 1
WEIGHTED_SUM_NUMBER_OF_JOBS = 20
CURRENT_TIME = 50
TIME_PARAMETER = 60
CUMULATIVE_QUEUE_TIMES = 20
CUMULATIVE_TIME_IN_SYSTEM = 100
ZERO_VALUE = 0
NEGATIVE_VALUE = -1
JOB_ID = 1
JOB_ARRIVAL_TIME = 55
JOB_CURRENT_SERVER = 1
JOB_PRIORITY = 1

@pytest.fixture
def environment_metrics_empty_test_object():
    return EnvironmentMetrics(TOTAL_SIMULATION_TIME)


@pytest.fixture
def environment_metrics_test_object_with_informations():
    metrics = EnvironmentMetrics(TOTAL_SIMULATION_TIME)

    metrics.total_number_of_processed_jobs_in_system = NUMBER_OF_PROCESSED_JOBS
    metrics.current_number_of_jobs = CURRENT_NUMBER_OF_JOBS
    metrics.weighted_sum_number_of_jobs = WEIGHTED_SUM_NUMBER_OF_JOBS
    metrics.current_time = CURRENT_TIME
    metrics.cumulative_queue_times = CUMULATIVE_QUEUE_TIMES
    metrics.cumulative_time_in_system = CUMULATIVE_TIME_IN_SYSTEM

    return metrics

@pytest.fixture
def job_mock_object():
    job = Job(JOB_ID, JOB_ARRIVAL_TIME, JOB_CURRENT_SERVER, JOB_PRIORITY)

    job.queue_times_per_server[JOB_CURRENT_SERVER] = 2

    return job


"""
Particionamento do espaço de entrada para função compute_departure() da classe EnvironmentMetrics utilizando Each Choice Coverage:
    time: 0 | < 0 | > 0 | None
    job: Válido | None
"""

"""time > 0 | job Válido (Válido)"""
def test_compute_departure_when_time_and_job_are_valid_should_update_metrics(environment_metrics_test_object_with_informations, job_mock_object):
    expected_number_of_processed_jobs = NUMBER_OF_PROCESSED_JOBS + 1
    expected_cumulative_time_in_system = CUMULATIVE_TIME_IN_SYSTEM + (TIME_PARAMETER - job_mock_object.arrival_time)
    expected_cumulative_queue_times = CUMULATIVE_QUEUE_TIMES + sum(job_mock_object.queue_times_per_server.values())
    expected_current_number_of_jobs = CURRENT_NUMBER_OF_JOBS - 1

    environment_metrics_test_object_with_informations.compute_departure(job_mock_object, time=TIME_PARAMETER)

    assert environment_metrics_test_object_with_informations.total_number_of_processed_jobs_in_system == expected_number_of_processed_jobs
    assert environment_metrics_test_object_with_informations.cumulative_time_in_system == expected_cumulative_time_in_system
    assert environment_metrics_test_object_with_informations.cumulative_queue_times == expected_cumulative_queue_times
    assert environment_metrics_test_object_with_informations.current_number_of_jobs == expected_current_number_of_jobs

"""time = 0 | job Válido (Inválido)"""
def test_compute_departure_when_time_is_smaller_than_current_time_should_raise_exception(environment_metrics_test_object_with_informations, job_mock_object):
    with pytest.raises(ValueError):
        environment_metrics_test_object_with_informations.compute_departure(job_mock_object, time=ZERO_VALUE)

"""time = None | job Válido (Inválido)"""
def test_compute_departure_when_time_is_none_should_raise_exception(environment_metrics_empty_test_object, job_mock_object):
    with pytest.raises(TypeError):
        environment_metrics_empty_test_object.compute_departure(job_mock_object, time=None)

"""time < 0 | job Válido (Inválido)"""
def test_compute_departure_when_time_is_negative_should_raise_exception(environment_metrics_empty_test_object, job_mock_object):
    with pytest.raises(ValueError):
        environment_metrics_empty_test_object.compute_departure(job_mock_object, time=NEGATIVE_VALUE)

"""time > 0 | job Inválido (Inválido)"""
def test_compute_departure_when_job_is_none_should_raise_exception(environment_metrics_empty_test_object):
    with pytest.raises(TypeError):
        environment_metrics_empty_test_object.compute_departure(job=None, time=TIME_PARAMETER)


"""
Particionamento do espaço de entrada para função get_mean_time_in_system() da classe EnvironmentMetrics:
    total_number_of_processed_jobs_in_system: 0 | > 0
"""

"""total_number_of_processed_jobs_in_system = 0 (Válido)"""
def test_get_mean_time_in_system_when_no_jobs_processed_should_return_zero(environment_metrics_empty_test_object):
    assert environment_metrics_empty_test_object.get_mean_time_in_system() == 0

"""total_number_of_processed_jobs_in_system > 0 (Válido)"""
def test_get_mean_time_in_system_when_jobs_processed_should_return_mean(environment_metrics_test_object_with_informations):
    expected_mean = CUMULATIVE_TIME_IN_SYSTEM / NUMBER_OF_PROCESSED_JOBS
    
    assert environment_metrics_test_object_with_informations.get_mean_time_in_system() == expected_mean
