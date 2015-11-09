# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.base as base
import libs.lm as lm
model = lm.Model(self.get_theta(context=self.context))
mean = base.Mean(self.get_theta(name="mean", context=self.context))
d = mean - self.action["km"]
model.update(self.reward["km"], [1, d, d^2])
mean.update(self.reward["km"])
self.set_theta(model)
self.set_theta(mean, name="mean")
