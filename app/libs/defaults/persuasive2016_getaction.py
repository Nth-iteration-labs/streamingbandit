# -*- coding: utf-8 -*-
# Work in progress....
import libs.tools as tls

# Retrieve average for the current weather and user:
average = tls.mean(self.get_theta(context=self.context), value_only=True)

# Compute goal:
goal = average * 1.1
self.action["distance"] = goal

# Determine activity:
if self.context["weather"] == "sunny":
    self.action["activity"] = "run"
else:
    self.action["activity"] = "swim"

# Log to database
self.log_data({"context":self.context, "goal": goal})