#!/usr/bin/env python3
import json
import random as rnd
from requests import put, get
import numpy as np

#########################################################
# This is an agent for Bootstrapped Thompson Sampling
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
    # Random customer type:
    customer = np.random.binomial(1,0.5)

    context["Type"] = customer

    # Get the action
    url = "{}/{}/getAction.json?key={}&context={}".format(BASE_URL,exp_id,key,json.dumps(context))
    result = get(url)
    jsonobj = json.loads(result.text)
    action = int(jsonobj["action"]["Price"])
    print(result.text)

    # Set the decision logic
    # Since this is just testing the algorithm, there's no need for complicated stuff
    # Here we will just make a model based on the assumption in the sample codes
    # that is provided in the defaults section + some noise
    y = 5 + 3*price + 2*price**2 + 5*customer + 1.5*customer*price + -.25*customer*price**2 + np.random.normal(0,.1)

    # Set the reward
    url = "{}/{}/setReward.json?key={}&reward={}&action={}&context={}".format(BASE_URL,exp_id,key,json.dumps({"Revenue":y}),json.dumps({"Price":action}),json.dumps(context))
    result = get(url)
    print(result.text)


# After the experiment is done, we want to check how our Theta looks like
# Just to show some functionality of StreamingBandit
# In case of BTS this will be a huge JSON object, since it contains 100 samples!
url = "{}/stats/{}/getCurrentTheta.json".format(BASE_URL,exp_id)
