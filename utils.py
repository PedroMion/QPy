import random, numpy as np


def exponential(lambda_value):
  return -np.log(1-random.random())/lambda_value

def generate_exponential_arrivals(delta, arrival_rate):
    time = 0
    arrivals = []

    while time < delta:
        new_arrival_time = round((time + exponential(arrival_rate)), 4)

        if new_arrival_time < delta:
            arrivals.append(new_arrival_time)

        time = new_arrival_time
    
    return arrivals