# Get parameters
# Create dummy for customer
if(self.context["customer"] == "returning"):
    customer = 1
else:
    customer = 0
price = self.action["price"]

# Create logistic function
logistic = lambda x: 1 / (1 + numpy.exp(-x))

# Compute purchase yes / no
buy = numpy.random.binomial(1, logistic(0.1 * ((price + (customer * 4))-10)**2))

# Compute the reward
self.reward["revenue"] = buy * price