n = 100
mean_list = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if mean_list.count() >= n:
    self.action["treatment"] = mean_list.max()
    self.action["propensity"] = 1
else:
    self.action["treatment"] = mean_list.random()
    self.action["propensity"] = 0.5