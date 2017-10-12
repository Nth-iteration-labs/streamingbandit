# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as lm
import numpy as np

# Extract values:
device = self.context["device"]
price = self.action["price"]

# Create feature vector and response:
X = [1, price, price**2, device, device*price, device*price**2]
y = self.reward["revenue"]

# Update the lm.model, specifically the default, 
# the number of replicates and the default parameters
BTS = bts.BTS(self.get_theta(), lm.LM, m = 100, default_params = \
       {'b': np.zeros(6).tolist(), 'A' : np.identity(6).tolist(), 'n' : 0})

BTS.update(y, X)

self.set_theta(BTS)