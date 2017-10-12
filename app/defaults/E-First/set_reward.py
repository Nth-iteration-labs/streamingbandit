# This is the summary step as explained in the JSS paper
import libs.base as base

n = 100
meanList = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if meanList.count() < n:
  mean = base.Mean(self.get_theta(key="treatment", value=self.action["treatment"])) 
  mean.update(self.reward["value"])
  self.set_theta(mean, key="treatment", value=self.action["treatment"])