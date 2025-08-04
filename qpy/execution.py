import heapq


from .event import Event
from .job import Job
from .network import INetwork
from .results import SimulationResults
from .server import Server


class Execution:
    def __init__(self, time: float, warmup: float, queue: list, network_configuration: INetwork, time_unit: str):
        self.time = time
        self.warmup = warmup
        self.current_time = 0
        self.event_queue = queue
        self.event_count = len(queue)
        self.network_configuration = network_configuration
        self.next_departure_by_server = [0] * len(network_configuration.servers)
        self.results = SimulationResults(len(self.network_configuration.servers), time, time_unit)
    
    def add_next_departure_event(self, server: int, job: Job, current_time: float, service_time: float, event: str):
        new_event_object = Event(current_time + service_time, self.event_queue, event, job, server)

        heapq.heappush(self.event_queue, (current_time + service_time, self.event_count, new_event_object))
        self.next_departure_by_server[server] = new_event_object

        self.event_count += 1
        
        if event == 'departure':
            job.serve(current_time)

    def route_job_after_event(self, event: Event, server: Server):
        route = server.route_job()

        if route != 'end':
            event.job.reroute(self.current_time, route)
            destination_server = self.network_configuration.servers[route]
            
            if event.job.arrival_time > self.warmup:
                self.results.reroute(self.current_time, event.server_id, route)

            service_time = destination_server.job_arrival(event.job, self.current_time)

            if service_time:
                self.add_next_departure_event(route, event.job, self.current_time, service_time, event='departure' if destination_server.is_next_event_departure() else 'preemption')
        else:
            event.job.reroute(self.current_time)
            if event.job.arrival_time > self.warmup:
                self.results.reroute(self.current_time, event.server_id, destination_server=None)
                self.results.compute_departure(event.job, self.current_time)
            self.network_configuration.finish_job(self.event_queue, self.current_time)

    def case_event_is_arrival(self, event: Event, server: Server):
        event.job.reroute(self.current_time)
        service_time = server.job_arrival(event.job, self.current_time)

        if service_time:
            self.add_next_departure_event(event.server_id, event.job, self.current_time, service_time, event='departure' if server.is_next_event_departure() else 'preemption')
        if self.current_time > self.warmup:
            self.results.compute_arrival(self.current_time, event.server_id)

    def case_event_is_departure_or_preemption(self, event: Event, server: Server):
        new_job_being_executed = server.finish_execution(self.current_time, is_preemption = event.type == 'preemption')

        if new_job_being_executed:
            new_job_service_time = new_job_being_executed[0]
            new_job = new_job_being_executed[1]

            self.add_next_departure_event(event.server_id, new_job, self.current_time, new_job_service_time, event='departure' if server.is_next_event_departure() else 'preemption')
        
        self.route_job_after_event(event, server)

    def execute(self) -> SimulationResults:
        while(len(self.event_queue) > 0 and self.current_time <= self.warmup + self.time):
            next_event = heapq.heappop(self.event_queue)[2]

            if not next_event:
                continue

            server = self.network_configuration.servers[next_event.server_id]
            
            self.current_time = next_event.current_time

            if next_event.type == 'arrival':
                self.case_event_is_arrival(next_event, server)
            
            else:
                self.case_event_is_departure_or_preemption(next_event, server)

        return self.results