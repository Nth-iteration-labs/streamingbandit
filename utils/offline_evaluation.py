import json
from requests import put,get
import numpy as np
import matplotlib.pyplot as  plt
from pymongo import MongoClient, ASCENDING, DESCENDING

BASE_URL = "http://localhost:8080"
exp_id = 11
key = "384dc6a03a"

N = 10000

np.random.seed(10)

x = np.random.uniform(0,10,N)
c = 5
c2 = 10
mu = 0
var = 0.1

y = -(x - c)**2 + c2 + np.random.normal(mu,var,N)

for i in range(N):
    #url = "{}/{}/getaction.json?key={}".format(BASE_URL,exp_id,key)
    #result = get(url)
    #jsonobj = json.loads(result.text)
    
    y_send = y[i]
    x_send = x[i]
    url = "{}/{}/setreward.json?key={}&reward={}&action={}".format(BASE_URL,exp_id,key,json.dumps({"y":y_send}),json.dumps({"x":x_send}))
    result = get(url)
    print(result.text)


mongo_client = MongoClient('localhost',27017)
mongo_db = mongo_client['logs']

exp_id_off = 6

results = mongo_db.logs.find({"type":"offline_evaluation","experiment":exp_id_off},sort=[("time",DESCENDING)])

suggestion = np.array([0])
#action = np.array([0])
regret = np.array([0])

for row in results:
    print(row["suggestion"])
    suggestion = np.append(suggestion, row["suggestion"])
#    action = np.append(action, row["action"])
    regret = np.append(regret, (regret[-1] + (10 - row["reward"])))

#threshold = action - suggestion

#plt.plot(threshold)
plt.plot(regret)
plt.ylabel("Regret")
plt.xlabel("Time")
plt.show()

plt.plot(suggestion)
plt.title("Suggestions")
plt.xlabel("Time")
plt.ylabel("x")
plt.show()
