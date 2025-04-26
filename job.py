class Job:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.arrival_time_in_current_server = arrival_time
        self.time_in_queue = 0

    def serve(self, start_time):
        self.time_in_queue += start_time - self.arrival_time_in_current_server
    
    def reroute(self, arrival_time):
        self.arrival_time_in_current_server = arrival_time