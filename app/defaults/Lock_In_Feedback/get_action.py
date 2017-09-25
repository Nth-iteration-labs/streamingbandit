import libs.lif as lf
theta = self.get_theta(all_float=False)
Lif = lf.Lif(theta, x0=1.0, a=7 , t=150, gamma=.06, omega=1.0, lifversion=1)
suggestion = Lif.suggest()
self.action["x"] = suggestion["x"]
self.action["t"] = suggestion["t"]
self.set_theta(Lif)
