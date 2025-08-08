from typing import Optional, Union
from .distribution import IDistribution
from .event import Event
from .job import Job
from .queue_discipline import Discipline, IQueue
from .utils import randomly_draw_from_dictionary
from .validation_utils import validate_object_params_not_none, validate_number_params_not_negative_and_not_none


class ServerExecution:
    def __init__(self, service_distribution: IDistribution, queue: IQueue):
        self.service_distribution = service_distribution
        self.queue = queue

        self.reset_execution_configuration()
    
    def reset_execution_configuration(self):
        self.current_job_being_executed = None
        self.current_job_size = 0
        self.time_current_execution_started = 0

    def execute_new_job(self, job: Job, size: float, time: float):
        validate_object_params_not_none('execute_new_job', job=job)
        validate_number_params_not_negative_and_not_none(function_name='execute_new_job', size=size, time=time)

        self.current_job_being_executed = job
        self.current_job_size = size
        self.time_current_execution_started = time

    def remaining_time_for_current_job(self, time: float) -> float:
        validate_number_params_not_negative_and_not_none(function_name='remaining_time_for_current_job', time=time)

        if time < self.time_current_execution_started:
            raise ValueError(f'Job can\'t have negative reimaining time.\nCurrent time: {time} | Time execution started: {self.time_current_execution_started}')

        return self.current_job_size - (time - self.time_current_execution_started)

    def is_next_event_departure(self) -> bool:
        if self.queue.discipline == Discipline.RR:
            if self.current_job_size > self.queue.preemption_time:
                return False
        
        return True

    def job_arrival(self, job: Job, time: float, event: Event) -> Optional[float]:
        job_size = self.service_distribution.sample()
        
        if self.current_job_being_executed == None:
            self.execute_new_job(job, job_size, time)

            return job_size
        if self.queue.discipline == Discipline.SRT and self.queue.with_preemption:
            if job_size < self.remaining_time_for_current_job(time):
                self.queue.insert(self.current_job_being_executed, self.remaining_time_for_current_job(time))
                event.canceled = True

                self.execute_new_job(job, job_size, time)

                return job_size
        
        self.queue.insert(job, job_size)

    def job_departure(self, time: float) -> Optional[tuple]:
        next_job_in_line = self.queue.first_in_line()

        if next_job_in_line:
            new_job_size = next_job_in_line[0]
            new_job = next_job_in_line[1]

            self.execute_new_job(new_job, new_job_size, time)

            return next_job_in_line if self.is_next_event_departure() else (self.queue.preemption_time, new_job)
        
        self.reset_execution_configuration()
    
    def preempt(self, time: float) -> tuple:
        next_job = self.queue.first_in_line

        if next_job:
            new_job_size = next_job[0]
            new_job = next_job[1]

            self.queue.insert(self.current_job_being_executed, self.remaining_time_for_current_job(time))

            self.execute_new_job(new_job, new_job_size, time)

            return next_job if self.is_next_event_departure() else (self.queue.preemption_time, new_job)

        self.execute_new_job(self.current_job_being_executed, self.remaining_time_for_current_job(time), time)

        return (self.remaining_time_for_current_job() if self.is_next_event_departure() else self.queue.preemption_time, self.current_job_being_executed)

class Server:
    def __init__(self, id: int, service_distribution: IDistribution, queue: IQueue):
        self.id = id
        self.server_execution = ServerExecution(service_distribution, queue)
        self.destinations = {"end": 1.0}
        self.job_count = 0
    
    def add_destination(self, destination_server_id: int, probability: float):
        end_probability = self.destinations["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinations["end"] -= probability
        self.destinations[destination_server_id] = probability
    
    def route_job(self) -> Union[int, str]:
        return randomly_draw_from_dictionary(self.destinations)
    
    def is_next_event_departure(self) -> bool:
        return self.server_execution.is_next_event_departure()

    def job_arrival(self, job: Job, time: float, event: Event) -> Optional[float]:
        self.job_count += 1

        return self.server_execution.job_arrival(job, time, event)
    
    def finish_execution(self, time: float, is_preemption: bool=False) -> Optional[tuple]:
        if is_preemption:
            return self.server_execution.preempt(time)
        return self.server_execution.job_departure(time)