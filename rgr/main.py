import os
from json import dump as write_json
from functools import partial
import scheduling
import plots


OUT_DIR = 'out'

ERLANG_FLOW_ORDER = 1   # if 1 then Poisson
SIZE = 40
INTERVAL = 0.05
LAMBDA = 22.26          # (0, inf)
EXECUTION_TIME = [
  0.01133,              # lab 1
  0.00427,              # lab 2
  0.00852,              # lab 3
  0.00443,              # lab 4
  0.00159,              # lab 5
  0.02322,              # lab 6
  0.01025               # lab 7
]
ALGORITHMS = dict(
  fifo=scheduling.fifo,
  edf=scheduling.earliest_deadline_first,
  rm=scheduling.rate_monotonic
)
TASKS_QUEUE_GEN = partial(scheduling.erlang_tasks_flow, ERLANG_FLOW_ORDER)


def format_to_json(data, keys):
  formatted = list()
  for value in data:
    obj = dict()
    for key in keys:
      obj[key] = getattr(value, key)
    formatted.append(obj)
  return formatted


def save_as_file(path, data):
  with open(path, 'w') as out:
    write_json(data, out, indent=2)
    out.write('\n')


def log_values_executed():
  task_gen = TASKS_QUEUE_GEN(INTERVAL, LAMBDA, EXECUTION_TIME)
  tasks = [ next(task_gen) for _ in range(SIZE) ]
  generated_path = '%s/json/generated.json' % OUT_DIR
  tasks_formattable = ['arrival', 'wcet', 'deadline']
  res_formattable = tasks_formattable + ['executed', 'started', 'finished']
  tasks_formatted = format_to_json(tasks, tasks_formattable)
  save_as_file(generated_path, tasks_formatted)
  print('Queue size: %s' % SIZE)
  for algoritm, fn in ALGORITHMS.items():
    res = fn(tasks)
    print('\nAverage wait time (%s): %.5f' % (algoritm, res.wait_time_avg))
    print('Missed dealines (%s): %d' % (algoritm, res.missed_deadlines))
    res_formatted = format_to_json(res.timeline, res_formattable)
    res_path = '%s/json/%s.json' % (OUT_DIR, algoritm)
    save_as_file(res_path, res_formatted)


def first_plot():
  SIZE_STEP = 5
  SIZE_MAX = 500
  size_iterable = SIZE_STEP
  plot_data = dict(edf=([], []), rm=([], []), fifo=([], []))
  while size_iterable <= SIZE_MAX:
    task_gen = TASKS_QUEUE_GEN(INTERVAL, LAMBDA, EXECUTION_TIME)
    tasks = [ next(task_gen) for _ in range(size_iterable) ]
    for algoritm, fn in ALGORITHMS.items():
      res = fn(tasks)
      data = plot_data[algoritm]
      data[0].append(size_iterable)
      data[1].append(res.wait_time_avg)
    size_iterable += SIZE_STEP
  plots.task_amount_wait_time_plot(LAMBDA, plot_data, f'{OUT_DIR}/imgs')


def second_third_plots():
  INTENSITY_STEP = 1
  INTENSITY_MAX = 116
  intensity_iterable = 1
  plot_data = dict(edf=([], [], []), rm=([], [], []), fifo=([], [], []))
  while intensity_iterable <= INTENSITY_MAX:
    task_gen = TASKS_QUEUE_GEN(INTERVAL, intensity_iterable, EXECUTION_TIME)
    tasks = [ next(task_gen) for _ in range(SIZE) ]
    for algoritm, fn in ALGORITHMS.items():
      res = fn(tasks)
      data = plot_data[algoritm]
      data[0].append(intensity_iterable)
      data[1].append(res.wait_time_avg)
      data[2].append(res.idle)
    intensity_iterable += INTENSITY_STEP
  plots.tasks_intensity_idle_and_wait(plot_data, f'{OUT_DIR}/imgs')


def checkDir(dir):
  if not os.path.exists(dir):
    os.mkdir(dir)


if __name__ == '__main__':
  checkDir(OUT_DIR)
  checkDir(f'{OUT_DIR}/json')
  log_values_executed()
  checkDir(f'{OUT_DIR}/imgs')
  first_plot()
  second_third_plots()
