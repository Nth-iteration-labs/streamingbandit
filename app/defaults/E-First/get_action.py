import libs.base as base

n = 100
meanList = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if meanList.count() >= n:
    self.action["treatment"] = meanList.max()
    self.action["propensity"] = 1
else:
    self.action["treatment"] = meanList.random()
    self.action["propensity"] = 0.5