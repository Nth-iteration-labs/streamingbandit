#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random as rnd
from requests import put, get
import numpy as np
import matplotlib.pyplot as plt

BASE_URL = "http://localhost:8080"
id = 5
key = "281804239f"
#id = 6
#key = "121accf5ca"
N = 1000

# Linear model settings
c = 5
c2 = 5
mu = 0
var = .1
reward = np.array([0])
reward_over_time = np.array([])
regret = np.array([0])

for i in range(N):

    # Get the action
    url = "{}/{}/getAction.json?key={}".format(BASE_URL,id,key)
    result = get(url)
    jsonobj = json.loads(result.text)
    action = jsonobj["action"]["size"]
    #print(result.text)

    # Set reward
    y = -(action - c)**2 + c2 + np.random.normal(mu, var)
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,id,key,json.dumps({"y":y}),json.dumps({"size":action}))
    result = get(url)
    #print(result.text)

    tmp_reward = reward[-1] + y
    reward = np.append(reward, tmp_reward)
    tmp_rot = tmp_reward / i
    reward_over_time = np.append(reward_over_time, tmp_rot)
    regret = np.append(regret, (regret[-1] + (5 - tmp_reward)))

    print("Regret is: {}".format(regret[-1]))

plt.plot(regret)
