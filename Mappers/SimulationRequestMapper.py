from qpy import Environment, Distribution, QueueDiscipline


class SimulationRequestMapper:
    def __init__(self, request):
        self.request = request
        self._setup_environment()

    def _setup_environment(self):
        self._create_environment_object()
        self._add_devices()
        self._add_connections()

    def _create_environment_object(self):
        if self.request.networkConfiguration.networkType == "Open":
            self.env = Environment()
        else:
            self.env = Environment(number_of_terminals=int(self.request.networkConfiguration.numberOfTerminals),
                            average_think_time=int(self.request.networkConfiguration.averageThinkTime))

    def _get_distribution(self, distributionProperties):
        match distributionProperties.distribution:
            case 'exponential':
                return Distribution.exponential(lambda_value=distributionProperties.params['lambda'])
            case 'constant':
                return Distribution.constant(value=distributionProperties.params['constantValue'])
            case 'uniform':
                return Distribution.uniform(lower_bound=distributionProperties.params['lowerBound'], upper_bound=distributionProperties.params['upperBound'])
            case 'normal':
                return Distribution.normal(mu=distributionProperties.params['mu'], sigma=distributionProperties.params['sigma'])
            case _:
                raise ValueError('Distribution not allowed: ' + distributionProperties.distribution)
    
    def _get_queue_discipline(self, queueProperties):
        match queueProperties.queueDiscipline:
            case 'fcfs':
                return QueueDiscipline.fcfs()
            case 'lcfs':
                return QueueDiscipline.lcfs()
            case 'srt':
                return QueueDiscipline.srt(bool(queueProperties.params['withPreemption']))
            case 'rr':
                return QueueDiscipline.round_robin(float(queueProperties.params['preemptionTime']))
            case 'priority':
                return QueueDiscipline.priority_queue(bool(queueProperties.params['withPreemption']))
            case _:
                raise ValueError('Queue discipline not allowed: ' + queueProperties.queueDiscipline)

    def _add_servers(self):
        for server in self.request.devices.servers:
            service_dist = self._get_distribution(server.distribution)
            queue_disc = None
            if server.queue:
                queue_disc = self._get_queue_discipline(server.queue)
            self.server_ids_mapper[server.device_id] = self.env.add_server(service_dist, queue_disc)

    def _add_arrivals(self):
        for arrival in self.request.devices.arrivals:
            arrival_dist = self._get_distribution(arrival.distribution)

            priority = None
            if arrival.priorityDistribution:
                priority = {p["key"]: p["prob"] for p in arrival.priorityDistribution}

            target_server_id = self.server_ids_mapper[arrival.destination]
            self.env.add_entry_point(target_server_id, arrival_dist, priority)            

    def _add_devices(self):
        self.server_ids_mapper = {}
        
        self._add_servers()

        if self.request.networkConfiguration.networkType == "Open":
            self._add_arrivals()
        else:
            # Adiciona probabilidades de roteamento do terminal
            pass
    
    def _add_connections(self):
        for connection in self.request.connections:
            if connection.source.startswith("server") and connection.target.startswith("server"):
                origin = self.server_ids_mapper[connection.source]
                dest = self.server_ids_mapper[connection.target]

                self.env.add_servers_connection(origin, dest, connection.routingProbability or 1.0)
    
    def get_environemnt(self):
        return self.env