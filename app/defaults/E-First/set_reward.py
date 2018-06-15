# This is the summary step as explained in the JSS paper
n = 100
# Leave out the following two lines to keep updating the means after n interactions
mean_list = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if mean_list.count() < n:
  mean = base.Mean(self.get_theta(key="treatment", value=self.action["treatment"])) 
  mean.update(self.reward["value"])
  self.set_theta(mean, key="treatment", value=self.action["treatment"])