# -*- coding: utf-8 -*-
import libs.tools as tls

# Options:
k = 3           # Number of versions, A, B, C, ...k

# Retrieve proportion from store:
prop = tls.proportion(self.get_theta(action=self.action))
self.debug(prop)

# Update propotion
prop = tls.update(tls.proportion, prop, self.reward["click"])

# Store and create an index to retrieve all
#self.set_theta(prop, action=self.action, all_action=True)

# (Optional): Log the data
#self.log_data({
#        'type' : "setreward",
#        'action' : self.action["choice"],
#        'time' : int(time.time()),
#        'context' : self.context
#      })

