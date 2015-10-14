# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.tools as tls
import time
import numpy as np

# Settings:
k = 3       # Number of versions

# Tetrieve objects:
Theta = self.get_theta(all_action=True)

# Assign random or to the highest proportion:
self.action["choice"] = tls.bernbandit_thompson(Theta, k)

# (Optional): Log the data
self.log_data({
        'type' : "getaction",
        'action' : self.action["choice"],
        'time' : int(time.time()),
        'context' : self.context
      })