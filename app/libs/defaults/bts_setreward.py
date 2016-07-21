# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as ls

# Example for JSS paper
# Extract values:
customer = self.context["Type"]
price = self.action["Price"]

# Create feature vector and response:
X = [1, price, price**2, customer, customer*price, customer*price**2]
y = self.reward["Revenue"]

# Update the lm.model, specifically the default, and
# specify the number of replicates
BTS = bts.model(get_theta(), lm.Model, m = 100)

BTS.update(y, X)

self.set_theta(BTS)
