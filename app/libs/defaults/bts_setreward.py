# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as ls

# Extract values:
customer = self.context["Type"]
price = self.action["Price"]

# Create feature vector and response:
X = [1, price, price**2, customer, customer*price, customer*price**2]
y = self.reward["Revenue"]

# Update the lm.model, specifically the default, and
# specify the number of replicates
BTS = bts.model(self.get_theta(), lm.Model, m = 100, default_parameters = {'b' : [1,1,1], 'A' : [[1,0,0],[0,1,0],[0,0,1]], 'n' : 0})

BTS.update(y, X)

self.set_theta(BTS)
