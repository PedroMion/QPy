from .distribution import IDistribution
from .queue_discipline import Discipline, IQueue
from .utils import randomly_draw_from_dictionary


class ServerExecution:
    def __init__(self, service_distribution: IDistribution, queue: IQueue):
        self.service_distribution = service_distribution
        self.queue = queue
        self.current_job_being_executed = None
        self.current_job_size = 0
        self.time_current_execution_started = 0
    
    def execute_new_job(self, job, size, time):
            self.current_job_being_executed = job
            self.current_job_size = size
            self.time_current_execution_started = time

    def remaining_time_for_current_job(self, time):
        return self.current_job_size - (time - self.time_current_execution_started)

    def job_arrival(self, job, time):
        job_size = self.service_distribution.sample()
        
        if self.current_job_being_executed == None:
            self.execute_new_job(job, job_size, time)

            return job_size
        if self.queue.discipline == Discipline.SRT and self.queue.with_preemption:
            if job_size < self.remaining_time_for_current_job(time):
                # Decide how to do this. How to impact the event queue properly
                pass
        
        self.queue.insert(job, job_size)


class Server:
    def __init__(self, service_distribution: IDistribution, queue: IQueue):
        self.server_execution = ServerExecution(service_distribution, queue)
        self.destinies = {"end": 1.0}
        self.job_count = 0
    
    def add_destination(self, destination_server, probability):
        end_probability = self.destinies["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinies["end"] -= probability
        self.destinies[destination_server] = probability

    def service_time(self):
        return self.service_distribution.sample()
    
    def get_first_in_line(self):
        return self.queue.first_in_line()
    
    def route_job(self):
        return randomly_draw_from_dictionary(self.destinies)
    
    def finish_current_job(self):
        self.job_count -= 1
        
        if self.job_count < 0:
            raise ValueError("No jobs currently in execution.")

        if self.job_count > 0:
            return self.service_time()