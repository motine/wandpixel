#!/usr/bin/env python3

from time import sleep
from subprocess import Popen
import signal
from datetime import time, datetime

TIME_TABLE = [
  # make sure that the time table is ordered ascending!
  (time(6, 30), './start.py pan images/art/*'),
  (time(8, 30), './start.py --brightness 20 weather'),
  (time(15, 30), './start.py --brightness 255 pan images/art/*'),
  (time(20, 30), './start.py --brightness 50 pan images/art/*'),
  (time(23, 0), None),
]

current_process = None
last_time_table_item = None

try:
  while True:
    # determine current time table item
    current_time = datetime.now().time()
    past_time_table_times = list(filter(lambda item: current_time >= item[0], TIME_TABLE))
    if past_time_table_times:
      current_time_table_item = past_time_table_times[-1]
    else:
      # it's too early, so we need to wait for the first time table entry to come into effect
      # sleep(60)
      sleep(5)
      continue

    # check & subsititute process
    time_table_item_changed = current_time_table_item != last_time_table_item
    process_died = current_process == None or current_process.poll() != None
    if time_table_item_changed or (process_died and current_time_table_item[1]):
      if current_process != None: # stop the process before
        current_process.send_signal(signal.SIGINT)
        current_process.wait()
      command = current_time_table_item[1]
      if command: # if there is no command we do nothing
        current_process = Popen("exec " + current_time_table_item[1], shell=True) # start the new one; see https://stackoverflow.com/a/13143013
    last_time_table_item = current_time_table_item

    # wait
    sleep(5)
finally:
  if current_process != None:
    current_process.send_signal(signal.SIGINT)
    current_process.wait()
