#!/usr/bin/env python3
import json
import random as rnd
from requests import put, get
import numpy as np

#########################################################
# This is an agent for Thompson sampling for optimal design
#
# Before going through this agent, please read the README that is provided in the utils folder
# The other agents for the other policies (LiF, BTS etc.) contain a similar structure, but will have different decision logic for the action-reward relationship.
# Those are all just illustrations of how StreamingBandit and the policies can be used.
#########################################################

# SETUP:
BASE_URL = "http://localhost:8080" # Server location
exp_id = 1                         # Experiment ID, change this accordingly
key = "e0bc219a3"                  # Experiment key, change this accordingly
N = 100                            # Length of experiment

for i in range(N):
    # Get the action
    url = "{}/{}/getAction.json?key={}".format(BASE_URL,exp_id,key)
    result = get(url)
    jsonobj = json.loads(result.text)
    action = int(jsonobj["action"]["Treatment"])
    print(result.text)

    # Set the decision logic
    # Since this is just testing the algorithm, there's no need for complicated stuff
    # Let's assume that treatment 1 has a probability of giving a reward = 1 of 0.75
    # And that treatment 2 has a probability of giving reward = 1 of 0.25
    choice = np.random.binomial(1,0.75) if action == 1 else np.random.binomial(1,0.25)

    # Set the reward
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,exp_id,key,json.dumps({"value":choice}),json.dumps({"Treatment":action}))
    result = get(url)
    print(result.text)


# After the experiment is done, we want to check how our Theta looks like
# Just to show some functionality of StreamingBandit
url = "{}/stats/{}/getCurrentTheta.json".format(BASE_URL,exp_id)
