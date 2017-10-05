# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as lm
import numpy as np

device = self.context["device"] 

BTS = bts.BTS(self.get_theta(), lm.LM, m = 100, default_params = \
        {'b': [0,0,0,0,0,0], 'A' : [[1,0,0,0,0,0],[0,1,0,0,0,0], \
                                    [0,0,1,0,0,0],[0,0,0,1,0,0], \
                                    [0,0,0,0,1,0],[0,0,0,0,0,1]], 'n' : 0})

# Return one of the m samples
model = lm.LM(default = BTS.sample())
betas = model.get_coefs()

if (betas[2,0] + betas[5,0] * device) == 0:
    x = 0
else:
    x = - ((betas[1,0] + betas[4,0] * device) / 2*(betas[2,0] + betas[5,0] * device))
    x = np.asscalar(x)

self.action["price"] = x
