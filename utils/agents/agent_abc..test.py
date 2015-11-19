#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random as rnd
from requests import put, get
import numpy as np


# SETUP:
BASE_URL = "http://localhost:8080"      # Server location
id = 1                                  # Experiment ID of the ABC... test
key= "e0bc219a3"                        # Key
k = 10                                  # Number of options
N = 999                                 # Length of the test
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
    action = jsonobj["action"]["version"]   
    print(result.text)
    
    # Set reward
    choice = 0 if action == "A" else 1
    click = np.random.binomial(1, p[choice-1])
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,id,key,json.dumps({"click":click}),json.dumps({"version":action}))   
    result = get(url)
    print(result.text)
    
    # log:
    reward = reward + click
    rewards = np.append(rewards, click)
    choices = np.append(choices, action) 

if N < printtill:
    print(choices)
    print(rewards)

print("Total reward is: {}".format(reward))
