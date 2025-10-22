from DTO.SimulationResponseDTO import SimulationResponse, ServerModel, PriorityModel, EnvironmentModel
from qpy import SimulationResults


class SimulationResponseMapper:
    def __init__(self, results: SimulationResults):
        self._results = results
        self._response_object = None

        self._map_simulation_response()

    def _map_simulation_response(self):
        env = self._add_environment_information()
        servers = self._add_servers_information()
        priority = self._add_priority_information()

        self._response_object = SimulationResponse(environment=env, servers=servers, priority=priority)
    
    def _add_environment_information(self):
        env = self._results.environment_metrics

        return EnvironmentModel(
            processedJobs = env.get_number_of_processed_jobs(),
            averageTimeInSystem = env.get_mean_time_in_system(),
            averageQueueTime = env.get_mean_queue_time(),
            averageNumberOfJobs = env.get_mean_number_of_jobs_in_system(),
            throughput = env.get_throughput(),
            maxDemand = max(s.get_demand() for s in self._results.server_metrics)
        )

    def _add_servers_information(self):
        mapped_servers = []

        for server in self._results.server_metrics:
            server_response_object = ServerModel(
                serverId = '',
                processedJobs = server.get_number_of_processed_jobs(),
                averageTimeInServer = server.get_mean_time_in_server(),
                averageQueueTime = server.get_mean_queue_time(),
                averageNumberOfJobs = server.get_mean_number_of_jobs_in_system(),
                averageVisitsPerJob = server.get_mean_visits_per_job(),
                utilization = server.get_server_utilization(),
                throughput = server.get_throughput(),
                demand = server.get_demand()
            )

            mapped_servers.append(server_response_object)
        
        return mapped_servers
    
    def _add_priority_information(self):
        if len(self._results.priority_metrics.keys()) > 1:
            mapped_priority = []

            for key, value in sorted(self._results.priority_metrics.items()):
                priority_response_object = PriorityModel(
                    priority = key,
                    processedJobs = value.get_number_of_processed_jobs(),
                    averageTimeInSystem = value.get_mean_time_in_system(),
                    averageQueueTime = value.get_mean_queue_time()
                )

                mapped_priority.append(priority_response_object)
            
            return mapped_priority

    def get_response_object(self) -> SimulationResponse:
        return self._response_object