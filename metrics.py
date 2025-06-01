from collections import defaultdict


class GeneralMetrics:
    def __init__(self, total_simulation_time):
        self.total_simultion_time = total_simulation_time
        self.total_number_of_processed_jobs_in_system = 0
        self.current_number_of_jobs = 0
        self.weighted_sum_number_of_jobs = 0
        self.current_time = 0
        self.cumulative_queue_times = 0
    
    def count_number_of_jobs(self, time, event):
        self.weighted_sum_number_of_jobs += round(self.current_number_of_jobs * (time - self.current_time), 4)
        self.current_time = round(time, 4)

        if event == 'arrival':
            self.current_number_of_jobs += 1
        else:
            self.current_number_of_jobs -= 1

    def compute_arrival(self, time):
        self.count_number_of_jobs(time, 'arrival')

    def get_number_of_processed_jobs(self):
        return self.total_number_of_processed_jobs_in_system
    
    def get_mean_queue_time(self):
        return self.cumulative_queue_times / self.total_number_of_processed_jobs_in_system

    def get_mean_number_of_jobs_in_system(self):
        return (round(self.weighted_sum_number_of_jobs / self.total_simultion_time, 4)) if self.total_simultion_time > 0 else 0

    def get_throughput(self):
        return self.total_number_of_processed_jobs_in_system / self.total_simultion_time if self.total_simultion_time > 0 else 0

class EnvironmentMetrics(GeneralMetrics):
    def __init__(self, total_simulation_time):
        super().__init__(total_simulation_time)
        self.cumulative_time_in_system = 0
    
    def compute_departure(self, job, time):
        self.count_number_of_jobs(time, 'departure')

        self.total_number_of_processed_jobs_in_system += 1
        self.cumulative_time_in_system += (time - job.arrival_time)
        self.cumulative_queue_times += sum(job.queue_times_per_server.values())

    def get_mean_time_in_system(self):
        return self.cumulative_time_in_system / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0

class ServerMetrics(GeneralMetrics):
    def __init__(self, server_id, total_simulation_time):
        super().__init__(total_simulation_time)
        self.server_id = server_id
        self.cumulative_time_in_server = 0
        self.cumulative_server_busy_time = 0
        self.cumulative_visits_per_job = 0
    
    def compute_departure(self, job, time):
        self.count_number_of_jobs(time, 'departure')

        self.total_number_of_processed_jobs_in_system += 1

        self.cumulative_queue_times += job.queue_times_per_server[self.server_id]
        self.cumulative_time_in_server += job.total_time_per_server[self.server_id]
        self.cumulative_server_busy_time += job.total_time_per_server[self.server_id] - job.queue_times_per_server[self.server_id]

        self.cumulative_visits_per_job += job.total_visits_per_server[self.server_id]
    
    def get_number_of_processed_jobs(self):
        return self.cumulative_visits_per_job

    def get_mean_time_in_server(self):
        return self.cumulative_time_in_server / self.cumulative_visits_per_job if self.cumulative_visits_per_job > 0 else 0

    def get_mean_visits_per_job(self):
        return self.cumulative_visits_per_job / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0

    def get_server_utilization(self):
        return self.cumulative_server_busy_time / self.total_simultion_time if self.total_simultion_time > 0 else 0

    def get_throughput(self):
        return self.cumulative_visits_per_job / self.total_simultion_time