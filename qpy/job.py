from .validation_utils import validate_number_params_not_negative_and_not_none, validate_number_params_not_negative
from collections import defaultdict


class Job:
    def __init__(self, id: int, arrival_time: float, current_server: int, priority: int):
        self.id = id
        self.arrival_time = arrival_time
        self.current_server = current_server
        self.priority = priority
        self.arrival_time_at_current_server = arrival_time
        self.arrival_times_per_server = defaultdict(lambda: [])
        self.queue_times_per_server = defaultdict(lambda: 0)
        self.total_time_per_server = defaultdict(lambda: 0)
        self.total_visits_per_server = defaultdict(lambda: 0)

        self.arrival_times_per_server[current_server].append(arrival_time)
        self.total_visits_per_server[current_server] += 1

    def _switch_servers_and_compute_state(self, time: float, server: int):
        validate_number_params_not_negative_and_not_none(function_name='switch_servers_and_compute_state', time=time, server=server)

        self.current_server = server
        self.arrival_time_at_current_server = time
        self.arrival_times_per_server[server].append(time)
        self.total_visits_per_server[server] += 1

    def serve(self, service_started_time: float):
        if service_started_time < self.arrival_time_at_current_server:
            raise ValueError(f'Job can\'t be executed before arrival.\nService started: {service_started_time} | Arrival time: {self.arrival_time_at_current_server}')
        
        self.queue_times_per_server[self.current_server] += service_started_time - self.arrival_time_at_current_server


    def reroute(self, completion_time: float, new_server: int = None):
        validate_number_params_not_negative_and_not_none(function_name='reroute', completion_time=completion_time)
        validate_number_params_not_negative(function_name='reroute', new_server=new_server)

        
        self.total_time_per_server[self.current_server] += completion_time - self.arrival_time_at_current_server

        if new_server:
            self._switch_servers_and_compute_state(completion_time, new_server)