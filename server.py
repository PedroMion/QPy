from utils import get_service_time_from_average_and_distribution, randomly_draw_from_dictionary


class Server:
    def __init__(self, average_service_time, service_time_distribution, queue_discipline='FCFS'):
        self.average_service_time = average_service_time
        self.service_time_distribution = service_time_distribution
        self.queue_discipline = queue_discipline
        self.queue = []
        self.destinies = {"end": 1.0}
        self.job_count = 0
    
    def add_destination(self, destination_server, probability):
        end_probability = self.destinies["end"]

        if probability > end_probability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinies["end"] -= probability
        self.destinies[destination_server] = probability

    def service_time(self):
        return get_service_time_from_average_and_distribution(1 / self.average_service_time, self.service_time_distribution)
    
    def get_first_in_line(self):
        return self.queue.pop(0)
    
    def route_job(self):
        return randomly_draw_from_dictionary(self.destinies)

    def add_to_queue(self, job):
        self.job_count += 1

        if self.job_count == 1:
            return self.service_time()

        if job.priority == 0:
            self.queue.append(job)
        else:
            index = 0
            while index < len(self.queue):
                if job.priority > self.queue[index].priority:
                    break
                index += 1
            self.queue.insert(index, job)

        return
    
    def finish_current_job(self):
        self.job_count -= 1
        
        if self.job_count < 0:
            raise ValueError("No jobs currently in execution.")

        if self.job_count > 0:
            return self.service_time()