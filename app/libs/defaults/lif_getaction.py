# -*- coding: utf-8 -*-
import libs.lif as lf

key = "question"
value = self.context['question']
theta = self.get_theta(all_float=False,name="theta", key=key, value=value)
Lif = lf.Lif(theta, x0=1.0, A=1.4 , T=100, gamma=.004, omega=.8, lifversion=2)
suggestion = Lif.suggest()
self.action["x"] = suggestion["x"]
self.action["t"] = suggestion["t"]
self.set_theta(Lif.get_dict(), name="theta", key=key, value=value)

import time

self.log_data({
    "type" : "getadvice",
    "t" : suggestion["t"],
    "x" : suggestion["x"],
    "time" : int(time.time()),
    "context" : self.context,
    "q" : self.context['question']
})

# Example URL
# /2/getAction.json?key=24ff7bb26&context={"question":2}