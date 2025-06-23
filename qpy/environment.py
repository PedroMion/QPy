from .distribution import IDistribution
from .execution import Execution
from .network import ClosedNetwork, OpenNetwork
from .queue_discipline import IQueue
from .results import SimulationResults
from .utils import validade_priority_input
from typing import Optional
from pydantic import validate_call


class Environment():
    @validate_call
    def __init__(self, number_of_terminals: Optional[int] = None, average_think_time: Optional[float] = None, time_unit: str = 'seconds'):
        self.network = None
        self.is_closed = False
        self.time_unit = time_unit
        
        if number_of_terminals is None or average_think_time is None:
            self.network = OpenNetwork()
        else:
            self.network = ClosedNetwork(average_think_time, number_of_terminals)
            self.is_closed = True
    
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def add_server(self, service_distribution: IDistribution, queue_discipline: Optional[IQueue] = None):        
        self.network.add_server(service_distribution, queue_discipline)
    
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def add_entry_point(self, server_id: int, arrival_distribution: IDistribution, priority_distribution: Optional[dict] = None):
        if not self.is_closed:
            self.network.add_entry_point(server_id, arrival_distribution, validade_priority_input(priority_distribution))
        else:
            raise ValueError('Closed network does not allow entry points')
        
    @validate_call
    def add_priority_closed_network(self, priorities: dict):
        if self.is_closed:
            self.network.add_priorities(priorities)
    
    @validate_call
    def add_terminals_routing_probability(self, destination_server_id: int, probability: float):
        if self.is_closed:
            self.network.add_terminals_routing_probability(destination_server_id, probability)
        else:
            raise ValueError('Open network does not allow terminal routing')
    
    @validate_call
    def simulate(self, time_in_seconds: float, warmup_time: float) -> SimulationResults:
        queue = self.network.generate_jobs(time_in_seconds + warmup_time)

        new_execution = Execution(time_in_seconds, warmup_time, queue, self.network, self.time_unit)

        return new_execution.execute()