from execution import Execution
from network import ClosedNetwork, OpenNetwork
from utils import validate_distribution_input, validade_priority_input


class Environment:
    def __init__(self, number_of_terminals=None, average_think_time=None, time_unit='seconds'):
        self.network = None
        self.is_closed = False
        self.time_unit = time_unit
        
        if number_of_terminals is None or average_think_time is None:
            self.network = OpenNetwork()
        else:
            self.network = ClosedNetwork(average_think_time, number_of_terminals)
            self.is_closed = True
    
    def add_server(self, average_service_time, service_distribution = 'exponential', queue_discipline = 'FCFS'):
        self.network.add_server(average_service_time, validate_distribution_input(service_distribution), queue_discipline)

    def add_entry_point(self, server_id, average_arrival_time, arrival_discipline='exponential', priority_distribution=None):
        if not self.is_closed:
            self.network.add_entry_point(server_id, average_arrival_time, validate_distribution_input(arrival_discipline), validade_priority_input(priority_distribution))
        else:
            raise ValueError('Closed network does not allow entry points')
    
    def add_priority_closed_network(self, priorities):
        if self.is_closed:
            self.network.add_priorities(priorities)

    def add_terminals_routing_probability(self, destination_server_id, probability):
        if self.is_closed:
            self.network.add_terminals_routing_probability(destination_server_id, probability)
        else:
            raise ValueError('Open network does not allow terminal routing')

    def simulate(self, time_in_seconds, warmup_time):
        queue = self.network.generate_jobs(time_in_seconds + warmup_time)

        new_execution = Execution(time_in_seconds, warmup_time, queue, self.network, self.time_unit)

        return new_execution.execute()