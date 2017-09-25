# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.base as base
propl = base.List(self.get_theta(key="Treatment"), base.Proportion, ["1", "2", "3", "4"])
if propl.count() > 1000:
    self.action["Treatment"] = propl.max()
else:
    self.action["Treatment"] = propl.random()
