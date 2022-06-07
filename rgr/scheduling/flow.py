from math import exp, factorial
from random import uniform, choice, randint
from .datastructs import Task
from .tools import round_digits


get_poisson_value = lambda l, x: pow(l, x) * exp(-l) / factorial(x)

def get_poisson_random(intensity):
  get_distribution_value = lambda x: get_poisson_value(intensity, x)
  distribution_sum = exp(-intensity)
  rand = 0
  limit = uniform(0, 1)
  while limit > distribution_sum:
    rand += 1
    distribution_sum += get_distribution_value(rand)
  return rand


def erlang_tasks_flow(order, interval, intensity, wcets):
  i = 0
  skippable = 0
  while True:
    start = i
    i += 1
    bounds = start * interval, i * interval
    tasks_count = get_poisson_random(intensity)
    for _ in range(tasks_count):
      arrival = uniform(*bounds)
      wcet = choice(wcets)
      k = randint(10, 20)
      deadline = arrival + wcet * k
      task = Task(arrival=round_digits(arrival), wcet=round_digits(wcet), deadline=round_digits(deadline))
      skippable += 1
      if skippable == order:
        skippable = 0
        yield task
