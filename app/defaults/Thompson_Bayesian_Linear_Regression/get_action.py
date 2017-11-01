key = "simulation"
value = "simulation"

default = self.get_theta(key=key, value=value)

if default == {}:
    default = {'J' : [1, 1, 1], 'P' : [[1,0,0],[0,1,0],[0,0,1]], 'err' : 1}

model = tbl.ThompsonBayesianLinear(default)

betas = model.sample()

x = - (betas[1] / (2*betas[2]))
x = np.asscalar(x)

self.action["x"] = x
