# -*- coding: utf-8 -*-
import libs.thompson as thmp
propl = thmp.BBThompsonList(self.get_theta(key="Treatment"), ["1","2","3","4"])
self.action["Treatment"] = propl.thompson()
self.action["Propensity"] = propl.propensity(self.action["Treatment"], n = 1000)
