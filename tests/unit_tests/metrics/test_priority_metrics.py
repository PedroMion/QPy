import pytest


from qpy.job import Job
from qpy.metrics import PriorityMetrics


TIME_PARAMETER = 60
TOTAL_SIMULATION_TIME = 200
NUMBER_OF_PROCESSED_JOBS = 10
CUMULATIVE_QUEUE_TIMES = 20
CUMULATIVE_TIME_IN_SYSTEM = 100
ZERO_VALUE = 0
NEGATIVE_VALUE = -1
JOB_ID = 1
JOB_ARRIVAL_TIME = 40
SERVER_ID = 1
JOB_PRIORITY = 1
JOB_QUEUE_TIMES_PER_SERVER = {SERVER_ID: 5}

@pytest.fixture
def priority_metrics_empty_test_object():
    return PriorityMetrics(TOTAL_SIMULATION_TIME)

@pytest.fixture
def priority_metrics_test_object_with_informations():
    metrics = PriorityMetrics(TOTAL_SIMULATION_TIME)

    metrics.total_number_of_processed_jobs_in_system = NUMBER_OF_PROCESSED_JOBS
    metrics.cumulative_queue_times = CUMULATIVE_QUEUE_TIMES
    metrics.cumulative_time_in_system = CUMULATIVE_TIME_IN_SYSTEM

    return metrics

@pytest.fixture
def job_mock_object():
    job = Job(JOB_ID, JOB_ARRIVAL_TIME, SERVER_ID, JOB_PRIORITY)
    job.queue_times_per_server = JOB_QUEUE_TIMES_PER_SERVER
    return job


"""
Particionamento do espaço de entrada para função compute_departure() da classe PriorityMetrics:
    job: Válido | None
    time: 0 | < 0 | > 0 | None
"""

"""time > 0 | job Válido (Válido)"""
def test_compute_departure_when_time_and_job_are_valid_should_update_metrics(priority_metrics_test_object_with_informations, job_mock_object):
    expected_number_of_processed_jobs = NUMBER_OF_PROCESSED_JOBS + 1
    expected_cumulative_time_in_system = CUMULATIVE_TIME_IN_SYSTEM + (TIME_PARAMETER - JOB_ARRIVAL_TIME)
    expected_cumulative_queue_times = CUMULATIVE_QUEUE_TIMES + JOB_QUEUE_TIMES_PER_SERVER[SERVER_ID]

    priority_metrics_test_object_with_informations.compute_departure(job=job_mock_object, time=TIME_PARAMETER)

    assert priority_metrics_test_object_with_informations.total_number_of_processed_jobs_in_system == expected_number_of_processed_jobs
    assert priority_metrics_test_object_with_informations.cumulative_time_in_system == expected_cumulative_time_in_system
    assert priority_metrics_test_object_with_informations.cumulative_queue_times == expected_cumulative_queue_times


"""time > 0 | job = None (Inválido)"""
def test_compute_departure_when_job_is_invalid_should_raise_exception(priority_metrics_empty_test_object):
    with pytest.raises(TypeError):
        priority_metrics_empty_test_object.compute_departure(job=None, time=TIME_PARAMETER)


"""time = 0 | job Válido (Inválido)"""
def test_compute_departure_when_time_is_smaller_than_arrival_time_should_raise_exception(priority_metrics_test_object_with_informations, job_mock_object):
    with pytest.raises(ValueError):
        priority_metrics_test_object_with_informations.compute_departure(job=job_mock_object, time=ZERO_VALUE)


"""time < 0 | job Válido (Inválido)"""
def test_compute_departure_when_time_is_negative_should_raise_exception(priority_metrics_empty_test_object, job_mock_object):
    with pytest.raises(ValueError):
        priority_metrics_empty_test_object.compute_departure(job=job_mock_object, time=NEGATIVE_VALUE)


"""time = None | job Válido (Inválido)"""
def test_compute_departure_when_time_is_none_should_raise_exception(priority_metrics_empty_test_object, job_mock_object):
    with pytest.raises(TypeError):
        priority_metrics_empty_test_object.compute_departure(job=job_mock_object, time=None)


"""
Particionamento do espaço de entrada para função get_mean_time_in_system() da classe PriorityMetrics:
    total_number_of_processed_jobs_in_system: 0 | > 0
"""

"""total_number_of_processed_jobs_in_system = 0 (Válido)"""
def test_get_mean_time_in_system_when_no_jobs_were_processed_should_return_zero(priority_metrics_empty_test_object):
    assert priority_metrics_empty_test_object.get_mean_time_in_system() == 0


"""total_number_of_processed_jobs_in_system > 0 (Válido)"""
def test_get_mean_time_in_system_when_jobs_were_processed_should_return_mean(priority_metrics_test_object_with_informations):
    expected_mean = CUMULATIVE_TIME_IN_SYSTEM / NUMBER_OF_PROCESSED_JOBS

    assert priority_metrics_test_object_with_informations.get_mean_time_in_system() == expected_mean
