import matplotlib.pyplot as plt


def task_amount_wait_time_plot(intensity, data, out_dir='.'):
  save_plot(
    file=f'{out_dir}/time-tasks.png',
    title=f'Wait_time(tasks) for intensity = {intensity}',
    data=data,
    xy=(0, 1),
    labels=('tasks', 'wait_time')
  )


def tasks_intensity_idle_and_wait(data, out_dir='.'):
  plots = [
    ['Wait_time(intensity)', f'{out_dir}/time-intensity.png', data, (0, 1), ('intensity', 'wait_time')],
    ['Idle(intensity)', f'{out_dir}/idle-intensity.png', data, (0, 2), ('intensity', 'idle')]
  ]
  for params in plots: save_plot(*params)


def save_plot(title, file, data, xy, labels):
  figure = plt.gcf()
  plt.title(title)
  x, y = xy
  label_x, label_y = labels
  plt.xlabel(label_x)
  plt.ylabel(label_y)
  for algorithm in data:
    points = data[algorithm]
    plt.plot(points[x], points[y], label=algorithm)
  plt.legend()
  figure.set_size_inches(10, 4)
  plt.savefig(file, dpi=100)
  plt.figure()
