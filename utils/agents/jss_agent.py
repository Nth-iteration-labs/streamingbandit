#!/usr/bin/env python3
import json
import random as rnd
from requests import put, get
import numpy as np

#########################################################
# This is an agent for the JSS running example of the Introduction section
# Depending on the experiments used, this agent can also be used for the nested experiments
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
    # Get the action
    url = "{}/{}/getAction.json?key={}".format(BASE_URL,exp_id,key)
    result = get(url)
    jsonobj = json.loads(result.text)
    action = jsonobj["action"]["Treatment"]
    # If this is a nested experiment, this is the Experiment type
    #experiment = int(jsonobj["action"]["Experiment"])
    print(result.text)

    # Set the decision logic
    # Since this is just testing the algorithm, there's no need for complicated stuff
    # Let's assume that treatment T has a probability of giving a reward = 1 of 0.75
    # And that treatment C has a probability of giving reward = 1 of 0.25
    # After N = 1000 (if set like such in the code in the software)
    # we hope to see treatment T to be selected at all times
    choice = np.random.binomial(1,0.75) if action == "T" else np.random.binomial(1,0.25)

    # Set the reward
    url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,exp_id,key,json.dumps({"value":choice}),json.dumps({"Treatment":action}))
    # If there's nested experiment, this is the url
    #url = "{}/{}/setReward.json?key={}&reward={}&action={}".format(BASE_URL,exp_id,key,json.dumps({"value":choice}),json.dumps({"action":action,"Experiment":experiment}))
    result = get(url)
    print(result.text)


# After the experiment is done, we want to check how our Theta looks like
# Just to show some functionality of StreamingBandit
url = "{}/stats/{}/getCurrentTheta.json".format(BASE_URL,exp_id)
