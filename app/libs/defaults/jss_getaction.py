# This is the decision step as explained in the JSS paper
n = 1000
import libs.base as base
meanList = base.List(self.get_theta(key="Treatment"), base.Mean, ["C", "T"])
if meanList.count() > n:
    self.action["Treatment"] = meanList.max()
else:
    self.action["Treatment"] = meanList.random()
