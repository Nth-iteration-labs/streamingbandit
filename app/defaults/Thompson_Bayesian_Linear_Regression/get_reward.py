import numpy as np
mu = 0
var = 0.1
c = 5
c2 = 10
self.reward["y"] = -(self.action["x"] - c)**2 + c2 + np.random.normal(mu, var)

