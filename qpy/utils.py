import random, numpy as np
import heapq


from .job import Job
from .enums import DistributionType


def randomly_draw_from_dictionary(probabilities):
  probability = random.random()
  probability_sum = 0

  for possible_value in probabilities.keys():
    probability_sum += probabilities[possible_value]

    if probability <= probability_sum:
        return possible_value

def constant(value):
   return value

def exponential(lambda_value):
  return -np.log(1-random.random())/lambda_value

def normal(mu, sigma):
  return random.gauss(mu, sigma)

def uniform(a, b):
  return random.uniform(a, b)

def route_distribution(average_service_rate, distribution):
  if distribution == DistributionType.CONSTANT:
    return constant(average_service_rate)
  elif distribution == DistributionType.EXPONENTIAL:
    return exponential(average_service_rate)
  else:
    raise ValueError(f'Unsupported distribution: {distribution}')

def randomize_priority(priorities):
  if priorities:
    return randomly_draw_from_dictionary(priorities)
  return 0

def validate_distribution_input(input):
  if DistributionType.is_valid(input):
    return input
  return 'exponential'  # Decide later between using exponential as default or raising exception

def validade_priority_input(input):
  if not input:
    return

  cumulative_sum = 0

  try:
    for key in input.keys():
      if int(key) >= 0:
        cumulative_sum += input[key]
      else:
        raise Exception
    if round(cumulative_sum) != 1:
      for key in input.keys():
        input[key] = round(input[key] / cumulative_sum, 4)
    
    return input
  except:
    raise ValueError("Wrong priority distribution. Input has to be dictionary containing integer (priority) as keys and double (probability) as value. Lower piorities will be executed first.")

def get_service_time_from_average_and_distribution(average_service_rate, distribution):
  return route_distribution(average_service_rate, distribution)


def generate_new_job_closed_network(queue, event_count, time, average_think_time, routing_probabilities, priorities):
  routing = 'end'
  think_time = 0

  while routing == 'end':
    think_time += exponential(1 / average_think_time)
    routing = randomly_draw_from_dictionary(routing_probabilities)

  new_job = Job(event_count, time + think_time, routing, randomize_priority(priorities))

  heapq.heappush(queue, (time + think_time, event_count, 'arrival', new_job, routing))
    

def generate_arrivals(queue, delta, server, arrival_rate, arrival_distribution, priorities, event_count):
  time = 0

  while time < delta:
      new_arrival_time = round((time + route_distribution(arrival_rate, arrival_distribution)), 4)

      if new_arrival_time < delta:
          new_job = Job(event_count, new_arrival_time, server, randomize_priority(priorities))

          heapq.heappush(queue, (new_arrival_time, event_count, 'arrival', new_job, server))

      time = new_arrival_time
      event_count += 1