# -*- coding: utf-8 -*-
import libs.thompson as thmp
propl = thmp.BBThompsonList(self.get_theta(key="treatment"), ["1","2","3","4"])
self.action["treatment"] = propl.thompson()
self.action["propensity"] = propl.propensity(self.action["treatment"], n = 1000)
