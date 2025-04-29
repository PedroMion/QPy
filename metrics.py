class EnvironmentMetrics:
    def __init__(self):
        self.num_of_jobs = 0
        self.arrival_times = []
        self.queue_times = []
        self.time_in_system = []
    
    def compute_job(self, job, time):
        self.num_of_jobs += 1
        self.arrival_times.append(job.arrival_time)
        self.queue_times.append(job.time_in_queue)
        self.time_in_system.append(time - job.arrival_time)
    
    def num_processed_jobs(self):
        return self.num_of_jobs

    def mean_time_in_system(self):
        return sum(self.time_in_system) / self.num_of_jobs
    
    def mean_queue_time(self):
        return sum(self.queue_times) / self.num_of_jobs