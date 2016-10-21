# -*- coding: utf-8 -*-
import libs.lif as lf

key = "question"
value = self.context['question']

theta = self.get_theta(all_float=False, key=key, value=value)
Lif = lf.Lif(theta, x0=1.0, A=7 , T=150, gamma=.06, omega=1.0, lifversion=1)
Lif.update(self.action["t"],self.action["x"], self.reward)
self.set_theta(Lif, key=key, value=value)

# An example of how to log the data
import time

self.log_data({
    "type" : "setreward",
    "t" : self.action["t"],
    "x" : self.action["x"],
    "y" : self.reward,
    "x0" : theta['x0'],
    "time" : int(time.time()),
    "context" : self.context,
    "q" : self.context['question']
})
