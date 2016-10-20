# -*- coding: utf-8 -*-
import libs.lif as lf

key = "question"
value = self.context['question']

theta = self.get_theta(all_float=False, key=key, value=value)
Lif = lf.Lif(theta, x0=1.0, A=7 , T=150, gamma=.06, omega=1.0, lifversion=1)
suggestion = Lif.suggest()

self.action["x"] = suggestion["x"]
self.action["t"] = suggestion["t"]

self.set_theta(Lif, key=key, value=value)

# Example of logging the data
import time

self.log_data({
    "type" : "getadvice",
    "t" : suggestion["t"],
    "x" : suggestion["x"],
    "time" : int(time.time()),
    "context" : self.context,
    "q" : self.context['question']
})
