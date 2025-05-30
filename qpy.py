import heapq


from network import OpenNetwork
from results import SimulationResults


class Environment:
    def __init__(self, num_of_terminals=None, average_think_time=None):
        self.network = None
        
        if num_of_terminals is None or average_think_time is None:
            self.network = OpenNetwork()
        else:
            raise NotImplemented()
    
    def add_server(self, average_service_time, queue_discipline = 'FCFS'):
        self.network.add_server(average_service_time, queue_discipline)

    def add_entry_point(self, server_id, average_arrival_time):
        self.network.add_entry_point(server_id, average_arrival_time)

    def simulate(self, time_in_seconds, warmup_time):
        queue = self.network.generate_jobs(time_in_seconds + warmup_time)

        new_execution = Execution(time_in_seconds, warmup_time, queue, self.network)

        return new_execution.execute()


class Execution:
    def __init__(self, time, warmup, queue, network_configuration):
        self.time = time
        self.warmup = warmup
        self.current_time = 0
        self.event_queue = queue
        self.event_count = len(queue)
        self.network_configuration = network_configuration
        self.results = SimulationResults(len(self.network_configuration.servers), time)
    
    def serve_new_job(self, server, job, current_time, service_time):
        heapq.heappush(self.event_queue, (current_time + service_time, self.event_count, 'departure', job, server))
        job.serve(current_time)
        self.event_count += 1

    def execute(self):
        while(len(self.event_queue) > 0 and self.current_time <= self.warmup + self.time):
            next_event = heapq.heappop(self.event_queue)
            self.current_time = next_event[0]
            job = next_event[3]
            server_id = next_event[4]
            server = self.network_configuration.servers[server_id]

            if next_event[2] == 'arrival':
                job.reroute(self.current_time)
                service_time = server.add_to_queue(job)

                if service_time:
                    self.serve_new_job(server_id, job, self.current_time, service_time)
                if self.current_time > self.warmup:
                    self.results.compute_arrival(self.current_time, server_id)
            else:
                #case where event is departure
                new_job_service_time = server.finish_current_job()

                if new_job_service_time:
                    self.serve_new_job(server_id, server.get_first_in_line(), self.current_time, new_job_service_time)
                
                route = server.route_job()

                if route != 'end':
                    job.reroute(self.current_time, route)
                    service_time = self.servers[route].add_to_queue(job)

                    if service_time:
                        self.serve_new_job(route, job, self.current_time, service_time)
                else:
                    job.reroute(self.current_time)
                    if job.arrival_time > self.warmup:
                        self.results.compute_departure(job, self.current_time)
        return self.results