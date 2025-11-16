from qpy.distribution import Distribution
from qpy.environment import Environment
from qpy.queue_discipline import QueueDiscipline
from utils import value_within_range


DELTA_JOBS_PERCENTAGE = 0.10 # 10% margin of error
TOTAL_SIMULATION_TIME = 20000
WARMUP_TIME = 10000

LOWER_BOUND_SERVER = 0.0001
UPPER_BOUND_SERVER = 2.0001
LOWER_BOUND_ARRIVAL = 0.5
UPPER_BOUND_ARRIVAL = 2.5

LAMBDA = 1/((LOWER_BOUND_ARRIVAL + UPPER_BOUND_ARRIVAL) / 2)
MU = 1/((LOWER_BOUND_SERVER + UPPER_BOUND_SERVER) / 2)

EXPECTED_UTILIZATION = LAMBDA / MU
EXPECTED_SERVICE_TIME = 1 / MU

def _create_environment_with_servers(num_of_servers: int) -> Environment:
    env = Environment()

    for _ in range(num_of_servers):
        env.add_server(service_distribution=Distribution.uniform(LOWER_BOUND_SERVER, UPPER_BOUND_SERVER), queue_discipline=QueueDiscipline.fcfs())

    env.add_entry_point(0, Distribution.uniform(LOWER_BOUND_ARRIVAL, UPPER_BOUND_ARRIVAL))

    return env

def test_open_network_MM1_uniform_FCFS():
    env = _create_environment_with_servers(num_of_servers=1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * LAMBDA

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_UTILIZATION, ans.server_metrics[0].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_SERVICE_TIME, ans.environment_metrics.get_mean_time_in_system() - ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)

def test_open_network_MM2_all_jobs_go_through_both_servers_uniform_FCFS():
    env = _create_environment_with_servers(num_of_servers=2)
    env.add_servers_connection(0, 1, 1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * LAMBDA

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs, ans.server_metrics[0].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs, ans.server_metrics[1].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_UTILIZATION, ans.server_metrics[0].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_UTILIZATION, ans.server_metrics[1].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_SERVICE_TIME * 2, ans.environment_metrics.get_mean_time_in_system() - ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE) # Times two for two servers

def test_open_network_MM3_all_jobs_go_through_server_0_and_half_chance_to_both_servers_uniform():
    env = _create_environment_with_servers(num_of_servers=3)
    env.add_servers_connection(0, 1, 0.5)
    env.add_servers_connection(0, 2, 0.5)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME * 10, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * 10 * LAMBDA
    expected_number_of_jobs_each_server = expected_number_of_jobs / 2

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs_each_server, ans.server_metrics[1].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs_each_server, ans.server_metrics[2].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_UTILIZATION, ans.server_metrics[0].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(EXPECTED_UTILIZATION / 2, ans.server_metrics[1].get_server_utilization(), DELTA_JOBS_PERCENTAGE) # Half because jobs split
    assert value_within_range(EXPECTED_UTILIZATION / 2, ans.server_metrics[2].get_server_utilization(), DELTA_JOBS_PERCENTAGE) # Half because jobs split
    assert value_within_range(EXPECTED_SERVICE_TIME * 2, ans.environment_metrics.get_mean_time_in_system() - ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)