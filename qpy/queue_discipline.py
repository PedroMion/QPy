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
    def clear(self):
        pass

    @abstractmethod
    def with_preemption(self):
        pass

class FirstComeFirstServed(IQueue):
    def __init__(self):
        self._queue = deque()
        self.discipline = Discipline.FCFS
    
    def insert(self, job: Job, service_time: float):
        if job is None or service_time is None:
            return
        
        self._queue.append((service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return self._queue.popleft()
        except:
            return
    
    def clear(self):
        self._queue = deque()

    def with_preemption(self):
        return False

class LastComeFirstServed(IQueue):
    def __init__(self):
        self._queue = deque()
        self.discipline = Discipline.LCFS
    
    def insert(self, job: Job, service_time: float):
        if job is None or service_time is None:
            return

        self._queue.append((service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return self._queue.pop()
        except:
            return

    def clear(self):
        self._queue = deque()

    def with_preemption(self):
        return False

class ShortestRemainingTime(IQueue):
    def __init__(self, with_preemption: bool = False):
        self._queue = []
        self._preemption = with_preemption
        self.discipline = Discipline.SRT
    
    def insert(self, job: Job, service_time: float):
        if job is None or service_time is None:
            return
        
        heapq.heappush(self._queue, (service_time, job.arrival_time_at_current_server, job))
    
    def first_in_line(self) -> tuple:
        try:
            queue_element = heapq.heappop(self._queue)

            return (queue_element[0], queue_element[2])
        except:
            return

    def clear(self):
        self._queue = []

    def with_preemption(self):
        return self._preemption

class RoundRobin(IQueue):
    def __init__(self, preemption_time: float):
        self._queue = deque()
        self.preemption_time = preemption_time
        self.discipline = Discipline.RR
    
    def insert(self, job: Job, service_time: float):
        if job is None or service_time is None:
            return
        
        self._queue.append((service_time, job))
    
    def first_in_line(self) -> tuple:
        try:
            return self._queue.popleft()
        except:
            return
    
    def clear(self):
        self._queue = deque()

    def with_preemption(self):
        return True

class PriorityQueue(IQueue):
    def __init__(self, with_preemption: bool = False):
        self._queue = []
        self._preemption = with_preemption
        self.discipline = Discipline.PRIORITY

    def insert(self, job: Job, service_time: float):
        if job is None or service_time is None:
            return
        
        heapq.heappush(self._queue, (-job.priority, job.arrival_time_at_current_server, service_time, job))
    
    def first_in_line(self):
        try:
            queue_element = heapq.heappop(self._queue)

            return (queue_element[2], queue_element[3])
        except:
            return
    
    def clear(self):
        self._queue = []

    def with_preemption(self):
        return self._preemption

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
        if preemption_time <= 0:
            raise ValueError('Preemption time should be positive float')

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