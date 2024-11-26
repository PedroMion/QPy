class Environment:
    def __init__(self, numOfTerminals=None, avgThinkTime=None):
        if numOfTerminals is None or avgThinkTime is None:
            self.closed = False
        else:
            self.closed = True
            self.numOfTerminals = numOfTerminals
            self.avgThinkTime = avgThinkTime