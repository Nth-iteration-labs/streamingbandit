import numpy as np
import matplotlib.pyplot as plt
import pickle
from pymongo import MongoClient, ASCENDING, DESCENDING

mongo_client = MongoClient('localhost',27017)
mongo_db = mongo_client['logs']

exp_id = "1"

results = mongo_db.logs.find_one({"type":"evaluation","experiment":exp_id},sort=[("time", DESCENDING)])

logs = mongo_db.logs.find({"type":"getadvice","experiment":exp_id},sort=[("time",DESCENDING)]).limit(1000)

betas = []
x = []
J = []
mu = []
for row in logs:
    betas.append(row['betas'])
    x.append(row['x'])
    tmp = np.matrix(row['J'])
    tmp = np.squeeze(np.asarray(tmp))
    J.append(tmp.tolist())
    tmp = np.matrix(row['mu'])
    tmp = np.squeeze(np.asarray(tmp))
    mu.append(tmp.tolist())

plt.plot(mu)
plt.show()

#plt.plot(betas)
#plt.show()

#plt.plot(J)
#plt.show()

#plt.plot(x)
#plt.show()

regret = pickle.loads(results["regret"])

plt.plot(regret)
plt.title('Regret over time')
plt.xlabel('Time')
plt.ylabel('Regret')
plt.show()

#reward_over_time = pickle.loads(results["reward_over_time"])

#plt.plot(reward_over_time)
#plt.show()

rewards = pickle.loads(results["rewards"])

plt.plot(rewards)
plt.title('Rewards')
plt.xlabel('Time')
plt.ylabel('Reward')
plt.show()
