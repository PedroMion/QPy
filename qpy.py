from execution import Execution
from network import ClosedNetwork, OpenNetwork
from utils import validate_distribution_input


class Environment:
    def __init__(self, number_of_terminals=None, average_think_time=None):
        self.network = None
        self.is_closed = False
        
        if number_of_terminals is None or average_think_time is None:
            self.network = OpenNetwork()
        else:
            self.network = ClosedNetwork(average_think_time, number_of_terminals)
            self.is_closed = True
    
    def add_server(self, average_service_time, service_distribution = 'exponential', queue_discipline = 'FCFS'):
        self.network.add_server(average_service_time, validate_distribution_input(service_distribution), queue_discipline)

    def add_entry_point(self, server_id, average_arrival_time, arrival_discipline='exponential'):
        if not self.is_closed:
            self.network.add_entry_point(server_id, average_arrival_time, validate_distribution_input(arrival_discipline))
        else:
            raise ValueError('Closed network does not allow entry points')
    
    def add_terminals_routing_probability(self, destiny_server_id, probability):
        if self.is_closed:
            self.network.add_terminals_routing_probability(destiny_server_id, probability)
        else:
            raise ValueError('Open network does not allow terminal routing')

    def simulate(self, time_in_seconds, warmup_time):
        queue = self.network.generate_jobs(time_in_seconds + warmup_time)

        new_execution = Execution(time_in_seconds, warmup_time, queue, self.network)

        return new_execution.execute()