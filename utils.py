import random, numpy as np
import heapq


from job import Job


def exponential(lambda_value):
  return -np.log(1-random.random())/lambda_value

def generate_exponential_arrivals(queue, delta, server, arrival_rate, event_count):
    time = 0

    while time < delta:
        new_arrival_time = round((time + exponential(arrival_rate)), 4)

        if new_arrival_time < delta:
            new_job = Job(event_count, new_arrival_time, server)

            heapq.heappush(queue, (new_arrival_time, event_count, 'arrival', new_job, server))

        time = new_arrival_time
        event_count += 1