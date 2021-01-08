import traceback
import time
from threading import Thread

class JobScheduler:
  def __init__(self, task, timePeriodInSeconds):
    self.task = task
    self.timePeriodInSeconds = timePeriodInSeconds
    self.isStarted = False

  def start(self):
    thread = Thread(target=self.doStart)
    thread.start()

  def doStart(self):
    if self.isStarted:
      raise Exception("Couldn't start updator job as its already in process")
    self.isStarted = True
    while True:
      try:
        time.sleep(self.timePeriodInSeconds)
        self.task.execute()
      except:
        traceback.print_exc()