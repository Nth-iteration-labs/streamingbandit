import json
from requests import put,get
import numpy as np
import matplotlib.pyplot as  plt
from pymongo import MongoClient, ASCENDING, DESCENDING

mongo_client = MongoClient('localhost',27017)
mongo_db = mongo_client['logs']

c2 = 10

experiments = { 
                5 : { 'key' : "281804239f" , 'label' : 'Random', 'color' : 'black'},
                #7 : { 'key' : "29ffa7bc43" , 'label' : 'LiF', 'color' : 'brown' },
                #8 : { 'key' : "1e14243bd5" , 'label' : 'TBL', 'color' : 'blue'},
                #9 : { 'key' : "16f451a9d6" , 'label' : 'BTS', 'color' : 'red'},
               #10 : { 'key' : "384ea03749" , 'label' : 'Epsilon-first', 'color' : 'green'}
        }


fig = plt.figure(1)
ax = fig.add_subplot(111)

for k,v in experiments.items():
    exp_id = k

    print("I got here")

    for i in range(100):
        print(i)

        results = mongo_db.logs.find({"type":"offline_evaluation_iters","iteration":i,"experiment":exp_id,"var":0.1},sort=[("time",DESCENDING)])

        #suggestion = np.array([0])
        #action = np.array([0])
        regret = np.array([0])

        for row in results:
            #print(row["suggestion"])
            #suggestion = np.append(suggestion, row["suggestion"])
            #action = np.append(action, row["action"])
            regret = np.append(regret, (regret[-1] + (c2 - row["reward"])))

        print(v['label'])
        print(len(regret))

        ax.plot(regret)#, label = v['label'], color = v['color'])

#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.title('Average regret over time')
plt.xlabel('Time')
plt.ylabel('Regret')
#lgd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

fig.savefig('offline_regrets_averagerand.eps', format='eps')#, bbox_extra_artists=(lgd,), bbox_inches = 'tight')

#threshold = action - suggestion

#plt.plot(threshold)
#plt.plot(regret)
#plt.ylabel("Regret")
#plt.xlabel("Time")
#plt.show()

#plt.plot(suggestion)
#plt.title("Suggestions")
#plt.xlabel("Time")
#plt.ylabel("x")
#plt.show()
