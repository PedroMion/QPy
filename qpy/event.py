from .job import Job


class Event:
    def __init__(self, current_time: float, event_id: int, event_type: str, job: Job, server_id: int):
        self.current_time = current_time
        self.id = event_id
        self.type = event_type
        self.job = job
        self.server_id = server_id
        self.canceled = False