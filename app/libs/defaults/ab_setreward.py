# -*- coding: utf-8 -*-
# Imort tools (for updates, etc.) and time (for logging):
import libs.base as base
prop = base.Proportion(self.get_theta(action=self.action))
prop.update(self.reward["click"])
self.set_theta(prop, action=self.action)
