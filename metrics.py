class EnvironmentMetrics:
    def __init__(self):
        self.total_jobs = 0
        self.num_of_jobs_in_system = 0
        self.current_time = 0
        self.weighted_sum_num_jobs = 0
        self.arrival_times = []
        self.queue_times = []
        self.time_in_system = []
    
    def count_num_of_jobs(self, time, event):
        self.weighted_sum_num_jobs += round(self.num_of_jobs_in_system * (time - self.current_time), 4)
        self.current_time = round(time, 4)

        if event == 'arrival':
            self.num_of_jobs_in_system += 1
        else:
            self.num_of_jobs_in_system -= 1

    def compute_arrival(self, time):
        self.count_num_of_jobs(time, 'arrival')

    def compute_departure(self, job, time):
        self.count_num_of_jobs(time, 'departure')

        self.total_jobs += 1
        self.arrival_times.append(job.arrival_time)
        self.queue_times.append(job.time_in_queue)
        self.time_in_system.append(time - job.arrival_time)
    
    def num_processed_jobs(self):
        return self.total_jobs

    def mean_time_in_system(self):
        return sum(self.time_in_system) / self.total_jobs
    
    def mean_queue_time(self):
        return sum(self.queue_times) / self.total_jobs

    def mean_num_jobs_in_system(self):
        return round(self.weighted_sum_num_jobs / self.current_time, 4)