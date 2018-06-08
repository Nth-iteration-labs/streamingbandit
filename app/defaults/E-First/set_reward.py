# This is the summary step as explained in the JSS paper
n = 100
mean_list = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if mean_list.count() < n: # Leave this out to get a less greedy version of E-First
  mean = base.Mean(self.get_theta(key="treatment", value=self.action["treatment"])) 
  mean.update(self.reward["value"])
  self.set_theta(mean, key="treatment", value=self.action["treatment"])