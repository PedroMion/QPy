from collections import defaultdict
from metrics import EnvironmentMetrics, ServerMetrics


class SimulationResults:
    def __init__(self):
        self.environment_metrics = EnvironmentMetrics()
        self.server_metrics = ServerMetrics()
        self.jobs = defaultdict(lambda: None)
    
    def show_simulation_metrics(self):
        raise NotImplementedError()