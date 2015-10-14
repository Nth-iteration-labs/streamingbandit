# -*- coding: utf-8 -*-
import json
import random as rnd
from requests import put, get
import numpy as np


# SETUP:
BASE_URL = "http://localhost:8080"      # Server location
id = 1                                  # Experiment ID of the persuasive sample experiment
key= "1affa27676"                       # Key
N=100                                    # Number of calls

userid = 12                             # Id of user
weather = ["sunny", "rainy"]            # Possible values for weather



for i in range(N):
    
    # Get the action (and print the call and the result):   
    currentweather = rnd.choice(weather)
    url = "{}/{}/getAction.json?key={}&context={}".format(BASE_URL,id,key,json.dumps({"weather":currentweather,"userid":userid}))    
    print(url)    
    result = get(url)
    print(result.text)
    
    jsonobj = json.loads(result.text)
    action = int(jsonobj["action"]["distance"])   
    
    # Set reward
    actualkm = 10    # This user overshoots his goal all the time
    url = "{}/{}/setReward.json?key={}&reward={}&context={}".format(BASE_URL,id,key,json.dumps({"km":actualkm}),json.dumps({"weather":currentweather,"userid":userid}))   
    print(url)    
    result = get(url)
    print(result.text)
    
