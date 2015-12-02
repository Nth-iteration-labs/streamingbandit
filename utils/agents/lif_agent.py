# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import urllib,json,codecs

#change this to pymongo for greater compatibility
import iopro 

def getobs( x, max = 5, err=0 ):
    if (err==0):
        obsr = -1*pow((x-max),2)
    else:
        obsr = -1*pow((x-max),2) + np.random.normal(0,err,1)
    return obsr;
    
q = 99          
stream = 200                                         
p_return = 0.80                         
variance = 1
track_x  = []
x = 0.0
t = 0.0
y = 0.0

for i in range(0,stream):

   request = "http://78.46.212.194:8080/2/getAction.json?key=24ff7bb26&context={\"question\":"+str(q)+"}"
   response = urllib.request.urlopen(request)
   reader = codecs.getreader("utf-8") 
   obj = json.load(reader(response))
   
   t =  (obj["action"]["t"])
   x =  (obj["action"]["x"])
   
   if np.random.binomial(1, p_return, 1)==1: 
       
       y = getobs(x,5,variance)
       
       request =  "http://78.46.212.194:8080/2/setReward.json"
       request += "?key=24ff7bb26"
       request += "&context={\"question\":"+str(q)+"}"
       request += "&action={\"x\":" + str(float(x)) +",\"t\":" + str(float(t)) + "}"
       request += "&reward=" + str(float(y))
                    
       response = urllib.request.urlopen(request)
       reader = codecs.getreader("utf-8") 
       obj = json.load(reader(response)) 

   # log x
   track_x  =  np.append(track_x, x)

plt.plot(track_x)
plt.show()

#change the following to pymongo for greater compatibility

adapter = iopro.MongoAdapter('78.46.212.194', 27017, 'logs', 'logs')
results = adapter[['type','q','t', 'x','y','x0']][:]
results = np.sort(results, order='t')
t_x = results[['t','x0']][np.intersect1d(np.where(results['type'][:] == 'setreward'),np.where(results['q'][:]==q))]
plt.plot(t_x[['t']], t_x[['x0']])
plt.show()