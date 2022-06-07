from . import tools


fifo_sort = lambda t: t.arrival

@tools.parameters_wrapper(sort_key=fifo_sort)
def fifo(tasks):
  exec_timeline = list()
  timelime = 0
  while tasks:
    task = tasks.pop(0)
    if timelime < task.arrival:
      timelime = task.arrival
    task.started = tools.round_digits(timelime)
    timelime += task.wcet
    task.executed = task.wcet
    task.finished = tools.round_digits(timelime)
    exec_timeline.append(task)
  return exec_timeline
