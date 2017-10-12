import libs.lif as lf
theta = self.get_theta(all_float=False, key="treatment")
Lif = lf.Lif(theta, x0=3.0, a=.5, t=20, gamma=.2, omega=1.0, lifversion=1)
suggestion = Lif.suggest()
self.action["x"] = suggestion["x"]
self.action["t"] = suggestion["t"]
self.set_theta(Lif, key="treatment")