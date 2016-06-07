# -*- coding: utf-8 -*-
import libs.bts as bts
import libs.lm as lm
import scipy.optimize

# Extract values
customer = self.context["Type"]

BTS = bts.model(get_theta(), lm.Model, m = 100)

# Return one of the m samples
betas = BTS.sample()

def model(x, betas, customer):
    X = [1, x, x**2, customer, customer*x, customer*x**2]
    return -1*x*betas

ymax = minimize(model, x0=10, bound[0,200])

self.action["price"] = ymax
