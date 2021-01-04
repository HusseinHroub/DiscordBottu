import traceback
import time
from Jobs.Tasks import lolStatUpdatorTask
isStarted = False
sleepAmount = 900



def start():
  if isStarted:
    raise Exception("Couldn't start updator job as its already in process")
  while True:
    try:
      time.sleep(sleepAmount)
      lolStatUpdatorTask.updateDBStats()
    except:
      traceback.print_exc()
