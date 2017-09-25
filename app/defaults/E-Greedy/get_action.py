import libs.base as base
import numpy as np
e = .1
meanList = base.List(self.get_theta(key="Treatment"), base.Mean, ["C", "T"])
if np.random.binomial(1,e) == 1:
    self.action["Treatment"] = meanList.random()
    self.action["Propensity"] = 0.1*0.5
else:
    self.action["Treatment"] = meanList.max()
    self.action["Propensity"] = (1-e)
