# Instantiate BTS with m=100 samples:
BTS = bts.BTS(self.get_theta(), lm.LM, m = 100, default_params = \
       {'b': np.zeros(6).tolist(), 'A' : np.identity(6).tolist(), 'n' : 0})

# Return one of the m samples:
model = lm.LM(default = BTS.sample())

# Retrieve its coefficients:
betas = model.get_coefs()

# Create dummy for customer
if(self.context["customer"] == "returning"):
    customer = 1
else:
    customer = 0

# Maximize the function
if (betas[2] + betas[5] * customer) == 0:
    x = 0
else:
    x = - ((betas[1] + betas[4] * customer) / 2*(betas[2] + betas[5] * customer))
    x = np.asscalar(x)

# Return the price
self.action["price"] = x