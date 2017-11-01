theta = self.get_theta(all_float=False)
Lif = lif.LiF(theta, x0=3.0, a=.5, t=100, gamma=.02, omega=1.0, lifversion=1)
Lif.update(self.action["t"], self.action["x"], self.reward["r"], self.action["x0"])
self.set_theta(Lif)