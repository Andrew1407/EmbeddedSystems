from .tools import remove_task, round_digits, clone_task
from functools import partial


def priority_scheduler(tasks, sort_key):
  exec_timeline = list()
  current_task = tasks[0]
  search_nearest = partial(get_best_fit_task, sort_key)
  timeline = 0
  while tasks:
    if current_task is None:
      current_task = tasks[0]
    if timeline < current_task.arrival:
      timeline = current_task.arrival
    nearest = search_nearest(tasks, current_task, timeline)
    executed = current_task.executed or current_task.wcet
    if nearest is None:
      remove_task(tasks, current_task)
      current_task.started = round_digits(timeline)
      timeline += executed
      current_task.executed = executed
      current_task.finished = round_digits(timeline)
      exec_timeline.append(current_task)
      current_task = None
    else:
      fulfilled = clone_task(current_task)
      fulfilled.executed = round_digits(nearest.arrival - timeline)
      fulfilled.started = round_digits(timeline)
      current_task.executed = round_digits(current_task.wcet - fulfilled.executed)
      timeline += current_task.executed
      current_task.finished = round_digits(timeline)
      exec_timeline.append(fulfilled)
      current_task = nearest
  return exec_timeline


def get_best_fit_task(sort_key, tasks, current, timeline):
  nearest_fits = lambda t: t.arrival > timeline and \
                           t.arrival < timeline + current.wcet
  arrived = [ t for t in tasks if nearest_fits(t) ]
  arrived.sort(key=sort_key)
  for t in arrived:
    if t.wcet < current.wcet: return t
  return None
