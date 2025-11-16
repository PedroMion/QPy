from qpy.environment import Environment
from qpy.distribution import Distribution
from qpy.queue_discipline import QueueDiscipline
from utils import value_within_range


DELTA_JOBS_PERCENTAGE = 0.05 # 5% margin of error

TOTAL_SIMULATION_TIME = 1000
WARMUP_TIME = 2000

MU = 1
LAMBDA = 0.5

def _create_environment_with_servers(num_of_servers: int) -> Environment:
    env = Environment()

    for _ in range(num_of_servers):
        env.add_server(service_distribution=Distribution.constant(1/MU), queue_discipline=QueueDiscipline.fcfs())

    env.add_entry_point(0, Distribution.constant(1/LAMBDA))

    return env

def test_open_network_MM1_constant_FCFS():
    env = _create_environment_with_servers(num_of_servers=1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    assert ans.environment_metrics.get_number_of_processed_jobs() == TOTAL_SIMULATION_TIME * LAMBDA - 1 # One job each 2 seconds starting on second 2

def test_open_network_MM2_all_jobs_go_through_both_servers_constant_FCFS():
    env = _create_environment_with_servers(num_of_servers=2)
    env.add_servers_connection(0, 1, 1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    assert ans.environment_metrics.get_number_of_processed_jobs() == TOTAL_SIMULATION_TIME * LAMBDA - 1 # One job each 2 seconds starting on second 2

    assert ans.server_metrics[0].get_number_of_processed_jobs() == TOTAL_SIMULATION_TIME * LAMBDA - 1 # All jobs go through server 0

    assert ans.server_metrics[1].get_number_of_processed_jobs() == TOTAL_SIMULATION_TIME * LAMBDA - 1 # All jobs go through server 1

def test_open_network_MM3_all_jobs_go_through_server_0_and_half_chance_to_both_servers_constant():
    env = _create_environment_with_servers(num_of_servers=3)
    env.add_servers_connection(0, 1, 0.5)
    env.add_servers_connection(0, 2, 0.5)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME * 50, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * 50 * LAMBDA - 1 # One job each 2 seconds starting on second 2

    assert ans.environment_metrics.get_number_of_processed_jobs() == expected_number_of_jobs
    assert ans.server_metrics[0].get_number_of_processed_jobs() == expected_number_of_jobs # All jobs go through server 0

    assert value_within_range(expected=expected_number_of_jobs // 2, actual=ans.server_metrics[1].get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE) # 50% of jobs go through server 1
    assert value_within_range(expected=expected_number_of_jobs // 2, actual=ans.server_metrics[2].get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE) # 50% of jobs go through server 2