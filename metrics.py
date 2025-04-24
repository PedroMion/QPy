class EnvironmentMetrics:
    def __init__(self):
        self.arrival_times = []
        self.queue_times = []
        self.time_in_system = []
    
    def compute_job(self, job):
        return