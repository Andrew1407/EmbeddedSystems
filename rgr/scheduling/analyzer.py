from .datastructs import QueueExecuted


def analyze(tasks, exec_timeline):
  grouped = group_chunks(exec_timeline)
  return QueueExecuted(
    tasks=tasks,
    timeline=exec_timeline,
    idle=get_idle(exec_timeline),
    wait_time_avg=get_avg_wait(grouped),
    missed_deadlines=get_missed_deadlines(grouped)
  )


def get_idle(chunks):
  finished = max(t.finished for t in chunks)
  active_time = sum(t.executed for t in chunks)
  return (finished - active_time) / finished


def get_missed_deadlines(grouped):
  finished = [ grouped[key][-1] for key in grouped ]
  missed = [ t for t in finished if t.deadline < t.finished ]
  return len(missed)


def get_avg_wait(grouped):
  wait_list = list()
  for key in grouped:
    group = grouped[key]
    last_chunk = group[-1]
    wait_time = last_chunk.finished - last_chunk.wcet - last_chunk.arrival
    wait_list.append(wait_time)
  return sum(wait_list) / len(wait_list)


def group_chunks(chunks):
  groups = dict()
  key_template = '{}|{}|{}'
  for t in chunks:
    key = key_template.format(t.arrival, t.wcet, t.deadline)
    group = groups.get(key)
    if group is None:
      group = groups[key] = list()
    group.append(t)
  return groups
