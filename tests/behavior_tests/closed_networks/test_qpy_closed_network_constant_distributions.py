from qpy.environment import Environment
from qpy.distribution import Distribution
from qpy.queue_discipline import QueueDiscipline
from utils import value_within_range


DELTA_JOBS_PERCENTAGE = 0.05 # 5% margin of error

THINK_TIME = 2
TERMINALS = 4

TOTAL_SIMULATION_TIME = 1000
WARMUP_TIME = 2000

MU = 1

def _create_environment_with_servers(num_of_servers: int) -> Environment:
    env = Environment(number_of_terminals=TERMINALS, think_time_distribution=Distribution.constant(THINK_TIME))

    for _ in range(num_of_servers):
        env.add_server(service_distribution=Distribution.constant(1/MU), queue_discipline=QueueDiscipline.fcfs())

    env.add_terminals_routing_probability(destination_server_id=0, probability=1)

    return env

def test_closed_network_MM1_constant_FCFS():
    env = _create_environment_with_servers(num_of_servers=1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_utilization = 1
    expected_queue_time = max(((TERMINALS - (THINK_TIME * MU) - 1) * (1/MU)), 0) # After the system stabilizes, queue time can be predicted
    expected_time_in_system = expected_queue_time + 1/MU

    assert value_within_range(expected=TOTAL_SIMULATION_TIME * MU, actual=ans.environment_metrics.get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE) # Should be 100% utilization
    assert value_within_range(expected=expected_utilization, actual=ans.server_metrics[0].get_server_utilization(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected= expected_queue_time, actual=ans.environment_metrics.get_mean_queue_time(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_time_in_system * MU, actual=ans.environment_metrics.get_mean_time_in_system(), delta=DELTA_JOBS_PERCENTAGE)

def test_closed_network_MM2_all_jobs_go_through_both_servers_constant_FCFS():
    env = _create_environment_with_servers(num_of_servers=2)
    env.add_servers_connection(0, 1, 1)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME, warmup_time=WARMUP_TIME)

    expected_utilization = 1
    expected_queue_time = max(((TERMINALS - (THINK_TIME * MU) - 2) * (1/MU)), 0) # Second server takes away one job from count
    expected_time_in_system = expected_queue_time + 2 * 1/MU # Two servers

    assert value_within_range(expected=TOTAL_SIMULATION_TIME * MU, actual=ans.environment_metrics.get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE) # System througput is the same
    assert value_within_range(expected=TOTAL_SIMULATION_TIME * MU, actual=ans.server_metrics[0].get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=TOTAL_SIMULATION_TIME * MU, actual=ans.server_metrics[1].get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_utilization, actual=ans.server_metrics[0].get_server_utilization(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_utilization, actual=ans.server_metrics[1].get_server_utilization(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected= expected_queue_time, actual=ans.environment_metrics.get_mean_queue_time(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_time_in_system * MU, actual=ans.environment_metrics.get_mean_time_in_system(), delta=DELTA_JOBS_PERCENTAGE)

def test_closed_network_MM3_all_jobs_go_through_server_0_and_half_chance_to_both_servers_constant():
    env = _create_environment_with_servers(num_of_servers=3)
    env.add_servers_connection(0, 1, 0.5)
    env.add_servers_connection(0, 2, 0.5)

    ans = env.simulate(time_in_seconds=TOTAL_SIMULATION_TIME * 10, warmup_time=WARMUP_TIME)

    expected_number_of_jobs = TOTAL_SIMULATION_TIME * MU * 10
    expected_utilization = 1
    expected_queue_time = max(((TERMINALS - (THINK_TIME * MU) - 2) * (1/MU)), 0) # Second server takes away one job from count
    expected_time_in_system = expected_queue_time + 2 * 1/MU # Two servers

    assert value_within_range(expected=expected_number_of_jobs, actual=ans.environment_metrics.get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE) # System througput is the same
    assert value_within_range(expected=expected_number_of_jobs / 2, actual=ans.server_metrics[1].get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_number_of_jobs / 2, actual=ans.server_metrics[2].get_number_of_processed_jobs(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_utilization, actual=ans.server_metrics[0].get_server_utilization(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_utilization / 2, actual=ans.server_metrics[1].get_server_utilization(), delta=DELTA_JOBS_PERCENTAGE) # Half the work for servers 2 and 3
    assert value_within_range(expected=expected_utilization / 2, actual=ans.server_metrics[1].get_server_utilization(), delta=DELTA_JOBS_PERCENTAGE) # Half the work for servers 2 and 3
    assert value_within_range(expected= expected_queue_time, actual=ans.environment_metrics.get_mean_queue_time(), delta=DELTA_JOBS_PERCENTAGE)
    assert value_within_range(expected=expected_time_in_system * MU, actual=ans.environment_metrics.get_mean_time_in_system(), delta=DELTA_JOBS_PERCENTAGE)