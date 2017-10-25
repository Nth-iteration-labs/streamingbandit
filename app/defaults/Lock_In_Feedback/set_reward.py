theta = self.get_theta(all_float=False)
Lif = lif.Lif(theta, x0=3.0, a=.5, t=100, gamma=.2, omega=1.0, lifversion=1)
Lif.update(self.action["t"], self.action["x"], self.reward["r"])
self.set_theta(Lif)