# This is the summary step as explained in the JSS paper
mean = base.Mean(self.get_theta(key="treatment", value=self.action["treatment"]))
mean.update(self.reward["value"])
self.set_theta(mean, key="treatment", value=self.action["treatment"])