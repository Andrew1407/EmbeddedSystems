from dataclasses import fields
from .datastructs import Task
from .analyzer import analyze


round_digits = lambda n: round(number=n, ndigits=5)

def parameters_wrapper(sort_key):
  def decorator(algorithm):
    def wrapper(tasks):
      queue = get_queue_sorted(tasks, sort_key)
      queue_copy = [ clone_task(t) for t in queue ]
      executed = algorithm(queue)
      return analyze(queue_copy, executed)
    return wrapper
  return decorator


def clone_task(task):
  clone = Task(0, 0, 0)
  for field in fields(Task):
    setattr(clone, field.name, getattr(task, field.name))
  return clone


def get_queue_sorted(tasks, sort_key):
  queue = [ clone_task(t) for t in tasks ]
  queue.sort(key=sort_key)
  return queue


def remove_task(tasks, item):
  if item in tasks:
    index = tasks.index(item)
    del tasks[index]
