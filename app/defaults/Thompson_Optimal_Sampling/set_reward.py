var = base.Variance(self.get_theta(key="treatment", value=self.action["treatment"]))
var.update(self.reward["value"])
self.set_theta(var, key="treatment", value=self.action["treatment"])