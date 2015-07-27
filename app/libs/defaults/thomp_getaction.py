# -*- coding: utf-8 -*-
import numpy as np
import time

# Options:
k = 3           # Number of versions
log = True      # Log data to mognodb

################################################################

# Select the winner using Thompson sampling:
winner = 0
value = 0
for i in range(1,(k+1)):
    d = self.get_theta(action={'choice':i})
    est = np.random.beta(d.get("s",1), (d.get("n",2)-d.get("s",1)))
    if est > value:
        value = est
        winner = i
self.action['choice'] = winner
            
# Logging current action, time, and context JSON (Optional)
if log:
    self.log_data({
        'choice' : self.action["choice"],
        'time' : int(time.time()),
        'context' : self.context
      })