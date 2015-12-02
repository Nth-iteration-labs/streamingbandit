# -*- coding: utf-8 -*-
import libs.lif as lf

key = "question"
value = self.context['question']

theta = self.get_theta(all_float=False, key=key, value=value)
Lif = lf.Lif(theta, x0=1.0, A=1.4 , T=100, gamma=.004, omega=.8, lifversion=2)
Lif.update(self.action["t"],self.action["x"], self.reward)
self.set_theta(Lif, key=key, value=value)

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

# Example URL
# /2/setReward.json?key=24ff7bb26&action={"x":7.8,"t":2.0}&reward=6.8&context={"question":2}