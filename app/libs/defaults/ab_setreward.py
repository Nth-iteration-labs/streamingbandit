# -*- coding: utf-8 -*-
import numpy as np
import time

# Options:
k = 3           # Number of versions
N = 300         # Total number of trials (set to 0 for Inf / Thomp)
log = True      # Log data to mognodb


################################################################
# Increase overall count:
n = self.get_theta().get("n",1) + 1
self.set_theta({"n":n})

# If still running increase action count
if N==0 or n<N:
    d = self.get_theta(action={'choice':self.action['choice']})
    s = d.get("s",1) + self.reward
    n = d.get("n",2) + 1
    self.set_theta({"s":s, "n":n}, action={'choice':self.action['choice']})
    
# Logging current action, time, and context JSON
# Optional
if log:
    self.log_data({
        'type' : "setreward",
        'choice' : self.action["choice"],
        'time' : int(time.time()),
        'context' : self.context
      })