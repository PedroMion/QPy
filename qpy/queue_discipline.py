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
    PRIORITY = auto()

class IQueue(ABC):
    discipline: Discipline

    @abstractmethod
    def insert(self, job, service_time):
        pass
    
    @abstractmethod
    def first_in_line(self):
        pass

    @abstractmethod
    def with_preemption(self):
        pass

class FirstComeFirstServed(IQueue):
    def __init__(self):
        self.queue = deque()
        self.discipline = Discipline.FCFS
    
    def insert(self, job: Job, service_time: float = None):
        self.queue.append((service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return self.queue.popleft()
        except:
            return
    
    def with_preemption(self):
        return False

class LastComeFirstServed(IQueue):
    def __init__(self):
        self.queue = deque()
        self.discipline = Discipline.LCFS
    
    def insert(self, job: Job, service_time: float = None):
        self.queue.append((service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return self.queue.pop()
        except:
            return

    def with_preemption(self):
        return False

class ShortestRemainingTime(IQueue):
    def __init__(self, with_preemption: bool = False):
        self.queue = []
        self.preemption = with_preemption
        self.discipline = Discipline.SRT
    
    def insert(self, job: Job, service_time: float):
        heapq.heappush(self.queue, (service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return heapq.heappop(self.queue)
        except:
            return

    def with_preemption(self):
        return self.preemption

class RoundRobin(IQueue):
    def __init__(self, preemption_time: float):
        self.queue = deque()
        self.preemption_time = preemption_time
        self.discipline = Discipline.RR
    
    def insert(self, job: Job, service_time: float = None):
        self.queue.append((service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return self.queue.popleft()
        except:
            return
    
    def with_preemption(self):
        return True

class PriorityQueue(IQueue):
    def __init__(self, with_preemption: bool = False):
        self.queue = []
        self.preemption = with_preemption
        self.discipline = Discipline.PRIORITY

    def insert(self, job: Job, service_time: float):
        heapq.heappush(self.queue, (-job.priority, job.arrival_time_at_current_server, job, service_time))
    
    def first_in_line(self):
        try:
            queue_element = heapq.heappop(self.queue)

            return (queue_element[2], queue_element[3])
        except:
            return
    
    def with_preemption(self):
        return self.preemption

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
    
    @staticmethod
    @validate_call
    def priority_queue(with_preemption: Optional[bool] = False):
        return PriorityQueue(with_preemption)