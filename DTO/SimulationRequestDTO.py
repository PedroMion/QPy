from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class DistributionModel(BaseModel):
    distribution: str
    params: Dict[str, Any]

class QueueModel(BaseModel):
    queueDiscipline: str
    params: Dict[str, Any]

class ServerModel(BaseModel):
    deviceId: str
    distribution: DistributionModel
    queue: Optional[QueueModel] = None

class ArrivalModel(BaseModel):
    deviceId: str
    distribution: DistributionModel
    destination: str
    priorityDistribution: Optional[List[Dict[str, Any]]] = None

class ConnectionModel(BaseModel):
    source: str
    target: str
    routingProbability: Optional[float] = None

class TerminalRoutingModel(BaseModel):
    target: str
    routingProbability: Optional[float] = None

class TerminalConfigurationModel(BaseModel):
    routes: List[TerminalRoutingModel]
    priorityDistribution: Optional[List[Dict[str, Any]]] = None

class NetworkParametersModel(BaseModel):
    simulationTime: float
    warmupTime: float

class NetworkConfigurationModel(BaseModel):
    networkType: str
    numberOfTerminals: Optional[int] = None 
    thinkTimeDistribution: Optional[DistributionModel] = None

class DevicesModel(BaseModel):
    servers: List[ServerModel]
    arrivals: Optional[List[ArrivalModel]] = None

class SimulationRequest(BaseModel):
    networkParameters: NetworkParametersModel
    networkConfiguration: NetworkConfigurationModel
    devices: DevicesModel
    terminalsConfiguration: Optional[TerminalConfigurationModel] = None
    connections: Optional[List[ConnectionModel]] = None