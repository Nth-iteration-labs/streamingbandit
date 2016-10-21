import json
from requests import put,get
import numpy as np
import matplotlib.pyplot as  plt
import pandas as pd


#########################################################
# This is an agent for the parallel evaluation of multiple policies
# This behavior can be used with a simple simulation model
# But this can obviously be extended to use logged data (from e.g. a CSV file)
#
# Before going through this agent, please read the README that is provided in the utils folder
# The other agents for the other policies (LiF, BTS etc.) contain a similar structure, but will have different decision logic for the action-reward relationship.
# Those are all just illustrations of how StreamingBandit and the policies can be used.
#########################################################
BASE_URL = "http://localhost:8080" # Server location
N = 1000                           # Length of experiment

# If we do multiple iterations of parallel evaluation we want to reset the
# parameters of the experiment each iteration. This shows another cool feature
# of StreamingBandit
# Notice that each experiment should have the set_theta/get_theta keys
# set to "simulation". Or set it to blank - at least make it something consistent.
# This makes it easier to wipe the parameters of the experiment after each iteration.
theta_value = "simulation"
theta_key = "simulation" 

experiments = { 
                "1" : { 'key' : "281804239f" , 'label' : 'Random'},
                "2" : { 'key' : "29ffa7bc43" , 'label' : 'LiF'},
                "3" : { 'key' : "1e14243bd5" , 'label' : 'TBL'},
                "4" : { 'key' : "16f451a9d6" , 'label' : 'BTS'},
                "5" : { 'key' : "384ea03749" , 'label' : 'Epsilon-first'}
        }

for j in range(iterations):
    for k,v in experiments.items():
        exp_id = k
        key = v['key']
        url = "{}/{}/resetexperiment?key={}&theta_key={}&theta_value={}".format(BASE_URL, exp_id, key, theta_key, theta_value)
        result = get(url)
        print(result.text)
        if v['label'] == 'Epsilon-first':
            url = "{}/{}/resetexperiment?key={}&theta_key={}&theta_value={}".format(BASE_URL, exp_id, key, "count", "count" )
            result = get(url)
            print(result.text)

    # This is the experiment ID and key, which containts the code of the evaluation
    # policy. Please change accordingly
    exp_id = 11 
    key = "384dc6a03a"

    for i in range(N):
        # Get the action
        url = "{}/{}/getaction.json?key={}".format(BASE_URL,exp_id,key)
        result = get(url)
        jsonobj = json.loads(result.text)
        action = int(jsonobj["action"]["action"])
       
        # Make up decision logic, we will keep this fairly simple
        # The action is a number between 1 and 10
        reward = np.random.binomial(1,(1/action))

        # If you would like to save based on which interaction and iteration it is,
        # it's useful to supply the iteration and interaction number in the context
        # and change the code in StreamingBandit to log those two numbers.        
        # If this is not neeeded, you don't need to change the code, but the context
        # will be redundant.
        url = "{}/{}/setreward.json?key={}&reward={}&action={}&context={}".format(BASE_URL,exp_id,key,json.dumps({"reward":reward}),json.dumps({"action":action}),json.dumps({"iter":j,"inter":i}))
        result = get(url)
        print("Interaction {}, iteration {}".format(i,j))
        print(result.text)
