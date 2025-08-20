import pytest


from qpy.metrics import GeneralMetrics


TOTAL_SIMULATION_TIME = 200
NUMBER_OF_PROCESSED_JOBS = 10
CURRENT_NUMBER_OF_JOBS = 1
WEIGHTED_SUM_NUMBER_OF_JOBS = 20
CURRENT_TIME = 50
TIME_PARAMETER = 60
CUMULATIVE_QUEUE_TIMES = 20
ZERO_VALUE = 0
NEGATIVE_VALUE = -1

@pytest.fixture
def general_metrics_empty_test_object():
    return GeneralMetrics(TOTAL_SIMULATION_TIME)

@pytest.fixture
def general_metrics_test_object_with_informations():
    metrics = GeneralMetrics(TOTAL_SIMULATION_TIME)

    metrics.total_number_of_processed_jobs_in_system = NUMBER_OF_PROCESSED_JOBS
    metrics.current_number_of_jobs = CURRENT_NUMBER_OF_JOBS
    metrics.weighted_sum_number_of_jobs = WEIGHTED_SUM_NUMBER_OF_JOBS
    metrics.current_time = CURRENT_TIME
    metrics.cumulative_queue_times = CUMULATIVE_QUEUE_TIMES

    return metrics


"""
Particionamento do espaço de entrada para função compute_arrival() da classe GeneralMetrics utilizando Each Choice Coverage:
    time: 0 | < 0 | > 0 | None
"""

"""time > 0 (Válido)"""
def test_compute_arrival_when_time_is_valid_should_update_job_count(general_metrics_test_object_with_informations):
    expected_number_of_jobs = CURRENT_NUMBER_OF_JOBS + 1
    expected_weighted_sum_number_of_jobs = WEIGHTED_SUM_NUMBER_OF_JOBS + CURRENT_NUMBER_OF_JOBS * (TIME_PARAMETER - CURRENT_TIME)
    
    general_metrics_test_object_with_informations.compute_arrival(time=TIME_PARAMETER)

    assert general_metrics_test_object_with_informations.current_number_of_jobs == expected_number_of_jobs
    assert general_metrics_test_object_with_informations.weighted_sum_number_of_jobs == expected_weighted_sum_number_of_jobs

"""time < 0 (Inválido)"""
def test_compute_arrival_when_time_is_invalid_should_raise_exception(general_metrics_test_object_with_informations):
    with pytest.raises(ValueError):
        general_metrics_test_object_with_informations.compute_arrival(time=NEGATIVE_VALUE)

"""time = None (Inválido)"""
def test_compute_arrival_when_time_is_none_should_raise_exception(general_metrics_test_object_with_informations):
    with pytest.raises(TypeError):
        general_metrics_test_object_with_informations.compute_arrival(time=None)

"""time = 0 (Inválido)"""
def test_compute_arrival_when_new_time_smaller_than_current_time_should_raise_exception(general_metrics_test_object_with_informations):
    with pytest.raises(ValueError):
        general_metrics_test_object_with_informations.compute_arrival(time=ZERO_VALUE)


"""
Particionamento do espaço de entrada para função get_number_of_processed_jobs() da classe GeneralMetrics:
    total_number_of_processed_jobs_in_system: 0 | > 0
"""

"""total_number_of_processed_jobs_in_system = 0 (Válido)"""
def test_get_number_of_processed_jobs_when_no_jobs_were_processed_should_return_zero(general_metrics_empty_test_object):
    assert general_metrics_empty_test_object.get_number_of_processed_jobs() == 0

"""total_number_of_processed_jobs_in_system > 0 (Válido)"""
def test_get_number_of_processed_jobs_when_jobs_were_processed_should_return_count(general_metrics_test_object_with_informations):
    assert general_metrics_test_object_with_informations.get_number_of_processed_jobs() == NUMBER_OF_PROCESSED_JOBS


"""
Particionamento do espaço de entrada para função get_mean_queue_time() da classe GeneralMetrics:
    total_number_of_processed_jobs_in_system: 0 | > 0
"""

"""total_number_of_processed_jobs_in_system = 0 (Válido)"""
def test_get_mean_queue_time_when_no_jobs_processed_should_return_zero(general_metrics_empty_test_object):
    assert general_metrics_empty_test_object.get_mean_queue_time() == 0

"""total_number_of_processed_jobs_in_system > 0 (Válido)"""
def test_get_mean_queue_time_when_jobs_processed_should_return_mean(general_metrics_test_object_with_informations):
    expected_mean = CUMULATIVE_QUEUE_TIMES / NUMBER_OF_PROCESSED_JOBS

    assert general_metrics_test_object_with_informations.get_mean_queue_time() == expected_mean


"""
Particionamento do espaço de entrada para função get_mean_number_of_jobs_in_system() da classe GeneralMetrics:
    total_simulation_time: 0 | > 0
"""

"""total_simulation_time = 0 (Válido)"""
def test_get_mean_number_of_jobs_in_system_when_total_time_is_zero_should_return_zero(general_metrics_empty_test_object):
    metrics = GeneralMetrics(total_simulation_time=ZERO_VALUE)
    metrics.weighted_sum_number_of_jobs = WEIGHTED_SUM_NUMBER_OF_JOBS

    assert metrics.get_mean_number_of_jobs_in_system() == 0

"""total_simulation_time > 0 (Válido)"""
def test_get_mean_number_of_jobs_in_system_when_total_time_is_valid_should_return_mean(general_metrics_test_object_with_informations):
    expected_mean = round(WEIGHTED_SUM_NUMBER_OF_JOBS / TOTAL_SIMULATION_TIME, 4)

    assert general_metrics_test_object_with_informations.get_mean_number_of_jobs_in_system() == expected_mean


"""
Particionamento do espaço de entrada para função get_throughput() da classe GeneralMetrics:
    total_simulation_time: 0 | > 0
"""

"""total_simulation_time = 0 (Válido)"""
def test_get_throughput_when_total_time_is_zero_should_return_zero(general_metrics_empty_test_object):
    metrics = GeneralMetrics(total_simulation_time=ZERO_VALUE)
    metrics.total_number_of_processed_jobs_in_system = NUMBER_OF_PROCESSED_JOBS

    assert metrics.get_throughput() == 0

"""total_simulation_time > 0 (Válido)"""
def test_get_throughput_when_total_time_is_valid_should_return_throughput(general_metrics_test_object_with_informations):
    expected_throughput = NUMBER_OF_PROCESSED_JOBS / TOTAL_SIMULATION_TIME

    assert general_metrics_test_object_with_informations.get_throughput() == expected_throughput
