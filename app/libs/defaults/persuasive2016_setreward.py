# -*- coding: utf-8 -*-
# Persuasive 2016 Sample:
import libs.base as base
# Retrieve the average number of kilometers ran for the current weather
average = base.mean(self.get_theta(context=context))
# Compute a streaming update:
average.update(self.reward["km"])
# Store the results
self.set_theta(average, context=context)
# (Optional):
self.log_data({"context":self.context, "average": average})
