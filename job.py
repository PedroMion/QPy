from collections import defaultdict


class Job:
    def __init__(self, id, arrival_time, current_server):
        self.id = id
        self.arrival_time = arrival_time
        self.current_server = current_server
        self.arrival_time_at_current_server = arrival_time
        self.arrival_times_per_server = defaultdict(lambda: [])
        self.queue_times_per_server = defaultdict(lambda: 0)
        self.total_time_per_server = defaultdict(lambda: 0)
        self.total_visits_per_server = defaultdict(lambda: 0)

        self.arrival_times_per_server[current_server].append(arrival_time)
        self.total_visits_per_server[current_server] += 1

    def switch_servers_and_compute_state(self, time, server):
        self.current_server = server
        self.arrival_time_at_current_server = time
        self.arrival_times_per_server[server].append(time)
        self.total_visits_per_server[server] += 1

    def serve(self, service_started_time):
        self.queue_times_per_server[self.current_server] += service_started_time - self.arrival_time_at_current_server


    def reroute(self, completion_time, new_server = None):
        self.total_time_per_server[self.current_server] += completion_time - self.arrival_time_at_current_server

        if new_server:
            self.switch_servers_and_compute_state(completion_time, new_server)