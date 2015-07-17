import json
import random as rnd
from requests import put, get


for i in range(200):
    # Get the action, by giving the expID
    r = get("http://localhost:8080/13/getAction.json?context={\"x\":12}&key=12321")
    #decoded = json.loads(r.decode('utf8'))
    jsonobj = json.loads(r.text)
    action = jsonobj["action"]
    print(r.text)    
    
    # Since we will not make a difference between action A and B, we do not need an if-else statement.
    reward = str(round(rnd.random()))
    # Put something without context
    r = get("http://localhost:8080/13/setReward.json?key=12321&reward="+reward+"&action={\"action\":\""+action+"\"}")
    print(r.text)
    print("Round"+str(i))

print("done")
