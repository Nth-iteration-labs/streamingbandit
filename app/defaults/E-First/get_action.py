import libs.base as base
meanList = base.List(self.get_theta(key="Treatment"), base.Mean, ["C", "T"])
if meanList.count() > 1000:
    self.action["Treatment"] = meanList.max()
    self.action["Propensity"] = 1
else:
    self.action["Treatment"] = meanList.random()
    self.action["Propensity"] = 0.5
