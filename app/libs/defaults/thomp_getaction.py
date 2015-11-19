# -*- coding: utf-8 -*-
# Import tools (for updates, etc.) and time (for logging):
import libs.thompson as thmp
import time
propl = thmp.BBThompsonList(self.get_theta(key="version"), ["A","B"])
self.action["version"] = propl.thompson()

# (Optional): Log the data
self.log_data({
        'type' : "getaction",
        'action' : self.action["version"],
        'time' : int(time.time()),
        'context' : self.context
      })
