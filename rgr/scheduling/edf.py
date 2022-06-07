from .tools import parameters_wrapper
from .priority_scheduler import priority_scheduler


edf_sort = lambda t: (t.deadline, t.arrival, t.wcet)

@parameters_wrapper(sort_key=edf_sort)
def earliest_deadline_first(tasks):
  return priority_scheduler(tasks, edf_sort)
