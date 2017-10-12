import libs.base as base
import numpy as np
e = .1
meanList = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if np.random.binomial(1,e) == 1:
    self.action["treatment"] = meanList.random()
    self.action["propensity"] = 0.1*0.5
else:
    self.action["treatment"] = meanList.max()
    self.action["propensity"] = (1-e)