# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.base as base
propl = base.List(self.get_theta(all_action=True), Proportion, ["A", "B"])
if propl.count() > 1000:
    self.action["version"] = propl.max()
else
    self.action["version"] = base.random(["A","B"])
