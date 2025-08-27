from collections import defaultdict
from .metrics import EnvironmentMetrics, PriorityMetrics, ServerMetrics
from .validation_utils import validate_number_params_not_negative_and_not_none, validate_object_params_not_none


class EnvironmentResults:
    def __init__(self, number_of_processed_jobs: int, mean_time_in_system: float, mean_queue_time: float, mean_number_of_jobs_in_system: float, throughput: float, max_demand: float):
        self.number_of_processed_jobs = number_of_processed_jobs
        self.mean_time_in_system = mean_time_in_system
        self.mean_queue_time = mean_queue_time
        self.mean_number_of_jobs_in_system = mean_number_of_jobs_in_system
        self.throughput = throughput
        self.max_demand = max_demand


class ServerResults:
    def __init__(self, number_of_processed_jobs: int, mean_time_in_server: float, mean_queue_time: float, mean_number_of_jobs_in_server: int, mean_visits_per_job: float, server_utilization: float, throughput: float, demand: float):
        self.number_of_processed_jobs = number_of_processed_jobs
        self.mean_time_in_server = mean_time_in_server
        self.mean_queue_time = mean_queue_time
        self.mean_number_of_jobs_in_server = mean_number_of_jobs_in_server
        self.mean_visits_per_job = mean_visits_per_job
        self.server_utilization = server_utilization
        self.throughput = throughput
        self.demand = demand


class PriorityResults:
    def __init__(self, number_of_processed_jobs: int, mean_time_in_system: float, mean_queue_time: float):
        self.number_of_processed_jobs = number_of_processed_jobs
        self.mean_time_in_system = mean_time_in_system
        self.mean_queue_time = mean_queue_time


class SimulationResults:
    def __init__(self, number_of_servers, total_simulation_time, time_unit):
        self.environment_metrics = EnvironmentMetrics(total_simulation_time)
        self.server_metrics = [ServerMetrics(i, total_simulation_time) for i in range(number_of_servers)]
        self.priority_metrics = defaultdict(lambda: PriorityMetrics(total_simulation_time))
        self.jobs = defaultdict(lambda: None)
        self.time_unit = time_unit
    
    def _add_job_to_result(self, job):
        self.jobs[job.id] = job
    
    def _compute_servers_departure(self, job, time):
        for server_id in range(len(self.server_metrics)):
            self.server_metrics[server_id].compute_environment_departure(job)

    def compute_arrival(self, current_time, server_id):
        validate_number_params_not_negative_and_not_none(function_name='compute_arrival', current_time=current_time, server_id=server_id)

        self.environment_metrics.compute_arrival(current_time)
        self.server_metrics[server_id].compute_arrival(current_time)

    def reroute(self, current_time, origin_server, destination_server):
        validate_number_params_not_negative_and_not_none(function_name='reroute', current_time=current_time, origin_server=origin_server)

        self.server_metrics[origin_server].compute_departure(current_time)

        if destination_server:
            self.server_metrics[destination_server].compute_arrival(current_time)

    def compute_departure(self, job, current_time):
        validate_number_params_not_negative_and_not_none(function_name='compute_departure', current_time=current_time)
        validate_object_params_not_none(function_name='compute_departure', job=job)

        self._add_job_to_result(job)
        self.environment_metrics.compute_departure(job, current_time)
        self.priority_metrics[job.priority].compute_departure(job, current_time)
        
        self._compute_servers_departure(job, current_time)
    
    def show_simulation_metrics(self):
        print('\n====================  Environment Metrics ====================\n')
        print(f'Total number of processed jobs: {self.environment_metrics.get_number_of_processed_jobs()}')
        print(f'E[T]: {self.environment_metrics.get_mean_time_in_system()} {self.time_unit} per job')
        print(f'E[Tq]: {self.environment_metrics.get_mean_queue_time()} {self.time_unit} per job')
        print(f'E[N]: {self.environment_metrics.get_mean_number_of_jobs_in_system()} jobs')
        print(f'X: {self.environment_metrics.get_throughput()} jobs per {self.time_unit}')
        print(f'Dmax: {max(s.get_demand() for s in self.server_metrics)} {self.time_unit} per job')

        for server in self.server_metrics:
            print(f'\n==================== Server {server.server_id+1} Metrics ====================\n')
            print(f'Total number of processed jobs: {server.get_number_of_processed_jobs()}')
            print(f'E[T]: {server.get_mean_time_in_server()} {self.time_unit} per job')
            print(f'E[Tq]: {server.get_mean_queue_time()} {self.time_unit} per job')
            print(f'E[N]: {server.get_mean_number_of_jobs_in_system()} jobs')
            print(f'E[V]: {server.get_mean_visits_per_job()} visits per job')
            print(f'Utilization: {server.get_server_utilization() * 100}%')
            print(f'X: {server.get_throughput()} jobs per {self.time_unit}')
            print(f'D: {server.get_demand()} {self.time_unit} per job')
        
        if len(self.priority_metrics.keys()) > 1:
            for key, value in sorted(self.priority_metrics.items()):
                print(f'\n==================== Priority {key} Metrics ====================\n')
                print(f'Total number of processed jobs: {value.get_number_of_processed_jobs()}')
                print(f'E[T]: {value.get_mean_time_in_system()} {self.time_unit} per job')
                print(f'E[Tq]: {value.get_mean_queue_time()} {self.time_unit} per job')