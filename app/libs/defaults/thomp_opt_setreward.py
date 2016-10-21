import libs.base as base
var = base.Variance(self.get_theta(key="Treatment"))
var.update(self.reward["value"])
self.set_theta(var, key="Treatment", value=self.action["Treatment"])
