e = .1
mean_list = base.List(self.get_theta(key="treatment"), base.Mean, ["control", "treatment"])
if np.random.binomial(1,e) == 1:
    self.action["treatment"] = mean_list.random()
    self.action["propensity"] = 0.1*0.5
else:
    self.action["treatment"] = mean_list.max()
    self.action["propensity"] = (1-e)