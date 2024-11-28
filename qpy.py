class Server:
    def __init__(self, avgServiceTime, queueDiscipline):
        self.avgServiceTime = avgServiceTime
        self.queueDiscipline = queueDiscipline
        self.destinies = {"end": 1.0}
        self.arrivals = []
    
    def addArrival(self, avgArrivalTime):
        self.arrivals.append(avgArrivalTime)
    
    def addDestiny(self, destinyServer, probability):
        endProbability = self.destinies["end"]

        if probability > endProbability:
            raise ValueError("Too many probabilities, values exceeding 1")
        
        self.destinies["end"] -= probability
        self.destinies[destinyServer] = probability

class Environment:
    def __init__(self, numOfTerminals=None, avgThinkTime=None):
        self.servers = []
        
        if numOfTerminals is None or avgThinkTime is None:
            self.closed = False
        else:
            self.closed = True
            self.numOfTerminals = numOfTerminals
            self.avgThinkTime = avgThinkTime
    
    def addServer(self, avgServiceTime, queueDiscipline = 'FCFS'):
        try:
            avgServiceTime = float(avgServiceTime)
        except ValueError:
            raise ValueError("Average service time must be double")
        
        if queueDiscipline != 'SRT' and queueDiscipline != 'FCFS':
            queueDiscipline = 'FCFS'
        
        self.servers.append(Server(avgServiceTime, queueDiscipline))

        return len(self.servers) - 1

    def addEntryPoint(self, serverId, avgArrivalTime):
        if serverId >= 0 and serverId < len(self.servers):
            self.servers[serverId].addArrival(avgArrivalTime)
            return
        raise ValueError("The provided serverId is not valid.")
