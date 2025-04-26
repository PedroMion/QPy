class EnvironmentMetrics:
    def __init__(self):
        self.arrival_times = []
        self.queue_times = []
        self.time_in_system = []
    
    def compute_job(self, job, time):
        self.arrival_times.append(job.arrival_time)
        self.queue_times.append(job.time_in_queue)
        self.time_in_system.append(time - job.arrival_time)