# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
propl = base.List(self.get_theta(key="treatment"), base.Proportion, ["1", "2"])
if propl.count() > 100:
    self.action["treatment"] = propl.max()
    self.action["propensity"] = 1
else:
    self.action["treatment"] = propl.random()
    self.action["propensity"] = 0.5
