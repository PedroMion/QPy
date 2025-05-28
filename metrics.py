from collections import defaultdict


class GeneralMetrics:
    def __init__(self):
        self.total_number_of_processed_jobs = 0
        self.current_number_of_jobs = 0
        self.weighted_sum_number_of_jobs = 0
        self.current_time = 0
        self.cumulative_queue_times = 0
        self.cumulative_time_in_system = 0
    
    def count_number_of_jobs(self, time, event):
        self.weighted_sum_number_of_jobs += round(self.current_number_of_jobs * (time - self.current_time), 4)
        self.current_time = round(time, 4)

        if event == 'arrival':
            self.current_number_of_jobs += 1
        else:
            self.current_number_of_jobs -= 1

    def compute_arrival(self, time):
        self.count_num_of_jobs(time, 'arrival')

    def compute_departure(self, job, time):
        self.count_num_of_jobs(time, 'departure')

        self.total_number_of_processed_jobs += 1
        self.cumulative_time_in_system += (time - job.arrival_time)
        self.cumulative_queue_times += job.time_in_queue

    def get_number_of_processed_jobs(self):
        return self.total_number_of_processed_jobs

    def get_mean_time_in_system(self):
        return self.cumulative_time_in_system / self.total_number_of_processed_jobs if self.total_number_of_processed_jobs > 0 else 0
    
    def get_mean_queue_time(self):
        return self.cumulative_queue_times / self.total_number_of_processed_jobs

    def get_mean_number_of_jobs_in_system(self):
        return (round(self.weighted_sum_number_of_jobs / self.current_time, 4)) if self.current_time > 0 else 0

class EnvironmentMetrics(GeneralMetrics):
    def __init__(self):
        super.__init__()

class ServerMetrics(GeneralMetrics):
    def __init__(self, server_id):
        super.__init__()
        self.server_id = server_id
        self.cumulative_server_busy_time = 0
        self.cumulative_visits_per_job = 0
    
    def compute_departure(self, job, time):
        super().compute_departure(job, time)

        self.cumulative_server_busy_time += job.time_in_system
        self.cumulative_visits_per_job += job.visits[self.server_id] - 1 # Super computes one visit / Verify later
    
    def get_mean_visits_per_job(self, total_jobs_processed_in_system):
        return self.cumulative_visits_per_job / total_jobs_processed_in_system if total_jobs_processed_in_system > 0 else 0

    def get_server_utilization(self):
        return self.cumulative_server_busy_time / self.current_time if self.current_time > 0 else 0
