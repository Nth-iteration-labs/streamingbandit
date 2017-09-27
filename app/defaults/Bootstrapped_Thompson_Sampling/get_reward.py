import numpy as np
device = self.context["Device"]
price = self.action["Price"]
logit = lambda x: np.log(x) - np.log(1 - x)
buy = np.random.binomial(1, logit(0.1 * ((price + (device * 4))-10)^2))
self.reward["Revenue"] = buy * price
