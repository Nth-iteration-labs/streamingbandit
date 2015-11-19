# -*- coding: utf-8 -*-
# Work in progress....
import libs.base as base 
key = "weather-uid"
value = self.context["weather"] + str(self.context["userid"])
# Retrieve average for the current weather and user:
average = base.Mean(self.get_theta(key=key, value=value))
# Compute goal:
self.action["distance"] = average.get_value() * 1.1
if self.action["distance"] == 0:
    self.action["distance"] = 1
# Set action
self.action["type"] = "run" if self.context["weather"] == "sunny" else "swim"
# Log to database
self.log_data({"context":self.context, "goal": goal})
