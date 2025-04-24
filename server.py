import random


class Server:
    def __init__(self, average_service_time, queue_discipline):
        self.average_service_time = average_service_time
        self.queue_discipline = queue_discipline
        self.destinies = {"end": 1.0}
        self.queue = []
        self.busy = False
    
    def isBusy(self):
        return self.busy
    
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
        self.queue.append(job)

        return
    
    def finish_current_job(self):
        try:
            self.queue.remove(0)
            self.busy = len(self.queue) > 0
            
            return self.route_job()
        except:
            raise ValueError("No jobs currently in execution.")