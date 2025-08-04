import random
import heapq


from .distribution import IDistribution
from .event import Event
from .job import Job
from typing import Optional


def randomly_draw_from_dictionary(probabilities):
  probability = random.random()
  probability_sum = 0

  for possible_value in probabilities.keys():
    probability_sum += probabilities[possible_value]

    if probability <= probability_sum:
        return possible_value

def randomize_priority(priorities):
  if priorities:
    return randomly_draw_from_dictionary(priorities)
  return 0

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


def generate_new_job_closed_network(queue: list, event_count: int, time: float, think_time_distribution: IDistribution, routing_probabilities: dict, priorities: Optional[dict] = None):
  routing = 'end'
  think_time = 0

  while routing == 'end':
    think_time += think_time_distribution.sample()
    routing = randomly_draw_from_dictionary(routing_probabilities)

  new_job = Job(event_count, time + think_time, routing, randomize_priority(priorities))

  heapq.heappush(queue, (time + think_time, event_count, Event(time + think_time, event_count, 'arrival', new_job, routing)))
    

def generate_arrivals(queue: list, event_count: int, delta: float, server: int, arrival_distribution: IDistribution, priorities: Optional[dict] = None):
  time = 0

  while time < delta:
      new_arrival_time = round((time + arrival_distribution.sample()), 4)

      if new_arrival_time < delta:
          new_job = Job(event_count, new_arrival_time, server, randomize_priority(priorities))
          
          heapq.heappush(queue, (new_arrival_time, event_count, Event(new_arrival_time, event_count, 'arrival', new_job, server)))

      time = new_arrival_time
      event_count += 1