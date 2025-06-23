from .distribution import IDistribution, Distribution
from .server import Server
from .queue_discipline import IQueue, QueueDiscipline
from .utils import generate_arrivals, generate_new_job_closed_network, validade_priority_input
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional


class INetwork(ABC):
    @abstractmethod
    def add_server(self, service_distribution: IDistribution, queue_discipline: IQueue) -> int:
        return
    
    @abstractmethod
    def generate_jobs(self, time_limit: float) -> list: 
        return

    @abstractmethod
    def finish_job(self, event_queue: list, time: float):
        return


class OpenNetwork(INetwork):
    def __init__(self):
        self.servers = []
        self.arrivals = defaultdict(lambda: [])
        self.priorities = defaultdict(lambda: None)
    
    def add_server(self, service_distribution: IDistribution, queue_discipline: IQueue) -> int:        
        if not queue_discipline:
            queue_discipline = QueueDiscipline.FCFS()
        
        self.servers.append(Server(service_distribution, queue_discipline))
        server_id = len(self.servers) - 1

        return server_id
    
    def add_entry_point(self, server_id: int, arrival_distribution: IDistribution, priority_distribution: Optional[dict] = None):
        if server_id >= 0 and server_id < len(self.servers):
            self.arrivals[server_id].append(arrival_distribution)

            if priority_distribution:
                self.priorities[server_id] = priority_distribution

            return

        raise ValueError("The provided server id is not valid.")

    def generate_jobs(self, time_limit: float) -> list: 
        event_queue = []
        event_count = 0

        for server in self.arrivals.keys():
            for distribution in self.arrivals[server]:
                generate_arrivals(event_queue, event_count, time_limit, server, distribution, self.priorities[server])

                event_count = len(event_queue)
        return event_queue

    def finish_job(self, event_queue: Optional[list] = None, time: Optional[float] = None):
        return
    


class ClosedNetwork(INetwork):
    def __init__(self, think_time_distribution: IDistribution, number_of_terminals: int):
        self.servers = []
        self.priorities = {}
        self.entry_point_routing = defaultdict(lambda: 0)
        self.think_time_distribution = think_time_distribution
        self.number_of_terminals = number_of_terminals
        self.job_count = 0

        self.entry_point_routing['end'] = 1
    
    def add_server(self, service_distribution: IDistribution, queue_discipline: str) -> int:        
        if queue_discipline != 'SRT' and queue_discipline != 'FCFS':
            queue_discipline = 'FCFS'
        
        self.servers.append(Server(service_distribution, queue_discipline))
        server_id = len(self.servers) - 1

        return server_id

    def add_priorities(self, priorities: dict):
        if validade_priority_input(priorities):
            self.priorities = priorities

    def add_terminals_routing_probability(self, destination_server_id: int, probability: float):
        end_probability = self.entry_point_routing["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        if destination_server_id >= 0 and destination_server_id < len(self.servers):
            self.entry_point_routing["end"] -= probability
            self.entry_point_routing[destination_server_id] += probability

            return

        raise ValueError("A server with the provided id was not found")
    
    def generate_jobs(self, time_limit: Optional[float] = None) -> list: 
        event_queue = []

        for i in range(self.number_of_terminals):
            generate_new_job_closed_network(event_queue, i, 0, self.think_time_distribution, self.entry_point_routing, self.priorities)
        
        self.job_count = self.number_of_terminals

        return event_queue

    def finish_job(self, event_queue: list, time: float):
        generate_new_job_closed_network(event_queue, self.job_count, time, self.average_think_time, self.entry_point_routing, self.priorities)