from typing import List, Optional
from pydantic import BaseModel


class ServerModel(BaseModel):
    serverId: str
    processedJobs: int
    averageTimeInServer: float
    averageQueueTime: float
    averageNumberOfJobs: float
    averageVisitsPerJob: float
    utilization: float
    throughput: float
    demand: float

class PriorityModel(BaseModel):
    priority: int
    processedJobs: int
    averageTimeInSystem: float
    averageQueueTime: float

class EnvironmentsModel(BaseModel):
    processedJobs: int
    averageTimeInSystem: float
    averageQueueTime: float
    averageNumberOfJobs: float
    throughput: float
    maxDemand: float

class SimulationResult(BaseModel):
    environment: EnvironmentsModel
    servers: List[ServerModel]
    priority: Optional[List[PriorityModel]] = None