from qpy import Environment
from Mappers.Utils.DistributionMapper import get_distribution
from Mappers.Utils.QueueMapper import get_queue_discipline


class SimulationRequestMapper:
    def __init__(self, request):
        self._request = request
        self._setup_environment()

    def _setup_environment(self):
        self._create_environment_object()
        self._add_devices()

        if self._request.connections:
            self._add_connections()

    def _create_environment_object(self):
        if self._request.networkConfiguration.networkType == "Open":
            self._env = Environment()
        else:
            self._env = Environment(number_of_terminals=int(self._request.networkConfiguration.numberOfTerminals),
                            think_time_distribution=get_distribution(self._request.networkConfiguration.thinkTimeDistribution))

    def _add_servers(self):
        for server in self._request.devices.servers:
            service_dist = get_distribution(server.distribution)
            queue_disc = None
            if server.queue:
                queue_disc = get_queue_discipline(server.queue)
            self.server_ids_mapper[server.deviceId] = self._env.add_server(service_dist, queue_disc)

    def _add_arrivals(self):
        for arrival in self._request.devices.arrivals:
            arrival_dist = get_distribution(arrival.distribution)

            priority = None
            if arrival.priorityDistribution:
                priority = {p["key"]: p["prob"] for p in arrival.priorityDistribution}

            target_server_id = self.server_ids_mapper[arrival.destination]
            self._env.add_entry_point(target_server_id, arrival_dist, priority)            

    def _add_terminal_configuration(self):
        config = self._request.terminalsConfiguration

        if config.priorityDistribution:
            priorities = {p["key"]: p["prob"] for p in config.priorityDistribution}

            self._env.add_priority_closed_network(priorities)
        
        for route in config.routes:
            target_server_id = self.server_ids_mapper[route.target]

            self._env.add_terminals_routing_probability(target_server_id, route.routingProbability)   

    def _add_devices(self):
        self.server_ids_mapper = {}
        
        self._add_servers()

        if self._request.networkConfiguration.networkType == "Open":
            self._add_arrivals()
        else:
            self._add_terminal_configuration()
    
    def _add_connections(self):
        for connection in self._request.connections:
            if connection.source.startswith("server") and connection.target.startswith("server"):
                origin = self.server_ids_mapper[connection.source]
                dest = self.server_ids_mapper[connection.target]

                self._env.add_servers_connection(origin, dest, connection.routingProbability or 1.0)
    
    def get_environemnt(self):
        return self._env