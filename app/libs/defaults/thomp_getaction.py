# -*- coding: utf-8 -*-
import libs.thompson as thmp
propl = thmp.BBThompsonList(self.get_theta(key="Treatment"), ["1","2","3","4"])
self.action["Treatment"] = propl.thompson()

# (Optional): Log the data
import time
self.log_data({
        'type' : "getaction",
        'action' : self.action["Treatment"],
        'time' : int(time.time()),
        'context' : self.context
      })
