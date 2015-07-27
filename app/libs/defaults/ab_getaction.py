# -*- coding: utf-8 -*-
import numpy as np
import time

# Options:
k = 3           # Number of versions
N = 300           # Total number of trials
log = True      # Log data to mognodb


################################################################
# Get overall count:
n = self.get_theta().get("n",1)

# Select the version to show:
if N==0 or n<N:
    self.action['message'] = "Random action out of "+str(k)
    self.action['choice'] = np.random.randint(1,k+1)
else:
    winner = 0
    value = 0
    for i in range(1,(k+1)):
        d = self.get_theta(action={'choice':i})
        est = d.get("s",1)/d.get("n",2)
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