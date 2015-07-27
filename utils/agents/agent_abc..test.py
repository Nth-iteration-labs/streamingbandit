# -*- coding: utf-8 -*-
import json
import random as rnd
from requests import put, get
import numpy as np


# SETUP:
BASE_URL = "http://localhost:8080"
id = 1          # Experiment ID of the ABC... test
key= 13          # Key
k = 3           # Number of options
N = 400         # Length of the test
best = .5       # Probablity of success best option
delta = .2      # Probablity of success other options



# Store of data:
printtill = 450
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
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,id,key,click,json.dumps({"choice":action}))  
    result = get(url)
    
    # log:
    reward = reward + click
    rewards = np.append(rewards, click)
    choices = np.append(choices, action) 

if N < printtill:
    print(choices)
    print(rewards)

print("Total reward is: {}".format(reward))