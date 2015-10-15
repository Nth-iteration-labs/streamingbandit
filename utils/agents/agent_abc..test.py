# -*- coding: utf-8 -*-
import json
import random as rnd
from requests import put, get
import numpy as np


# SETUP:
BASE_URL = "http://localhost:8080"      # Server location
id = 2                                  # Experiment ID of the ABC... test
key= "10112f20bb"                       # Key
k = 10                                  # Number of options
N = 999                                # Length of the test
best = .5                               # Probablity of success best option
delta = .2                              # Probablity of success other options = best-delta



# Store of data:
printtill = 1000
p = np.append(best, np.repeat(best-delta, k-1))
reward = 0
rewards = np.array([])
choices = np.array([])

for i in range(N):
    
    # Get the action:
    url = "{}/{}/getAction.json?key={}".format(BASE_URL,id,key)
    result = get(url)
    jsonobj = json.loads(result.text)
    action = int(jsonobj["action"]["choice"])   
    
    # Set reward
    click = np.random.binomial(1, p[action-1])
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,id,key,json.dumps({"click":click}),json.dumps({"choice":action}))   
    result = get(url)
    
    # log:
    reward = reward + click
    rewards = np.append(rewards, click)
    choices = np.append(choices, action) 

if N < printtill:
    print(choices)
    print(rewards)

print("Total reward is: {}".format(reward))