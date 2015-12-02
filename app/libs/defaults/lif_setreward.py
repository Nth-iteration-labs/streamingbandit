# -*- coding: utf-8 -*-
import libs.lif as lf

theta = self.get_theta(all_float=False,context={'question':self.context['question']}).get("theta",None)
Lif = lf.Lif(theta, x0=1.0, A=1.4 , T=100, gamma=.004, omega=.8, lifversion=2)
Lif.update(self.action["t"],self.action["x"], self.reward)
self.set_theta({"theta": Lif.get_theta()},context={'question':self.context['question']})

import time
self.log_data({
    "type" : "setreward",
    "t" : self.action["t"],
    "x" : self.action["x"],
    "y" : self.reward,
    "x0" : Lif.get_x0(),
    "time" : int(time.time()),
    "context" : self.context,
    "q" : self.context['question']
})

# Example URL
# /2/setReward.json?key=24ff7bb26&action={"x":7.8,"t":2.0}&reward=6.8&context={"question":2}