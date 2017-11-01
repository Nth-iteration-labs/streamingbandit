# Extract values:
# Create dummy for customer
if(self.context["customer"] == "returning"):
    customer = 1
else:
    customer = 0
price = self.action["price"]

# Create feature vector and response:
X = [1, price, price**2, customer, customer*price, customer*price**2]
y = self.reward["revenue"]

# Instantiate the m=100 lm.models
BTS = bts.BTS(self.get_theta(), lm.LM, m = 100, default_params = \
       {'b': np.zeros(6).tolist(), 'A' : np.identity(6).tolist(), 'n' : 0})

# Update the model parameters using the new observation
BTS.update(y, X)

# Store the updated values
self.set_theta(BTS)