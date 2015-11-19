# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.base as base
import libs.lm as lm
key = "weather-uid"
value = self.context["weather"] + str(self.context["userid"])
model = lm.Model(self.get_theta(key=key, value=value))
mean = base.Mean(self.get_theta(name="mean", key=key, value=value))
d = mean - self.action["km"]
model.update(self.reward["km"], [d, d^2])
mean.update(self.reward["km"])
self.set_theta(model, key=key, value=value)
self.set_theta(mean, name="mean", key=key, value=value)
