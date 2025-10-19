from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class DistributionModel(BaseModel):
    distribution: str
    params: Dict[str, Any]

class QueueModel(BaseModel):
    queueDiscipline: str
    params: Dict[str, Any]

class ServerModel(BaseModel):
    device_id: str
    distribution: DistributionModel
    queue: Optional[QueueModel] = None

class ArrivalModel(BaseModel):
    device_id: str
    distribution: DistributionModel
    priorityDistribution: Optional[List[Dict[str, Any]]] = None

class ConnectionModel(BaseModel):
    source: str
    target: str
    routingProbability: Optional[float] = None

class NetworkParametersModel(BaseModel):
    simulationTime: float
    warmupTime: float

class NetworkConfigurationModel(BaseModel):
    type: str
    numberOfTerminals: str
    averageThinkTime: str

class SimulationRequest(BaseModel):
    networkParameters: NetworkParametersModel
    networkConfiguration: NetworkConfigurationModel
    devices: Dict[str, List[Any]]
    connections: List[ConnectionModel]