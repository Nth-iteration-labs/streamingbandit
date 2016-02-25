# -*- coding: utf-8 -*-
# Persuasive 2016 Sample:
import libs.base as base
key = "weather-uid"
value = self.context["weather"] + str(self.context["userid"])
# Retrieve the average number of kilometers ran for the current weather
average = base.Mean(self.get_theta(key=key, value=value))
# Compute a streaming update:
average.update(self.reward["km"])
# Store the results
self.set_theta(average, key=key, value=value)
# (Optional):
self.log_data({"context":self.context, "average": average})
