from metrics import EnvironmentMetrics


class Server:
    def __init__(self, average_service_time, queue_discipline):
        self.average_service_time = average_service_time
        self.queue_discipline = queue_discipline
        self.destinies = {"end": 1.0}
        self.arrivals = []
    
    def add_arrival(self, average_arrival_time):
        self.arrivals.append(average_arrival_time)
    
    def add_destiny(self, destiny_server, probability):
        end_probability = self.destinies["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinies["end"] -= probability
        self.destinies[destiny_server] = probability

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
