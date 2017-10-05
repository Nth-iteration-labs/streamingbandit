# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as lm

# Extract values:
device = self.context["device"]
price = self.action["price"]

# Create feature vector and response:
X = [1, price, price**2, device, device*price, device*price**2]
y = self.reward["revenue"]

# Update the lm.model, specifically the default, 
# the number of replicates and the default parameters
BTS = bts.BTS(self.get_theta(), lm.LM, m = 100, default_params =  \
                {'b' : [0,0,0,0,0,0], 'A' : [[1,0,0,0,0,0],[0,1,0,0,0,0], \
                                             [0,0,1,0,0,0],[0,0,0,1,0,0], \
                                             [0,0,0,0,1,0],[0,0,0,0,0,1]], 'n' : 0})

BTS.update(y, X)

self.set_theta(BTS)
