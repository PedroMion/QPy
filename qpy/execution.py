import heapq


from .event import Event
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
        self.next_departure_event_by_server = [None] * len(self.network_configuration.servers)

    def _add_next_departure_event(self, server: int, job: Job, current_time: float, service_time: float, event_type: str):            
        if event_type == 'preemption':
            service_time = self.network_configuration.servers[server].get_preemption_time()
            
        new_event_object = Event(current_time + service_time, self.event_count, event_type, job, server)
        
        heapq.heappush(self.event_queue, (current_time + service_time, self.event_count, new_event_object))
        self.next_departure_event_by_server[server] = new_event_object

        self.event_count += 1

        job.serve(current_time)

    def _route_job_after_event(self, event: Event):
        route = event.server.route_job()

        if route != 'end':
            event.job.reroute(self.current_time, route)
            destination_server = self.network_configuration.servers[route]

            if event.job.arrival_time > self.warmup:
                self.results.reroute(self.current_time, event.server_id, route)
                self.results.compute_arrival(self.current_time, route)

            new_event = Event(self.current_time, self.event_count, 'arrival', event.job, route)
            self.event_count += 1

            service_time = destination_server.job_arrival(new_event)

            if service_time:
                self._add_next_departure_event(route, new_event.job, self.current_time, service_time, event_type='departure' if destination_server.is_next_event_departure() else 'preemption')
        else:
            event.job.reroute(self.current_time)
            if event.job.arrival_time > self.warmup:
                self.results.reroute(self.current_time, event.server_id, destination_server=None)
                self.results.compute_departure(event.job, self.current_time)
            self.network_configuration.finish_job(self.event_queue, self.current_time)

    def _case_event_is_arrival(self, event: Event):
        event.job.reroute(self.current_time)
        service_time = event.server.job_arrival(event)

        if service_time:
            if self.next_departure_event_by_server[event.server_id]:
                self.next_departure_event_by_server[event.server_id].canceled = True

            self._add_next_departure_event(event.server_id, event.job, self.current_time, service_time, event_type='departure' if event.server.is_next_event_departure() else 'preemption')
        if event.job.arrival_time > self.warmup:
            self.results.compute_arrival(self.current_time, event.server_id)

    def _case_event_is_departure_or_preemption(self, event: Event):
        new_job_being_executed = event.server.finish_execution(self.current_time, is_preemption=(event.type == 'preemption'))
        self.next_departure_event_by_server[event.server_id] = None

        if new_job_being_executed:
            new_job_service_time = new_job_being_executed[0]
            new_job = new_job_being_executed[1]

            self._add_next_departure_event(event.server_id, new_job, self.current_time, new_job_service_time, event_type='departure' if event.server.is_next_event_departure() else 'preemption')

        self._route_job_after_event(event)

    def execute(self) -> SimulationResults:
        end_time = self.warmup + self.time

        while len(self.event_queue) > 0:
            top_time = self.event_queue[0][0]
            if top_time > end_time:
                break

            next_event = heapq.heappop(self.event_queue)[2]

            if next_event.canceled:
                continue

            next_event.server = self.network_configuration.servers[next_event.server_id]

            self.current_time = round(next_event.current_time, 4)

            if next_event.type == 'arrival':
                self._case_event_is_arrival(next_event)
            else:
                self._case_event_is_departure_or_preemption(next_event)

        return self.results