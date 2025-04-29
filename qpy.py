import heapq


from metrics import EnvironmentMetrics
from server import Server
from utils import generate_exponential_arrivals


class Environment:
    def __init__(self, num_of_terminals=None, average_think_time=None):
        self.servers = []
        self.arrivals = {}
        
        if num_of_terminals is None or average_think_time is None:
            self.closed = False
        else:
            self.closed = True
            self.num_of_terminals = num_of_terminals
            self.average_think_time = average_think_time
    
    def add_server(self, average_service_time, queue_discipline = 'FCFS'):
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

    def simulate(self, time_in_seconds, warmup_time):
        queue = self.generate_jobs(time_in_seconds + warmup_time)

        new_execution = Execution(time_in_seconds, warmup_time, queue, self.servers)

        return new_execution.execute()


class Execution:
    def __init__(self, time, warmup, queue, servers):
        self.time = time
        self.warmup = warmup
        self.event_queue = queue
        self.event_count = len(queue)
        self.servers = servers
        self.metrics = EnvironmentMetrics()
    
    def serve_new_job(self, server, job, current_time, service_time):
        heapq.heappush(self.event_queue, (current_time + service_time, self.event_count, 'departure', job, server))
        job.serve(current_time)
        self.event_count += 1

    def execute(self):
        while(len(self.event_queue) > 0):
            next_event = heapq.heappop(self.event_queue)
            current_time = next_event[0]
            job = next_event[3]
            server_id = next_event[4]

            if next_event[2] == 'arrival':
                job.reroute(current_time)
                service_time = self.servers[server_id].add_to_queue(job)

                if service_time:
                    self.serve_new_job(server_id, job, current_time, service_time)
            else:
                #case where event is departure
                server = self.servers[server_id]
                new_job_service_time = server.finish_current_job()

                if new_job_service_time:
                    self.serve_new_job(server_id, job, current_time, new_job_service_time)
                
                route = server.route_job()

                if route != 'end':
                    job.reroute(current_time)
                    service_time = self.servers[server_id].add_to_queue(job)

                    if service_time:
                        self.serve_new_job(server_id, job, current_time, service_time)
                else:
                    if current_time > self.warmup:
                        self.metrics.compute_job(job, current_time)
        return self.metrics