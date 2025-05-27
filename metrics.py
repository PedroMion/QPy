from collections import defaultdict


class SimulationMetrics:
    def __init__(self):
        self.server_metrics = []
        self.total_jobs = 0
        self.num_of_jobs_in_system = 0
        self.current_time = 0
        self.weighted_sum_num_jobs = 0
        self.arrival_times = []
        self.queue_times = []
        self.time_in_system = []
    
    def count_num_of_jobs(self, time, event):
        self.weighted_sum_num_jobs += round(self.num_of_jobs_in_system * (time - self.current_time), 4)
        self.current_time = round(time, 4)

        if event == 'arrival':
            self.num_of_jobs_in_system += 1
        else:
            self.num_of_jobs_in_system -= 1

    def compute_arrival(self, time):
        self.count_num_of_jobs(time, 'arrival')

    def compute_departure(self, job, time):
        self.count_num_of_jobs(time, 'departure')

        self.total_jobs += 1
        self.arrival_times.append(job.arrival_time)
        self.queue_times.append(job.time_in_queue)
        self.time_in_system.append(time - job.arrival_time)
    
    def collect_server_metrics(self, servers):
        for server in servers:
            self.server_metrics.append(server.metrics)

    def num_processed_jobs(self):
        return self.total_jobs

    def mean_time_in_system(self):
        return (sum(self.time_in_system) / self.total_jobs) if self.total_jobs > 0 else 0
    
    def mean_queue_time(self):
        return sum(self.queue_times) / self.total_jobs

    def mean_num_jobs_in_system(self):
        return (round(self.weighted_sum_num_jobs / self.current_time, 4)) if self.current_time > 0 else 0
        
class ServerMetrics:
    def __init__(self):
        self.non_idle_time = 0
        self.time_in_queue = defaultdict(lambda: 0)
        self.total_time_in_server_by_job = defaultdict(lambda: 0)
        self.visits_per_job = defaultdict(lambda: 0)
