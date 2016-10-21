#!/usr/bin/env python3
import json
import random as rnd
from requests import put, get
import numpy as np

#########################################################
# This is an agent for the application in field experiments
#
# Before going through this agent, please read the README that is provided in the utils folder
# The other agents for the other policies (LiF, BTS etc.) contain a similar structure, but will have different decision logic for the action-reward relationship.
# Those are all just illustrations of how StreamingBandit and the policies can be used.
#########################################################

# SETUP:
BASE_URL = "http://localhost:8080" # Server location
exp_id = 1                         # Experiment ID, change this accordingly
key = "e0bc219a3"                  # Experiment key, change this accordingly
N = 1200                           # Length of experiment

for i in range(N):
    # Determine maxpercentage
    maxpercentage = 10

    # Get the action
    url = "{}/{}/getAction.json?key={}&context={}".format(BASE_URL,exp_id,key,json.dumps({"maxpercentage":maxpercentage})
    result = get(url)
    jsonobj = json.loads(result.text)
    split = int(jsonobj["action"]["split"])
    y = int(jsonobj["action"]["y"])
    print(result.text)

    # Set the decision logic
    # Since this is just testing the algorithm, there's no need for complicated stuff
    # The reward is a Gaussian with the percentage as the mean
    reward = np.random.normal(y, 3)

    # Set the reward
    url = "{}/{}/setReward.json?key={}&reward={}&action={}&contex={}".format(BASE_URL,exp_id,key,json.dumps({"revenue":choice}),json.dumps({"split":split,"y":y}),json.dumps({"maxpercentage":maxpercentage}))
    result = get(url)
    print(result.text)


# After the experiment is done, we want to check how our Theta looks like
# Just to show some functionality of StreamingBandit
url = "{}/stats/{}/getCurrentTheta.json".format(BASE_URL,exp_id)
