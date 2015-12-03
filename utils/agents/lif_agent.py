# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import urllib,json,codecs

#change to pymongo for greater compatibility
import iopro 

def getobs( x, max = 5, err=0 ):
    if (err==0):
        obsr = -1*pow((x-max),2)
    else:
        obsr = -1*pow((x-max),2) + np.random.normal(0,err,1)
    return obsr;

BASE_URL = "http://localhost:8080"
key = "69cd74c53"    
exp_id = 1
question_nr = 123456        

stream = 200                           
p_return = 0.80                         
variance = 1
track_x  = []
x = 0.0
t = 0.0
y = 1.0

for i in range(0,stream):

   request =  BASE_URL + "/" + str(exp_id) +"/getAction.json?key="+key
   request += "&context={\"question\":"+str(question_nr)+"}"
   response = urllib.request.urlopen(request)
   reader = codecs.getreader("utf-8") 
   obj = json.load(reader(response))
   
   t =  (obj["action"]["t"])
   x =  (obj["action"]["x"])
   
   if np.random.binomial(1, p_return, 1)==1: 
  
       y = getobs(x,5,variance)
       
       request =  BASE_URL + "/" + str(exp_id) + "/setReward.json"
       request += "?key="+key
       request += "&context={\"question\":"+str(question_nr)+"}"
       request += "&action={\"x\":" + str(float(x)) 
       request += ",\"t\":" + str(float(t)) + "}"
       request += "&reward=" + str(float(y))
                    
       response = urllib.request.urlopen(request)
       reader = codecs.getreader("utf-8") 
       obj = json.load(reader(response)) 

   # log x
   track_x  =  np.append(track_x, x)

plt.plot(track_x)
plt.show()

#change the following to pymongo for greater compatibility

adapter = iopro.MongoAdapter('localhost', 27017, 'logs', 'logs')
results = adapter[['type','q','t', 'x','y','x0']][:]
results = np.sort(results, order='t')
selection_setreward = np.where(results['type'][:] == 'setreward')
selection_question =  np.where(results['q'][:]==question_nr)
intersect = np.intersect1d(selection_setreward,selection_question)
t_x = results[['t','x0']][intersect]
plt.plot(t_x[['t']], t_x[['x0']])
plt.show()