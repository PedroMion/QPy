import random, numpy as np
import heapq


from job import Job


def randomly_draw_from_dictionary(probabilities):
  probability = random.random()
  probability_sum = 0

  for destiny in probabilities.keys():
    probability_sum += probabilities[destiny]

    if probability <= probability_sum:
        return destiny

def exponential(lambda_value):
  return -np.log(1-random.random())/lambda_value

def generate_new_job_closed_network(queue, event_count, time, average_think_time, routing_probabilities):
    routing = 'end'
    think_time = 0

    while routing == 'end':
      think_time += exponential(1 / average_think_time)
      routing = randomly_draw_from_dictionary(routing_probabilities)

    new_job = Job(event_count, time + think_time, routing)

    heapq.heappush(queue, (time + think_time, event_count, 'arrival', new_job, routing))
    

def generate_exponential_arrivals(queue, delta, server, arrival_rate, event_count):
    time = 0

    while time < delta:
        new_arrival_time = round((time + exponential(arrival_rate)), 4)

        if new_arrival_time < delta:
            new_job = Job(event_count, new_arrival_time, server)

            heapq.heappush(queue, (new_arrival_time, event_count, 'arrival', new_job, server))

        time = new_arrival_time
        event_count += 1