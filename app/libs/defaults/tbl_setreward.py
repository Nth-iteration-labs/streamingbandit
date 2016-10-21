import libs.thompson_bayesian_linear as tbl
import numpy as np

key = "simulation"
value = "simulation"

x = self.action["x"]
y = self.reward["y"]

default = self.get_theta(key=key, value=value)

if default == {}:
    default = {'J' : [1,1,1], 'P' : [[1,0,0],[0,1,0],[0,0,1]], 'cov' : 1}

model = tbl.ThompsonBayesianLinear(default)

model.update(y = y, x = [1, x, x**2])
self.set_theta(model, key=key, value=value)
