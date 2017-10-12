import numpy
global numpy
device = self.context["device"]
price = self.action["price"]
logistic = lambda x: 1 / (1 + numpy.exp(-x))
buy = numpy.random.binomial(1, logistic(0.1 * ((price + (device * 4))-10)**2))
self.reward["revenue"] = buy * price
