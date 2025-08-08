from qpy.environment import Environment
from qpy.distribution import Distribution
from qpy.queue_discipline import QueueDiscipline


DELTA = 0.05

def test_open_network_MM1_constant_FCFS():
    env = Environment()
    env.add_server(service_distribution=Distribution.constant(1), queue_discipline=QueueDiscipline.fcfs())
    env.add_entry_point(0, Distribution.constant(2))

    ans = env.simulate(time_in_seconds=1000, warmup_time=2000)

    assert ans.environment_metrics.get_number_of_processed_jobs() == 499 # One job each 2 seconds starting in second 2
