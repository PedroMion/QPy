from collections import defaultdict
from metrics import EnvironmentMetrics, ServerMetrics


class SimulationResults:
    def __init__(self, number_of_servers, total_simulation_time, time_unit):
        self.environment_metrics = EnvironmentMetrics(total_simulation_time)
        self.server_metrics = [ServerMetrics(i, total_simulation_time) for i in range(number_of_servers)]
        self.jobs = defaultdict(lambda: None)
        self.time_unit = time_unit
    
    def add_job_to_result(self, job):
        self.jobs[job.id] = job
    
    def compute_arrival(self, current_time, server_id):
        self.environment_metrics.compute_arrival(current_time)
        self.server_metrics[server_id].compute_arrival(current_time)

    def compute_servers_departure(self, job, time):
        for server_id in job.total_time_per_server.keys():
            self.server_metrics[server_id].compute_departure(job, time)

    def compute_departure(self, job, current_time):
        self.add_job_to_result(job)
        self.environment_metrics.compute_departure(job, current_time)
        
        self.compute_servers_departure(job, current_time)
    
    def show_simulation_metrics(self):
        print('\n====================  Environment Metrics ====================\n')
        print(f'Total number of processed jobs: {self.environment_metrics.get_number_of_processed_jobs()}')
        print(f'E[T]: {self.environment_metrics.get_mean_time_in_system()} {self.time_unit} per job')
        print(f'E[Tq]: {self.environment_metrics.get_mean_queue_time()} {self.time_unit} per job')
        print(f'E[N]: {self.environment_metrics.get_mean_number_of_jobs_in_system()} jobs')
        print(f'X: {self.environment_metrics.get_throughput()} jobs per {self.time_unit}')

        for server in self.server_metrics:
            print(f'\n==================== Server {server.server_id+1} Metrics ====================\n')
            print(f'Total number of processed jobs: {server.get_number_of_processed_jobs()}')
            print(f'E[T]: {server.get_mean_time_in_server()} {self.time_unit} per job')
            print(f'E[Tq]: {server.get_mean_queue_time()} {self.time_unit} per job')
            print(f'E[N]: {server.get_mean_number_of_jobs_in_system()} jobs')
            print(f'E[V]: {server.get_mean_visits_per_job()} visits per job')
            print(f'Utilization: {server.get_server_utilization() * 100}%')
            print(f'X: {server.get_throughput()} jobs per {self.time_unit}')