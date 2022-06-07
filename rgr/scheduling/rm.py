from .tools import parameters_wrapper
from .priority_scheduler import priority_scheduler


rm_sort = lambda t: (t.arrival, t.wcet)

@parameters_wrapper(sort_key=rm_sort)
def rate_monotonic(tasks):
  return priority_scheduler(tasks, rm_sort)
