import heapq


from .job import Job
from .network import INetwork
from .results import SimulationResults


class Execution:
    def __init__(self, time: float, warmup: float, queue: list, network_configuration: INetwork, time_unit: str):
        self.time = time
        self.warmup = warmup
        self.current_time = 0
        self.event_queue = queue
        self.event_count = len(queue)
        self.network_configuration = network_configuration
        self.results = SimulationResults(len(self.network_configuration.servers), time, time_unit)
    
    def add_next_departure_event(self, server: int, job: Job, current_time: float, service_time: float, event: str):
        heapq.heappush(self.event_queue, (current_time + service_time, self.event_count, event, job, server))
        self.event_count += 1
        
        if event == 'departure':
            job.serve(current_time)

    def execute(self) -> SimulationResults:
        while(len(self.event_queue) > 0 and self.current_time <= self.warmup + self.time):
            next_event = heapq.heappop(self.event_queue)
            self.current_time = next_event[0]
            job = next_event[3]
            server_id = next_event[4]
            server = self.network_configuration.servers[server_id]

            if next_event[2] == 'arrival':
                job.reroute(self.current_time)
                service_time = server.job_arrival(job, self.current_time)

                if service_time:
                    self.add_next_departure_event(server_id, job, self.current_time, service_time, event='departure' if server.is_next_event_departure() else 'preemption')
                if self.current_time > self.warmup:
                    self.results.compute_arrival(self.current_time, server_id)
            
            else:
                # Case where event is departure or preemption
                new_job_being_executed = server.finish_execution(self.current_time, is_preemption = next_event[2] == 'preemption')

                if new_job_being_executed:
                    new_job_service_time = new_job_being_executed[0]
                    new_job = new_job_being_executed[1]

                    self.add_next_departure_event(server_id, new_job, self.current_time, new_job_service_time, event='departure' if server.is_next_event_departure() else 'preemption')
                
                route = server.route_job()

                if route != 'end':
                    job.reroute(self.current_time, route)
                    destination_server = self.network_configuration.servers[route]
                    
                    if job.arrival_time > self.warmup:
                        self.results.reroute(self.current_time, server_id, route)

                    service_time = destination_server.job_arrival(job, self.current_time)

                    if service_time:
                        self.add_next_departure_event(route, job, self.current_time, service_time, event='departure' if destination_server.is_next_event_departure() else 'preemption')
                else:
                    job.reroute(self.current_time)
                    if job.arrival_time > self.warmup:
                        self.results.reroute(self.current_time, server_id, destination_server=None)
                        self.results.compute_departure(job, self.current_time)
                    self.network_configuration.finish_job(self.event_queue, self.current_time)

        return self.results