import libs.base as base
meanList = base.List(self.get_theta(key="treatment"), base.Mean, ["C", "T"])
if meanList.count() > 1000:
    self.action["treatment"] = meanList.max()
    self.action["propensity"] = 1
else:
    self.action["treatment"] = meanList.random()
    self.action["propensity"] = 0.5
