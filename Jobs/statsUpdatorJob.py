import traceback
import time
from threading import Thread
from Jobs.Tasks import lolStatUpdatorTask
isStarted = False
sleepAmount = 900



def start():
  thread = Thread(target=doStart)
  thread.start()

def doStart():
  print('in do Start()')
  global isStarted
  if isStarted:
    raise Exception("Couldn't start updator job as its already in process")
  isStarted = True
  while True:
    try:
      print('started sleep')
      time.sleep(sleepAmount)
      print('started job!')
      lolStatUpdatorTask.updateDBStats()
    except:
      traceback.print_exc()