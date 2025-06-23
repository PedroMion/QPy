from .job import Job
from abc import ABC, abstractmethod
from collections import deque


class IQueue(ABC):
    @abstractmethod
    def insert(self):
        pass
    
    @abstractmethod
    def first_in_line(self):
        pass

class FirstComeFirstServed(IQueue):
    def __init__(self):
        self.queue = deque()
    
    def insert(self, job: Job):
        self.queue.append(job)
    
    def first_in_line(self) -> Job:
        return self.queue.popleft()

class QueueDiscipline():
    def __new__(cls, *args, **kwargs):
        if cls is QueueDiscipline:
            raise TypeError("Cannot instantiate this class directly.")
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def FCFS():
        return FirstComeFirstServed()