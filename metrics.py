class EnvironmentMetrics:
    def __init__(self):
        self.arrival_times = {}
        self.time_in_system = {}
    
    def job_arrival(self, job_id, time):
        self.arrival_times[job_id] = time
    
    def job_departure(self, job_id, time):
        try:
            self.time_in_system[job_id] = time - self.arrival_times[job_id]
        except:
            raise ValueError("Trying to remove job before arrival.")