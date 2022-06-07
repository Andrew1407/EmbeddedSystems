from dataclasses import dataclass

@dataclass
class Task:
  arrival: float
  wcet: float
  deadline: float
  executed: float = 0
  started: float = 0
  finished: float = 0


@dataclass
class QueueExecuted:
  timeline: list[Task]
  tasks: list[Task]
  wait_time_avg: float
  idle: float
  missed_deadlines: int
