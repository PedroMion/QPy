from abc import ABC, abstractmethod
from collections import defaultdict
from server import Server
from utils import generate_arrivals, generate_new_job_closed_network, validade_priority_input


class INetwork(ABC):
    @abstractmethod
    def add_server(self, average_service_time, queue_discipline):
        return
    
    @abstractmethod
    def generate_jobs(self, time_limit): 
        return

    @abstractmethod
    def finish_job(self, event_queue, time):
        return


class OpenNetwork(INetwork):
    def __init__(self):
        self.servers = []
        self.arrivals = defaultdict(lambda: defaultdict(lambda: 0))
        self.priorities = defaultdict(lambda: None)
    
    def add_server(self, average_service_time, service_distribution, queue_discipline):
        try:
            average_service_time = float(average_service_time)
        except ValueError:
            raise ValueError("Average service time must be double")
        
        if queue_discipline != 'SRT' and queue_discipline != 'FCFS':
            queue_discipline = 'FCFS'
        
        self.servers.append(Server(average_service_time, service_distribution, queue_discipline))
        server_id = len(self.servers) - 1

        return server_id
    
    def add_entry_point(self, server_id, average_arrival_time, arrival_distribution='exponential', priority_distribution=None):
        if server_id >= 0 and server_id < len(self.servers):
            self.arrivals[server_id][arrival_distribution] += average_arrival_time

            if priority_distribution:
                self.priorities[server_id] = priority_distribution

            return

        raise ValueError("The provided server id is not valid.")

    def generate_jobs(self, time_limit): 
        event_queue = []
        event_count = 0

        for server in self.arrivals.keys():
            for distribution in self.arrivals[server].keys():
                if self.arrivals[server][distribution] > 0:
                    generate_arrivals(event_queue, time_limit, server, self.arrivals[server][distribution], distribution, self.priorities[server], event_count)

                    event_count = len(event_queue)
        return event_queue

    def finish_job(self, event_queue, time):
        return
    


class ClosedNetwork(INetwork):
    def __init__(self, average_think_time, number_of_terminals):
        self.servers = []
        self.priorities = {}
        self.entry_point_routing = defaultdict(lambda: 0)
        self.average_think_time = average_think_time
        self.number_of_terminals = number_of_terminals
        self.job_count = 0

        self.entry_point_routing['end'] = 1
    
    def add_server(self, average_service_time, service_distribution, queue_discipline):
        try:
            average_service_time = float(average_service_time)
        except ValueError:
            raise ValueError("Average service time must be double")
        
        if queue_discipline != 'SRT' and queue_discipline != 'FCFS':
            queue_discipline = 'FCFS'
        
        if service_distribution != 'constant':
            service_distribution = 'exponential'
        
        self.servers.append(Server(average_service_time, service_distribution, queue_discipline))
        server_id = len(self.servers) - 1

        return server_id

    def add_priorities(self, priorities):
        if validade_priority_input(priorities):
            self.priorities = priorities

    def add_terminals_routing_probability(self, destination_server_id, probability):
        end_probability = self.entry_point_routing["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        if destination_server_id >= 0 and destination_server_id < len(self.servers):
            self.entry_point_routing["end"] -= probability
            self.entry_point_routing[destination_server_id] += probability

            return

        raise ValueError("A server with the provided id was not found")
    
    def generate_jobs(self, time_limit): 
        event_queue = []

        for i in range(self.number_of_terminals):
            generate_new_job_closed_network(event_queue, i, 0, self.average_think_time, self.entry_point_routing, self.priorities)
        
        self.job_count = self.number_of_terminals

        return event_queue

    def finish_job(self, event_queue, time):
        generate_new_job_closed_network(event_queue, self.job_count, time, self.average_think_time, self.entry_point_routing, self.priorities)