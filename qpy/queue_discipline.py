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
        """
        Returns a queue with discipline First Come First Served (FCFS). 
        This is the standard queue discipline used in most applications.
        """
        return FirstComeFirstServed()
    
    @staticmethod
    def lcfs():
        """
        Returns a queue with discipline Last Come First Served (LCFS).
        In this discipline, the most recently arrived job is served first.
        """
        return LastComeFirstServed()

    @staticmethod
    @validate_call
    def srt(with_preemption: Optional[bool] = True):
        """
        Returns a queue with discipline Shortest Remaining Time (SRT).

        Parameters
        ----------
        with_preemption : bool - Optional
            If True, enables preemption. A job in service may be preempted if a new job arrives with a shorter remaining time. Default is True.
        """
        return ShortestRemainingTime(with_preemption)
    
    @staticmethod
    @validate_call
    def round_robin(preemption_time: float):
        """
        Returns a queue with discipline Round Robin.

        Parameters
        ----------
        preemption_time : float - Required
            The time quantum after which the current job is preempted and the next one is served.
        """
        return RoundRobin(preemption_time)
    
    @staticmethod
    @validate_call
    def priority_queue(with_preemption: Optional[bool] = False):
        """
        Returns a queue with discipline Priority Queue.

        Parameters
        ----------
        with_preemption : bool - Optional
            If True, enables preemption based on job priority. A job in service may be preempted by a higher-priority job. Default is False.
        """
        return PriorityQueue(with_preemption)