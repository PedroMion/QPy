from abc import ABC, abstractmethod
from server import Server
from utils import generate_exponential_arrivals


class INetwork(ABC):
    @abstractmethod
    def add_server(self, average_service_time, queue_discipline):
        return
    
    @abstractmethod
    def add_entry_point(self, server_id, average_arrival_time):
        return
    
    @abstractmethod
    def generate_jobs(self, time_limit): 
        return

    @abstractmethod
    def finish_job(self, event_queue):
        return


class OpenNetwork(INetwork):
    def __init__(self):
        self.servers = []
        self.arrivals = {}
    
    def add_server(self, average_service_time, queue_discipline):
        try:
            average_service_time = float(average_service_time)
        except ValueError:
            raise ValueError("Average service time must be double")
        
        if queue_discipline != 'SRT' and queue_discipline != 'FCFS':
            queue_discipline = 'FCFS'
        
        self.servers.append(Server(average_service_time, queue_discipline))
        server_id = len(self.servers) - 1
        
        self.arrivals[server_id] = 0

        return server_id
    
    def add_entry_point(self, server_id, average_arrival_time):
        if server_id >= 0 and server_id < len(self.servers):
            self.arrivals[server_id] += average_arrival_time

            return

        raise ValueError("The provided server id is not valid.")

    def generate_jobs(self, time_limit): 
        event_queue = []
        event_count = 0

        for server in self.arrivals.keys():
            if self.arrivals[server] > 0:
                generate_exponential_arrivals(event_queue, time_limit, server, self.arrivals[server], event_count)

                event_count = len(event_queue)
        return event_queue

    def finish_job(self, event_queue):
        return