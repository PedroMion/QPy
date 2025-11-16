from qpy.distribution import Distribution
from qpy.environment import Environment
from qpy.queue_discipline import QueueDiscipline
from utils import value_within_range


DELTA_JOBS_PERCENTAGE = 0.15 # 15% margin of error
TOTAL_SIMULATION_TIME = 20000
WARMUP_TIME = 10000

MU = 1
LAMBDA = 0.5

def _create_environment_with_servers(num_of_servers: int) -> Environment:
    env = Environment()

    for _ in range(num_of_servers):
        env.add_server(service_distribution=Distribution.exponential(1/MU), queue_discipline=QueueDiscipline.fcfs())

    env.add_entry_point(0, Distribution.exponential(1/LAMBDA))

    return env

def test_open_network_MM1_exponential_FCFS():
    env = _create_environment_with_servers(num_of_servers=1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * LAMBDA
    expected_time_in_system = (1/(MU - LAMBDA)) # Formula for M/M/1
    expected_time_in_queue = expected_time_in_system - (1/MU) # Total time minus expected service time

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_time_in_system, ans.environment_metrics.get_mean_time_in_system(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_time_in_queue, ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)

def test_open_network_MM2_all_jobs_go_through_both_servers_exponential_FCFS():
    env = _create_environment_with_servers(num_of_servers=2)
    env.add_servers_connection(0, 1, 1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * LAMBDA
    expected_time_in_system = (1/(MU - LAMBDA)) * 2 # Two M/M/1's connected
    expected_time_in_queue = expected_time_in_system - ((1/MU) * 2) # Two service times

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs, ans.server_metrics[0].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs, ans.server_metrics[1].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_time_in_system, ans.environment_metrics.get_mean_time_in_system(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_time_in_queue, ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)

def test_open_network_MM3_all_jobs_go_through_server_0_and_half_chance_to_both_servers_exponential():
    env = _create_environment_with_servers(num_of_servers=3)
    env.add_servers_connection(0, 1, 0.5)
    env.add_servers_connection(0, 2, 0.5)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME * 10, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = (TOTAL_SIMULATION_TIME * 10) * LAMBDA
    expected_number_of_jobs_each_server = expected_number_of_jobs / 2 # 50% routing
    expected_time_in_system = (1/(MU - LAMBDA)) + (1/(MU - (LAMBDA/2))) # Normal M/M/1 connected to other M/M/1 with half the jobs, given the division
    expected_time_in_queue = expected_time_in_system - ((1/MU) * 2) # Both service times

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs_each_server, ans.server_metrics[1].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_number_of_jobs_each_server, ans.server_metrics[2].get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_time_in_system, ans.environment_metrics.get_mean_time_in_system(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_time_in_queue, ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)