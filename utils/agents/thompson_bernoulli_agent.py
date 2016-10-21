#!/usr/bin/env python3
import json
import random as rnd
from requests import put, get
import numpy as np

#########################################################
# This is an agent for the Thompson sampling for the K-armed Bernoulli bandit
#
# Before going through this agent, please read the README that is provided in the utils folder
# The other agents for the other policies (LiF, BTS etc.) contain a similar structure, but will have different decision logic for the action-reward relationship.
# Those are all just illustrations of how StreamingBandit and the policies can be used.
#########################################################

# SETUP:
BASE_URL = "http://localhost:8080" # Server location
exp_id = 1                         # Experiment ID, change this accordingly
key = "e0bc219a3"                  # Experiment key, change this accordingly
N = 500                            # Length of experiment

for i in range(N):
    # Get the action
    url = "{}/{}/getAction.json?key={}".format(BASE_URL,exp_id,key)
    result = get(url)
    jsonobj = json.loads(result.text)
    action = int(jsonobj["action"]["Treatment"])
    print(result.text)

    # Set the decision logic
    # Since this is just testing the algorithm, there's no need for complicated stuff
    # In the standard example/defaults we have 4 arms. Let's keep it simple, and assume
    # that each arm has a Bernoulli distribution with different p' such as:
    # Arm 1 : p = 0.25
    # Arm 2 : p = 0.5
    # Arm 3 : p = 0.5
    # Arm 4 : p = 0.75
    if action == 1:
        choice = np.random.binomial(1,0.25)
    elif action == 2 or action == 3:
        choice = np.random.binomial(1,0.5)
    else: #if action == 4
        choice = np.random.binomial(1,0.75)

    # Set the reward
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,exp_id,key,json.dumps({"value":choice}),json.dumps({"Treatment":action}))
    result = get(url)
    print(result.text)


# After the experiment is done, we want to check how our Theta looks like
# Just to show some functionality of StreamingBandit
url = "{}/stats/{}/getCurrentTheta.json".format(BASE_URL,exp_id)
