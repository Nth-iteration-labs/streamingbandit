import numpy as np
import matplotlib.pyplot as plt
import pickle
from pymongo import MongoClient, ASCENDING, DESCENDING
from requests import put, get
import json

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['logs']

BASE_URL = "http://localhost:8080"

theta_key = "simulation"
theta_value = "simulation"

lensim = 100
N = 10000

experiments = { 
                "5" : { 'key' : "281804239f" , 'label' : 'Random', 'color' : 'black'},
                "7" : { 'key' : "29ffa7bc43" , 'label' : 'LiF', 'color' : 'brown' },
                "8" : { 'key' : "1e14243bd5" , 'label' : 'TBL', 'color' : 'blue'},
                #"9" : { 'key' : "16f451a9d6" , 'label' : 'BTS', 'color' : 'red'},
               "10" : { 'key' : "384ea03749" , 'label' : 'Epsilon-first', 'color' : 'green'}
        }

fig = plt.figure(1)
ax = fig.add_subplot(111)

for k,v in experiments.items():
    exp_id = k
    results = mongo_db.logs.find({"type":"evaluation","experiment":exp_id}, sort=[("time", DESCENDING)])
    results.batch_size(50)

    regret = np.zeros(N+1)

    for cur in results:
        tmp_regret = pickle.loads(cur["regret"])
        regret = regret + tmp_regret

    regret = regret / lensim

    ax.plot(regret, label = v['label'], color = v['color'])

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.title('Average regret over time')
plt.xlabel('Time')
plt.ylabel('Regret')
lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

fig.savefig('regrets.eps', format='eps', bbox_extra_artists=(lgd,), bbox_inches = 'tight')
