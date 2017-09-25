# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.base as base
propl = base.List(self.get_theta(key="Treatment"), base.Proportion, ["1", "2"])
if propl.count() > 100:
    self.action["Treatment"] = propl.max()
    self.action["Propensity"] = 1
else:
    self.action["Treatment"] = propl.random()
    self.action["Propensity"] = 0.5
