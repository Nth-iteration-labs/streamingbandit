import json
from requests import put,get
import numpy as np
import matplotlib.pyplot as  plt

BASE_URL = "http://localhost:8080"


theta_key = "simulation"
theta_value = "simulation"

N = 10000

np.random.seed(10)

x = np.random.uniform(0,10,N)
c = 5
c2 = 10
mu = 0
var = 1

iterations = 100

y = -(x - c)**2 + c2 + np.random.normal(mu,var,N)

experiments = { 
                "5" : { 'key' : "281804239f" , 'label' : 'Random'},
                "7" : { 'key' : "29ffa7bc43" , 'label' : 'LiF'},
                "8" : { 'key' : "1e14243bd5" , 'label' : 'TBL'},
                "9" : { 'key' : "16f451a9d6" , 'label' : 'BTS'},
               "10" : { 'key' : "384ea03749" , 'label' : 'Epsilon-first'}
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

    exp_id = 11
    key = "384dc6a03a"

    for i in range(N):
        #url = "{}/{}/getaction.json?key={}".format(BASE_URL,exp_id,key)
        #result = get(url)
        #jsonobj = json.loads(result.text)
        
        y_send = y[i]
        x_send = x[i]
        url = "{}/{}/setreward.json?key={}&reward={}&action={}&context={}".format(BASE_URL,exp_id,key,json.dumps({"y":y_send}),json.dumps({"x":x_send}),json.dumps({"iter":j,"var":var,"inter":i}))
        result = get(url)
        print("Interaction {}, iteration {}".format(i,j))
        print(result.text)
