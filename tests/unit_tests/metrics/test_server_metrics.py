import pytest


from qpy.job import Job
from qpy.metrics import ServerMetrics


TOTAL_SIMULATION_TIME = 200
SERVER_ID = 1
NUMBER_OF_PROCESSED_JOBS = 10
CURRENT_NUMBER_OF_JOBS = 1
WEIGHTED_SUM_NUMBER_OF_JOBS = 20
CURRENT_TIME = 50
TIME_PARAMETER = 60
CUMULATIVE_QUEUE_TIMES = 20
CUMULATIVE_TIME_IN_SERVER = 100
CUMULATIVE_SERVER_BUSY_TIME = 80
CUMULATIVE_VISITS_PER_JOB = 5
ZERO_VALUE = 0
NEGATIVE_VALUE = -1
JOB_ID = 1
JOB_ARRIVAL_TIME = 55
JOB_PRIORITY = 1
JOB_QUEUE_TIMES_PER_SERVER = {SERVER_ID: 5}
JOB_TOTAL_TIME_PER_SERVER = {SERVER_ID: 12}
JOB_TOTAL_VISITS_PER_SERVER = {SERVER_ID: 2}

@pytest.fixture
def server_metrics_empty_test_object():
    return ServerMetrics(SERVER_ID, TOTAL_SIMULATION_TIME)


@pytest.fixture
def server_metrics_test_object_with_informations():
    metrics = ServerMetrics(SERVER_ID, TOTAL_SIMULATION_TIME)

    metrics.total_number_of_processed_jobs_in_system = NUMBER_OF_PROCESSED_JOBS
    metrics.current_number_of_jobs = CURRENT_NUMBER_OF_JOBS
    metrics.weighted_sum_number_of_jobs = WEIGHTED_SUM_NUMBER_OF_JOBS
    metrics.current_time = CURRENT_TIME
    metrics.cumulative_queue_times = CUMULATIVE_QUEUE_TIMES
    metrics.cumulative_time_in_server = CUMULATIVE_TIME_IN_SERVER
    metrics.cumulative_server_busy_time = CUMULATIVE_SERVER_BUSY_TIME
    metrics.cumulative_visits_per_job = CUMULATIVE_VISITS_PER_JOB

    return metrics

@pytest.fixture
def job_mock_object():
    job = Job(JOB_ID, JOB_ARRIVAL_TIME, SERVER_ID, JOB_PRIORITY)

    job.queue_times_per_server = JOB_QUEUE_TIMES_PER_SERVER
    job.total_time_per_server = JOB_TOTAL_TIME_PER_SERVER
    job.total_visits_per_server = JOB_TOTAL_VISITS_PER_SERVER

    return job


"""
Particionamento do espaço de entrada para função compute_departure() da classe ServerMetrics:
    time: 0 | < 0 | > 0 | None
"""

"""time > 0 (Válido)"""
def test_compute_departure_when_time_is_valid_should_update_job_count(server_metrics_test_object_with_informations):
    expected_number_of_jobs = CURRENT_NUMBER_OF_JOBS - 1
    expected_weighted_sum_of_jobs = WEIGHTED_SUM_NUMBER_OF_JOBS + CURRENT_NUMBER_OF_JOBS * (TIME_PARAMETER - CURRENT_TIME)

    server_metrics_test_object_with_informations.compute_departure(time=TIME_PARAMETER)

    assert server_metrics_test_object_with_informations.current_number_of_jobs == expected_number_of_jobs
    assert server_metrics_test_object_with_informations.weighted_sum_number_of_jobs == expected_weighted_sum_of_jobs

"""time = 0 (Inválido)"""
def test_compute_departure_when_time_is_smaller_than_current_time_should_raise_exception(server_metrics_test_object_with_informations):
    with pytest.raises(ValueError):
        server_metrics_test_object_with_informations.compute_departure(time=ZERO_VALUE)

"""time < 0 (Inválido)"""
def test_compute_departure_when_time_is_negative_should_raise_exception(server_metrics_empty_test_object):
    with pytest.raises(ValueError):
        server_metrics_empty_test_object.compute_departure(time=NEGATIVE_VALUE)

"""time = None (Inválido)"""
def test_compute_departure_when_time_is_none_should_raise_exception(server_metrics_empty_test_object):
    with pytest.raises(TypeError):
        server_metrics_empty_test_object.compute_departure(time=None)


"""
Particionamento do espaço de entrada para função compute_environment_departure() da classe ServerMetrics:
    job: Válido | None
"""

"""job Válido (Válido)"""
def test_compute_environment_departure_when_job_is_valid_should_update_metrics(server_metrics_test_object_with_informations, job_mock_object):
    expected_number_of_processed_jobs_in_system = NUMBER_OF_PROCESSED_JOBS + 1
    expected_cumulative_queue_times = CUMULATIVE_QUEUE_TIMES + job_mock_object.queue_times_per_server[SERVER_ID]
    expected_cumulative_time_in_server = CUMULATIVE_TIME_IN_SERVER + job_mock_object.total_time_per_server[SERVER_ID]
    expected_cumulative_server_busy_time = CUMULATIVE_SERVER_BUSY_TIME + (job_mock_object.total_time_per_server[SERVER_ID] - job_mock_object.queue_times_per_server[SERVER_ID])
    expected_cumulative_visits_per_job = CUMULATIVE_VISITS_PER_JOB + job_mock_object.total_visits_per_server[SERVER_ID]

    server_metrics_test_object_with_informations.compute_environment_departure(job=job_mock_object)

    assert server_metrics_test_object_with_informations.total_number_of_processed_jobs_in_system == expected_number_of_processed_jobs_in_system
    assert server_metrics_test_object_with_informations.cumulative_queue_times == expected_cumulative_queue_times
    assert server_metrics_test_object_with_informations.cumulative_time_in_server == expected_cumulative_time_in_server
    assert server_metrics_test_object_with_informations.cumulative_server_busy_time == expected_cumulative_server_busy_time
    assert server_metrics_test_object_with_informations.cumulative_visits_per_job == expected_cumulative_visits_per_job

"""job = None (Inválido)"""
def test_compute_environment_departure_when_job_is_none_should_raise_exception(server_metrics_empty_test_object):
    with pytest.raises(TypeError):
        server_metrics_empty_test_object.compute_environment_departure(job=None)


"""
Particionamento do espaço de entrada para função get_number_of_processed_jobs() da classe ServerMetrics:
    cumulative_visits_per_job: 0 | > 0
"""

"""cumulative_visits_per_job = 0 (Válido)"""
def test_get_number_of_processed_jobs_when_visits_werent_made_should_return_zero(server_metrics_empty_test_object):
    assert server_metrics_empty_test_object.get_number_of_processed_jobs() == 0

"""cumulative_visits_per_job > 0 (Válido)"""
def test_get_number_of_processed_jobs_when_visits_were_made_should_return_count(server_metrics_test_object_with_informations):
    assert server_metrics_test_object_with_informations.get_number_of_processed_jobs() == CUMULATIVE_VISITS_PER_JOB


"""
Particionamento do espaço de entrada para função get_mean_time_in_server() da classe ServerMetrics:
    cumulative_visits_per_job: 0 | > 0
"""

"""cumulative_visits_per_job = 0 (Válido)"""
def test_get_mean_time_in_server_when_visits_werent_made_should_return_zero(server_metrics_empty_test_object):
    assert server_metrics_empty_test_object.get_mean_time_in_server() == 0

"""cumulative_visits_per_job > 0 (Válido)"""
def test_get_mean_time_in_server_when_visits_were_made_should_return_mean(server_metrics_test_object_with_informations):
    expected_mean = CUMULATIVE_TIME_IN_SERVER / CUMULATIVE_VISITS_PER_JOB

    assert server_metrics_test_object_with_informations.get_mean_time_in_server() == expected_mean


"""
Particionamento do espaço de entrada para função get_mean_visits_per_job() da classe ServerMetrics:
    total_number_of_processed_jobs_in_system: 0 | > 0
"""

"""total_number_of_processed_jobs_in_system = 0 (Válido)"""
def test_get_mean_visits_per_job_when_jobs_werent_processed_should_return_zero(server_metrics_empty_test_object):
    assert server_metrics_empty_test_object.get_mean_visits_per_job() == 0

"""total_number_of_processed_jobs_in_system > 0 (Válido)"""
def test_get_mean_visits_per_job_when_jobs_processed_should_return_mean(server_metrics_test_object_with_informations):
    expected_mean = CUMULATIVE_VISITS_PER_JOB / NUMBER_OF_PROCESSED_JOBS

    assert server_metrics_test_object_with_informations.get_mean_visits_per_job() == expected_mean


"""
Particionamento do espaço de entrada para função get_server_utilization() da classe ServerMetrics:
    total_simulation_time: 0 | > 0
"""

"""total_simulation_time = 0 (Válido)"""
def test_get_server_utilization_when_total_time_is_zero_should_return_zero():
    metrics = ServerMetrics(SERVER_ID, total_simulation_time=0)
    metrics.cumulative_server_busy_time = CUMULATIVE_SERVER_BUSY_TIME

    assert metrics.get_server_utilization() == 0

"""total_simulation_time > 0 (Válido)"""
def test_get_server_utilization_when_total_time_is_valid_should_return_utilization(server_metrics_test_object_with_informations):
    expected_utilization = CUMULATIVE_SERVER_BUSY_TIME / TOTAL_SIMULATION_TIME

    assert server_metrics_test_object_with_informations.get_server_utilization() == expected_utilization


"""
Particionamento do espaço de entrada para função get_throughput() da classe ServerMetrics:
    total_simulation_time: 0 | > 0
"""

"""total_simulation_time = 0 (Válido)"""
def test_get_throughput_when_total_time_is_zero_should_return_zero():
    metrics = ServerMetrics(SERVER_ID, total_simulation_time=0)
    metrics.cumulative_visits_per_job = CUMULATIVE_VISITS_PER_JOB

    assert metrics.get_throughput() == 0

"""total_simulation_time > 0 (Válido)"""
def test_get_throughput_when_total_time_is_valid_should_return_throughput(server_metrics_test_object_with_informations):
    expected_throughput = CUMULATIVE_VISITS_PER_JOB / TOTAL_SIMULATION_TIME

    assert server_metrics_test_object_with_informations.get_throughput() == expected_throughput


"""
Particionamento do espaço de entrada para função get_demand() da classe ServerMetrics:
    total_number_of_processed_jobs_in_system: 0 | > 0
"""

"""total_number_of_processed_jobs_in_system = 0 (Válido)"""
def test_get_demand_when_no_jobs_were_processed_should_return_zero(server_metrics_empty_test_object):
    assert server_metrics_empty_test_object.get_demand() == 0

"""total_number_of_processed_jobs_in_system > 0 (Válido)"""
def test_get_demand_when_jobs_were_processed_should_return_demand(server_metrics_test_object_with_informations):
    expected_demand = CUMULATIVE_TIME_IN_SERVER / NUMBER_OF_PROCESSED_JOBS

    assert server_metrics_test_object_with_informations.get_demand() == expected_demand