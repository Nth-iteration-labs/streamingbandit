import libs.lif as lf
theta = self.get_theta(all_float=False,key="treatment", value=1)
Lif = lf.Lif(theta, x0=4.0, a=3 , t=100, gamma=.06, omega=1.0, lifversion=1)
suggestion = Lif.suggest()
self.action["x"] = suggestion["x"]
self.action["t"] = suggestion["t"]
self.set_theta(Lif,key="treatment", value=1)
