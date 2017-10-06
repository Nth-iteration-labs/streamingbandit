import libs.lif as lf
theta = self.get_theta(all_float=False,key="treatment", value=1)
Lif = lf.Lif(theta, x0=4.0, a=3 , t=100, gamma=.06, omega=1.0, lifversion=1)
Lif.update(self.action["t"], self.action["x"], self.reward["r"])
self.set_theta(Lif,key="treatment", value=1)
