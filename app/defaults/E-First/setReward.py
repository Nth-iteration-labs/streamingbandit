# This is the summary step as explained in the JSS paper
import libs.base as base
mean = base.Mean(self.get_theta(key="Treatment", value=self.action["Treatment"]))
mean.update(self.reward["value"])
self.set_theta(mean, key="Treatment", value=self.action["Treatment"])
