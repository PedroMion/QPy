from metrics import EnvironmentMetrics
from server import Server
from utils import generate_exponential_arrivals


class Environment:
    def __init__(self, num_of_terminals=None, average_think_time=None):
        self.servers = []
        self.job_arrival_times = []
        self.metrics = EnvironmentMetrics()
        
        if num_of_terminals is None or average_think_time is None:
            self.closed = False
        else:
            self.closed = True
            self.num_of_terminals = num_of_terminals
            self.average_think_time = average_think_time
    
    def addServer(self, average_service_time, queue_discipline = 'FCFS'):
        try:
            average_service_time = float(average_service_time)
        except ValueError:
            raise ValueError("Average service time must be double")
        
        if queue_discipline != 'SRT' and queue_discipline != 'FCFS':
            queue_discipline = 'FCFS'
        
        self.servers.append(Server(average_service_time, queue_discipline))

        return len(self.servers) - 1

    def addEntryPoint(self, server_id, average_arrival_time):
        if server_id >= 0 and server_id < len(self.servers):
            self.servers[server_id].add_arrival(average_arrival_time)
            return
        raise ValueError("The provided server id is not valid.")

    #def simulate(time_in_seconds):

