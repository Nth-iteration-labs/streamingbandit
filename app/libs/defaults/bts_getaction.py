# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as lm


BTS = bts.model(self.get_theta(), lm.Model, m = 100, default_parameters = {'b' : [1,1,1], 'A' : [[1,0,0],[0,1,0],[0,0,1]], 'n' : 0})

# Return one of the m samples
model = lm.LM(default = BTS.sample()
betas = model.get_coefs()

if betas[2,0] == 0
    x = 0
else:
    x = - (betas[1,0] / 2*betas[2,0])
    x = np.asscalar(x)

self.action["Price"] = x
