from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class DistributionModel(BaseModel):
    distribution: str
    params: Dict[str, str]

class QueueModel(BaseModel):
    queueDiscipline: str
    params: Dict[str, str]

class ServerModel(BaseModel):
    device_id: str
    distribution: DistributionModel
    queue: Optional[QueueModel] = None

class ArrivalModel(BaseModel):
    device_id: str
    distribution: DistributionModel
    destination: str
    priorityDistribution: Optional[List[Dict[str, str]]] = None

class ConnectionModel(BaseModel):
    source: str
    target: str
    routingProbability: Optional[float] = None

class NetworkParametersModel(BaseModel):
    simulationTime: float
    warmupTime: float

class NetworkConfigurationModel(BaseModel):
    networkType: str
    numberOfTerminals: str
    averageThinkTime: str

class SimulationRequest(BaseModel):
    networkParameters: NetworkParametersModel
    networkConfiguration: NetworkConfigurationModel
    servers: List[ServerModel]
    arrivals: List[ArrivalModel]
    connections: List[ConnectionModel]