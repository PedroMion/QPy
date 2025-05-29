from collections import defaultdict
from metrics import EnvironmentMetrics, ServerMetrics


class SimulationResults:
    def __init__(self, number_of_servers):
        self.environment_metrics = EnvironmentMetrics()
        self.server_metrics = [ServerMetrics(i) for i in range(number_of_servers)]
        self.jobs = defaultdict(lambda: None)
    
    def add_job_to_result(self, job):
        self.jobs[job.id] = job
    
    def compute_arrival(self, current_time, server_id):
        self.environment_metrics.compute_arrival(current_time)
        self.server_metrics[server_id].compute_arrival(current_time)
    
    def compute_server_departure(self, job, current_time, server_id):
        self.server_metrics[server_id].compute_departure(job, current_time)

    def compute_departure(self, job, current_time, server_id):
        self.add_job_to_result(job)
        self.environment_metrics.compute_departure(job, current_time)
        self.compute_server_departure(self, job, current_time, server_id)
    
    def show_simulation_metrics(self):
        raise NotImplementedError()