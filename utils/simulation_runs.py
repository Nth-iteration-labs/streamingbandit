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
N = 1001

experiments = { "6" : { 'key' : "121accf5ca", 'label' : 'Linear' },
                "5" : { 'key' : "281804239f" , 'label' : 'Random'},
                "7" : { 'key' : "29ffa7bc43" , 'label' : 'LiF'},
                "8" : { 'key' : "1e14243bd5" , 'label' : 'TBL'},
                "9" : { 'key' : "16f451a9d6" , 'label' : 'BTS'},
               "10" : { 'key' : "384ea03749" , 'label' : 'Epsilon-first'}
        }

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

for k,v in experiments.items():
    exp_id = k
    key = v['key']
    for i in range(0,lensim):
        print("Simulation {} for experiment {}".format(i, v['label']))
        url = "{}/eval/{}/simulate?key={}".format(BASE_URL,exp_id,key)
        result = get(url)
        print(result.text)
        url = "{}/{}/resetexperiment?key={}&theta_key={}&theta_value={}".format(BASE_URL, exp_id, key, theta_key, theta_value)
        result = get(url)
        print(result.text)
        if v['label'] == 'Epsilon-first':
            url = "{}/{}/resetexperiment?key={}&theta_key={}&theta_value={}".format(BASE_URL, exp_id, key, "count", "count" )
            result = get(url)
            print(result.text)

fig = plt.figure(1)
ax = fig.add_subplot(111)

for k,v in experiments.items():
    exp_id = k
    results = mongo_db.logs.find({"type":"evaluation","experiment":exp_id}, sort=[("time", DESCENDING)])

    regret = np.zeros(N)

    for cur in results:
        tmp_regret = pickle.loads(cur["regret"])
        regret = regret + tmp_regret

    regret = regret / lensim

    ax.plot(regret, label = v['label'])

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.title('Average regret over time')
plt.xlabel('Time')
plt.ylabel('Regret')
lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

fig.savefig('regrets.eps', format='eps', bbox_extra_artists=(lgd,), bbox_inches = 'tight')

for k,v in experiments.items():
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    exp_id = k
    results = mongo_db.logs.find({"type":"evaluation","experiment":exp_id}, sort=[("time", DESCENDING)])

    rewards = np.zeros(N)

    for cur in results:
        tmp_rewards = pickle.loads(cur["rewards"])
        rewards = rewards + tmp_rewards

    rewards = rewards / lensim

    ax.plot(rewards, label = v['label'])

    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.title('Average rewards over time')
    plt.xlabel('Time')
    plt.ylabel('Reward')
    #lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

    fig.savefig('rewards_{}.eps'.format(v['label']), format='eps')
    #fig.savefig('rewards.eps', format='eps', bbox_extra_artists=(lgd,), bbox_inches = 'tight')
