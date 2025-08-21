from collections import defaultdict

from qpy.job import Job
from qpy.validation_utils import validate_number_params_not_negative_and_not_none, validate_object_params_not_none


class GeneralMetrics:
    def __init__(self, total_simulation_time: float):
        self.total_simulation_time = total_simulation_time
        self.total_number_of_processed_jobs_in_system = 0
        self.current_number_of_jobs = 0
        self.weighted_sum_number_of_jobs = 0
        self.current_time = 0
        self.cumulative_queue_times = 0
    
    def _count_number_of_jobs(self, time: float, event: str):
        self.weighted_sum_number_of_jobs += round(self.current_number_of_jobs * (time - self.current_time), 4)
        self.current_time = round(time, 4)

        if event == 'arrival':
            self.current_number_of_jobs += 1
        else:
            self.current_number_of_jobs -= 1

    def compute_arrival(self, time: float):
        validate_number_params_not_negative_and_not_none(function_name='compute_arrival', time=time)

        if time < self.current_time:
            raise ValueError('Provided time smaller than already registered time.')

        self._count_number_of_jobs(time, 'arrival')

    def get_number_of_processed_jobs(self) -> int:
        return self.total_number_of_processed_jobs_in_system
    
    def get_mean_queue_time(self) -> float:
        return self.cumulative_queue_times / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0

    def get_mean_number_of_jobs_in_system(self) -> float:
        return (round(self.weighted_sum_number_of_jobs / self.total_simulation_time, 4)) if self.total_simulation_time > 0 else 0

    def get_throughput(self) -> float:
        return self.total_number_of_processed_jobs_in_system / self.total_simulation_time if self.total_simulation_time > 0 else 0

class EnvironmentMetrics(GeneralMetrics):
    def __init__(self, total_simulation_time: float):
        super().__init__(total_simulation_time)
        self.cumulative_time_in_system = 0
    
    def compute_departure(self, job: Job, time: float):
        validate_number_params_not_negative_and_not_none(function_name='compute_departure', time=time)
        validate_object_params_not_none(function_name='compute_departure', job=job)

        if time < self.current_time:
            raise ValueError('Provided time smaller than already registered time.')

        self._count_number_of_jobs(time, 'departure')

        self.total_number_of_processed_jobs_in_system += 1
        self.cumulative_time_in_system += (time - job.arrival_time)
        self.cumulative_queue_times += sum(job.queue_times_per_server.values())

    def get_mean_time_in_system(self) -> float:
        return self.cumulative_time_in_system / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0

class ServerMetrics(GeneralMetrics):
    def __init__(self, server_id: int, total_simulation_time: float):
        super().__init__(total_simulation_time)
        self.server_id = server_id
        self.cumulative_time_in_server = 0
        self.cumulative_server_busy_time = 0
        self.cumulative_visits_per_job = 0
    
    def compute_departure(self, time: float):
        validate_number_params_not_negative_and_not_none(function_name='compute_departure', time=time)

        if time < self.current_time:
            raise ValueError('Provided time smaller than already registered time.')

        self._count_number_of_jobs(time, 'departure')

    def compute_environment_departure(self, job: Job):
        validate_object_params_not_none(function_name='compute_environment_departure', job=job)

        self.total_number_of_processed_jobs_in_system += 1

        self.cumulative_queue_times += job.queue_times_per_server[self.server_id]
        self.cumulative_time_in_server += job.total_time_per_server[self.server_id]
        self.cumulative_server_busy_time += job.total_time_per_server[self.server_id] - job.queue_times_per_server[self.server_id]

        self.cumulative_visits_per_job += job.total_visits_per_server[self.server_id]
    
    def get_number_of_processed_jobs(self) -> int:
        return self.cumulative_visits_per_job

    def get_mean_time_in_server(self) -> float:
        return self.cumulative_time_in_server / self.cumulative_visits_per_job if self.cumulative_visits_per_job > 0 else 0

    def get_mean_visits_per_job(self) -> float:
        return self.cumulative_visits_per_job / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0

    def get_server_utilization(self) -> float:
        return self.cumulative_server_busy_time / self.total_simulation_time if self.total_simulation_time > 0 else 0

    def get_throughput(self) -> float:
        return self.cumulative_visits_per_job / self.total_simulation_time if self.total_simulation_time > 0 else 0
    
    def get_demand(self) -> float:
        return self.cumulative_time_in_server / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0

class PriorityMetrics(GeneralMetrics):
    def __init__(self, total_simulation_time: float):
        super().__init__(total_simulation_time)
        self.cumulative_time_in_system = 0
    
    def get_mean_time_in_system(self) -> float:
        return self.cumulative_time_in_system / self.total_number_of_processed_jobs_in_system if self.total_number_of_processed_jobs_in_system > 0 else 0
    
    def compute_departure(self, job: Job, time: float):
        validate_number_params_not_negative_and_not_none(function_name='compute_departure', time=time)
        validate_object_params_not_none(function_name='compute_departure', job=job)

        if time < job.arrival_time:
            raise ValueError('Provided time smaller than already registered time.')

        self.total_number_of_processed_jobs_in_system += 1
        self.cumulative_time_in_system += (time - job.arrival_time)
        self.cumulative_queue_times += sum(job.queue_times_per_server.values())