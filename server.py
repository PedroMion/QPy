import random


class Server:
    def __init__(self, average_service_time, queue_discipline):
        self.average_service_time = average_service_time
        self.queue_discipline = queue_discipline
        self.destinies = {"end": 1.0}
        self.job_count = 0
    
    def is_busy(self):
        return self.job_count > 0
    
    def add_destiny(self, destiny_server, probability):
        end_probability = self.destinies["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinies["end"] -= probability
        self.destinies[destiny_server] = probability
    
    def route_job(self):
        probability = random.random()
        probability_sum = 0

        for destiny in self.destinies.keys():
            probability_sum += self.destinies[destiny]

            if probability <= probability_sum:
                return destiny

    def add_to_queue(self, job):
        self.job_count += 1

        return
    
    def finish_current_job(self):
        self.job_count -= 1
        
        if self.job_count < 0:
            raise ValueError("No jobs currently in execution.")
        return self.route_job()
