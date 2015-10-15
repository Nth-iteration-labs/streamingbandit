# -*- coding: utf-8 -*-
# Persuasive 2016 Sample:
import libs.tools as tls

# http://localhost:8080/1/setReward.json?key=1affa27676&reward=%7B%22km%22%3A8%7D&action=%7B%22choice%22%3A1%7D

# Retrieve the average number of kilometers ran for the current weather
average = tls.mean(self.get_theta(context=context))

# Compute a streaming update:
average = tls.update(tls.mean, average, self.reward["km"])

# Store the results
self.set_theta(average, context=context)

# (Optional):
self.log_data({"context":self.context, "average": average})