# -*- coding: utf-8 -*-
# Work in progress....
import libs.base as base 
# Retrieve average for the current weather and user:
average = base.mean(self.get_theta(context=self.context))
# Compute goal:
self.action["distance"] = average * 1.1
# Set action
self.action["type"] = "run" if self.context["weather"] == "sunny" else "swim"
# Log to database
self.log_data({"context":self.context, "goal": goal})
