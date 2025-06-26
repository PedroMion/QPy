import heapq


from .job import Job
from abc import ABC, abstractmethod
from collections import deque
from enum import  auto, Enum
from pydantic import validate_call
from typing import Optional


class Discipline(Enum):
    FCFS = auto()
    LCFS = auto()
    SRT  = auto()
    RR   = auto()

class IQueue(ABC):
    discipline: Discipline

    @abstractmethod
    def insert(self, job, service_time):
        pass
    
    @abstractmethod
    def first_in_line(self):
        pass

class FirstComeFirstServed(IQueue):
    def __init__(self):
        self.queue = deque()
        self.discipline = Discipline.FCFS
    
    def insert(self, job: Job, service_time: float = None):
        self.queue.append(job)
    
    def first_in_line(self) -> Job:
        return self.queue.popleft()

class LastComeFirstServed(IQueue):
    def __init__(self):
        self.queue = deque()
        self.discipline = Discipline.LCFS
    
    def insert(self, job: Job, service_time: float = None):
        self.queue.append(job)
    
    def first_in_line(self) -> Job:
        return self.queue.pop()

class ShortestRemainingTime(IQueue):
    def __init__(self, with_preemption: bool = False):
        self.queue = []
        self.with_preemption = with_preemption
        self.discipline = Discipline.SRT
    
    def insert(self, job: Job, service_time: float):
        heapq.heappush(self.queue, (service_time, job))
    
    def first_in_line(self):
        return heapq.heappop(self.queue)[1]

class RoundRobin(IQueue):
    def __init__(self, preemption_time: float):
        self.queue = deque
        self.preemption_time = preemption_time
        self.discipline = Discipline.RR
    
    def insert(self, job: Job, service_time: float = None):
        self.queue.append(job)
    
    def first_in_line(self) -> Job:
        return self.queue.popleft()

class QueueDiscipline():
    def __new__(cls, *args, **kwargs):
        if cls is QueueDiscipline:
            raise TypeError("Cannot instantiate this class directly.")
        return super().__new__(cls, *args, **kwargs)

    @staticmethod
    def fcfs():
        return FirstComeFirstServed()
    
    @staticmethod
    def lcfs():
        return LastComeFirstServed()

    @staticmethod
    @validate_call
    def srt(with_preemption: Optional[bool] = True):
        return ShortestRemainingTime(with_preemption)
    
    @staticmethod
    @validate_call
    def round_robin(preemption_time: float):
        return RoundRobin(preemption_time)