from .distribution import IDistribution
from .execution import Execution
from .network import ClosedNetwork, OpenNetwork
from .queue_discipline import IQueue
from .results import SimulationResults
from .utils import validade_priority_input
from typing import Optional
from pydantic import validate_call


class Environment():
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def __init__(self, number_of_terminals: Optional[int] = None, think_time_distribution: Optional[IDistribution] = None, time_unit: str = 'seconds'):
        """
        Initializes the Environment object. Determines if the network is open or closed based on the input.

        Parameters
        ----------
        number_of_terminals : int - Optional
            The number of terminals in a closed network. If not provided, an open network is created.
        
        think_time_distribution : IDistribution - Optional
            The distribution used for the think time between requests in a closed network.
        
        time_unit : str - Optional
            The unit of time used for reporting results. Default is 'seconds'.
        """
        self.network = None
        self.is_closed = False
        self.time_unit = time_unit    
        
        if number_of_terminals is None or think_time_distribution is None:
            self.network = OpenNetwork()
        else:
            self.network = ClosedNetwork(think_time_distribution, number_of_terminals)
            self.is_closed = True
    
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def add_server(self, service_distribution: IDistribution, queue_discipline: Optional[IQueue] = None) -> int:
        """
        Function used to add a server to the environment.

        Parameters
        ----------
        service_distribution : IDistribution - Required
            The distribution from which the time samples are going to be drawn for each job. To check for options, see the factory class Distribution.
        
        queue_discipline : IQueue - Optional
            The queue discipline used on this server's queue. If not provided, FCFS is going to be used. To check for options, see the factory class QueueDiscipline.

        Returns
        -------
        int
            The server ID you must use to add entry points and/or connections to other servers, starting with 0.
        """
        return self.network.add_server(service_distribution, queue_discipline)
    
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def add_entry_point(self, server_id: int, arrival_distribution: IDistribution, priority_distribution: Optional[dict] = None):
        """
        Adds an entry point to a server in an open network.

        Parameters
        ----------
        server_id : int - Required
            The ID of the server where the entry point will be added.
        
        arrival_distribution : IDistribution - Required
            The distribution from which job arrival times are sampled.
        
        priority_distribution : dict - Optional
            A dictionary defining the priority distribution of arriving jobs. The dictionary should map integer (priority) to float (probability)

        Raises
        ------
        ValueError
            If the network is closed, entry points are not allowed.
        """
        if not self.is_closed:
            self.network.add_entry_point(server_id, arrival_distribution, validade_priority_input(priority_distribution))
        else:
            raise ValueError('Closed network does not allow entry points')

    @validate_call
    def add_servers_connection(self, origin_server_id: int, destination_server_id: int, routing_probability: float):
        """
        Creates a connection between two servers with a specified routing probability.

        Parameters
        ----------
        origin_server_id : int - Required
            The ID of the server from which jobs are routed.
        
        destination_server_id : int - Required
            The ID of the server to which jobs are routed.
        
        routing_probability : float - Required
            The probability of routing a job from the origin to the destination server.
        """
        self.network.add_servers_connection(origin_server_id, destination_server_id, routing_probability)
    
    @validate_call
    def add_priority_closed_network(self, priorities: dict):
        """
        Sets job priorities for a closed network, if you'd like to use them.

        Parameters
        ----------
        priorities : dict - Required
            A dictionary defining the job priorities for each class or job type.

        Raises
        ------
        ValueError
            If the network is not closed, this function can't be used.
        """
        if self.is_closed:
            self.network.add_priorities(priorities)
        else:
            raise ValueError('Open networks can\'t have priority without an entry point')
    
    @validate_call
    def add_terminals_routing_probability(self, destination_server_id: int, probability: float):
        """
        Sets the routing probability from terminals to a specific server in a closed network.

        Parameters
        ----------
        destination_server_id : int - Required
            The ID of the server to which terminals route jobs.
        
        probability : float - Required
            The probability that a terminal sends a job to the specified server.

        Raises
        ------
        ValueError
            If the network is open, terminal routing is not allowed.
        """
        if self.is_closed:
            self.network.add_terminals_routing_probability(destination_server_id, probability)
        else:
            raise ValueError('Open network does not allow terminal routing')
    
    @validate_call
    def simulate(self, time_in_seconds: float, warmup_time: float) -> SimulationResults:
        """
        Runs the simulation for the specified time, including a warm-up period. Without the warm-up, the metrics could be compromised.

        Parameters
        ----------
        time_in_seconds : float - Required
            The total simulation time, excluding the warm-up period.
        
        warmup_time : float - Required
            The warm-up period before collecting statistics. Jobs executed during this time are ignored in the results.

        Returns
        -------
        SimulationResults
            An object containing the metrics and results from the simulation.
        """
        queue = self.network.generate_jobs(time_in_seconds + warmup_time)

        new_execution = Execution(time_in_seconds, warmup_time, queue, self.network, self.time_unit)

        return new_execution.execute()