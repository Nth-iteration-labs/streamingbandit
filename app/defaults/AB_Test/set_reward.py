# -*- coding: utf-8 -*-
prop = base.Proportion(self.get_theta(key="treatment", value=self.action["treatment"]))
prop.update(self.reward["value"])
self.set_theta(prop, key="treatment", value=self.action["treatment"])
