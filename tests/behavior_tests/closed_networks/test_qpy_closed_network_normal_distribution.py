from qpy.distribution import Distribution
from qpy.environment import Environment
from qpy.queue_discipline import QueueDiscipline
from utils import value_within_range


DELTA_JOBS_PERCENTAGE = 0.15 # 15% margin of error
TOTAL_SIMULATION_TIME = 20000
WARMUP_TIME = 10000

THINK_TIME = 2
TERMINALS = 4

MU_SERVER = 4
SIGMA_SERVER = 2
MU_TERMINALS = 8
SIGMA_TERMINALS = 2

def _create_environment_with_servers(num_of_servers: int) -> Environment:
    env = Environment(number_of_terminals=TERMINALS, think_time_distribution=Distribution.normal(mu=MU_TERMINALS, sigma=SIGMA_TERMINALS))

    for _ in range(num_of_servers):
        env.add_server(service_distribution=Distribution.normal(mu=MU_SERVER, sigma=SIGMA_SERVER), queue_discipline=QueueDiscipline.fcfs())

    env.add_terminals_routing_probability(destination_server_id=0, probability=1)

    return env

def test_closed_network_MM1_normal_FCFS():
    env = _create_environment_with_servers(num_of_servers=1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * 1/MU_SERVER
    expected_utilization = 1

    assert value_within_range(expected_number_of_jobs, ans.environment_metrics.get_number_of_processed_jobs(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_utilization, ans.server_metrics[0].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(MU_SERVER, ans.environment_metrics.get_mean_time_in_system() - ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)

def test_closed_network_MM2_all_jobs_go_through_both_servers_normal_FCFS():
    env = _create_environment_with_servers(num_of_servers=2)
    env.add_servers_connection(0, 1, 1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_utilization = 0.8

    assert value_within_range(expected_utilization, ans.server_metrics[0].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_utilization, ans.server_metrics[1].get_server_utilization(), DELTA_JOBS_PERCENTAGE)

def test_closed_network_MM3_all_jobs_go_through_server_0_and_half_chance_to_both_servers_normal():
    env = _create_environment_with_servers(num_of_servers=3)
    env.add_servers_connection(0, 1, 0.5)
    env.add_servers_connection(0, 2, 0.5)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME * 10, warmup_time=WARMUP_TIME)

    expected_utilization = 0.8 # Lower because of other server

    assert value_within_range(expected_utilization, ans.server_metrics[0].get_server_utilization(), DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected_utilization / 2, ans.server_metrics[1].get_server_utilization(), DELTA_JOBS_PERCENTAGE) # Half because jobs split
    assert value_within_range(expected_utilization / 2, ans.server_metrics[2].get_server_utilization(), DELTA_JOBS_PERCENTAGE) # Half because jobs split
    assert value_within_range(MU_SERVER * 2, ans.environment_metrics.get_mean_time_in_system() - ans.environment_metrics.get_mean_queue_time(), DELTA_JOBS_PERCENTAGE)