from utils import get_service_time_from_average_and_distribution, randomly_draw_from_dictionary


class Server:
    def __init__(self, average_service_time, service_time_distribution='exponential', queue_discipline='FCFS'):
        self.average_service_time = average_service_time
        self.service_time_distribution = service_time_distribution
        self.queue_discipline = queue_discipline
        self.queue = []
        self.destinies = {"end": 1.0}
        self.job_count = 0
    
    def add_destiny(self, destiny_server, probability):
        end_probability = self.destinies["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinies["end"] -= probability
        self.destinies[destiny_server] = probability

    def service_time(self):
        return get_service_time_from_average_and_distribution(self.average_service_time, self.service_time_distribution)
    
    def get_first_in_line(self):
        return self.queue[0] 
    
    def route_job(self):
        return randomly_draw_from_dictionary(self.destinies)

    def add_to_queue(self, job):
        self.job_count += 1
        self.queue.append(job)

        if self.job_count == 1:
            return self.service_time()

        return
    
    def finish_current_job(self):
        self.job_count -= 1
        
        if self.job_count < 0:
            raise ValueError("No jobs currently in execution.")
        self.queue.pop(0)

        if self.job_count > 0:
            return self.service_time()