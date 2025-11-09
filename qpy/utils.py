import random
import heapq


from .distribution import IDistribution
from .event import Event
from .job import Job
from .validation_utils import validate_object_params_not_none
from collections import defaultdict
from typing import Optional


def _randomize_priority(priorities):
  if priorities:
    return randomly_draw_from_dictionary(priorities)
  return 0

def randomly_draw_from_dictionary(probabilities):
  validate_object_params_not_none(function_name='randomly_draw_from_dictionary', probabilities=probabilities)

  probability = random.random()
  probability_sum = 0

  for possible_value in probabilities.keys():
    probability_sum += probabilities[possible_value]

    if probability <= probability_sum:
        return possible_value

def transform_input_closed_network(input):
  validate_object_params_not_none(function_name='transform_input_closed_network', input=input)

  if 'end' not in input:
    return input
  
  if input['end'] == 1:
    raise ValueError('Closed network need to have at least one route from terminals')

  margin = 1 - input['end']

  new_dict = defaultdict(lambda: 0)
  for key in input.keys():
    if key != 'end':
      new_dict[key] = round(input[key] / margin, 4)

  return new_dict

def validate_priority_input(input, with_priority = True):
  if not input or not with_priority:
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
    raise ValueError("Wrong priority distribution. Input has to be dictionary containing integer (priority) as keys and double (probability) as value. Higher piorities will be executed first.")


def generate_new_job_closed_network(queue: list, event_count: int, time: float, think_time_distribution: IDistribution, routing_probabilities: dict, priorities: Optional[dict] = None):
  routing = 'end'
  think_time = 0

  while routing == 'end':
    think_time += think_time_distribution.sample()
    routing = randomly_draw_from_dictionary(routing_probabilities)

  new_job = Job(event_count, round(time + think_time, 4), routing, _randomize_priority(priorities))

  heapq.heappush(queue, (round(time + think_time, 4), event_count, Event(time + think_time, event_count, 'arrival', new_job, routing)))
  event_count += 1
    

def generate_arrivals(queue: list, event_count: int, delta: float, server: int, arrival_distribution: IDistribution, priorities: Optional[dict] = None):
  time = 0

  while time < delta:
      new_arrival_time = round((time + arrival_distribution.sample()), 4)

      if new_arrival_time < delta:
          new_job = Job(event_count, new_arrival_time, server, _randomize_priority(priorities))
          
          heapq.heappush(queue, (new_arrival_time, event_count, Event(new_arrival_time, event_count, 'arrival', new_job, server)))

      time = new_arrival_time
      event_count += 1