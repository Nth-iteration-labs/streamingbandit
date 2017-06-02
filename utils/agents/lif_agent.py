# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import urllib
import json
import codecs
import pymongo
import future

# Settings

MONGO_IP = "localhost"
MONGO_PORT = 27017
BASE_URL = "http://localhost:8080"
key = "2857aa87a7"
exp_id = 4
question_nr = 12345678

# Python 2 and 3 compatibility
from future.standard_library import install_aliases
install_aliases()


#############################################################
# This is the agent used in the Lock-in Feedback example
# See the README in the utils folder for more information
#############################################################


def do_chart(qr):
    client = pymongo.MongoClient(MONGO_IP, MONGO_PORT)
    db = client.logs

    fig = plt.figure(figsize=(4.8, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(which='both', direction='out')
    ax.grid(which='both')

    cursor = db.logs.find({"type": "setreward", "q": int(qr)}) \
        .sort([("t", pymongo.ASCENDING)])
    result_list = list(cursor)
    client.close()
    t_local = [ts['t'] for ts in result_list]
    x0 = [xs['x0'] for xs in result_list]
    plt.plot(t_local, x0)
    plt.show()


def getobs(x_in, max_in=5, err=0):
    if err == 0:
        obsr = -1 * pow((x_in - max_in), 2)
    else:
        obsr = -1 * pow((x_in - max_in), 2) + np.random.normal(0, err, 1)
    return obsr


stream = 200
p_return = 0.80
variance = 1
track_x = []
x = 0.0
t = 0.0
y = 1.0

for i in range(0, stream):

    request = BASE_URL + "/" + str(exp_id) + "/getAction.json?key=" + key
    request += "&context={\"question\":" + str(question_nr) + "}"
    response = urllib.request.urlopen(request)
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))

    t = (obj["action"]["t"])
    x = (obj["action"]["x"])

    if np.random.binomial(1, p_return, 1) == 1:
        y = getobs(x, 5, variance)

        request = BASE_URL + "/" + str(exp_id) + "/setReward.json"
        request += "?key=" + key
        request += "&context={\"question\":" + str(question_nr) + "}"
        request += "&action={\"x\":" + str(float(x))
        request += ",\"t\":" + str(float(t)) + "}"
        request += "&reward=" + str(float(y))

        response = urllib.request.urlopen(request)
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(response))

    track_x = np.append(track_x, x)

plt.plot(track_x)
plt.show()
do_chart(question_nr)
