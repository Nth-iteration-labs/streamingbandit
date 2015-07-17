# -*- coding: utf-8 -*-

import redis
import yaml
import json

f = open("../scripts/config.cfg","r")
settings = yaml.load(f)
r_server = redis.Redis(settings["redis_ip"], settings["redis_port"])

exp_id = 13


### Insett the code for action
with open ("AB_getaction.py", "r") as myfile:
    codestr=myfile.read()
r_server.set("exp:%s:getAction" % exp_id, codestr)

### Insert the code for rewards
with open ("AB_setreward.py", "r") as myfile:
    codestr=myfile.read()
r_server.set("exp:%s:setReward" % exp_id, codestr)

### Initialize the theta: (at least the grant one)
theta = {}
theta["n"] = 0      # starting number of observations
theta["k"] = 4      # number of versions
r_server.hmset("exp:%s:theta" % exp_id, theta)