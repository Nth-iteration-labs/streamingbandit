# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import numpy as np
import time

from bson.binary import Binary
import _pickle

from core.experiment import Experiment

class Simulate(tornado.web.RequestHandler):

    def get(self, exp_id):
        """ Simulate your experiment on a simple model
        The model that is drawn from is:

        y = -(x - c)**2 + c2 + rnorm(mu,var)

        Currently there is no context. Make sure that the action of your
        experiment results in:

        {"x" : x}

        This is how the model currently expects your action to be formulated.
        This might become more flexible later on.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        |http://example.com/eval/5/simulate?key=XXX&N=10&c=5&c2=10&mu=0&var=1|
        +--------------------------------------------------------------------+

        :param int exp_id: Experiment ID as specified in the url
        :param string key: The key corresponding to the experiment
        :param int N: The number of simulation draws
        :param int c: The size of the parabola
        :param int c2: The height of the parabola
        :param int mu: The mean of the noise on the model
        :param int var: The variance of the noise on the model
        :param string log_stats: Flag for logging the results in the database
        
        :returns: A JSON of the form: {"simulate":"success"}
        :raises AuthError: 401 Invalid Key

        """

        key = self.get_argument("key", default = False)
        
        # Number of draws
        N = int(self.get_argument("N", default = 1000))

        log_stats = self.get_argument("log_stats", default = True)

        # Parameterset for the simulator
        c = float(self.get_argument("c", default = 5))
        c2 = float(self.get_argument("c2", default = 10))
        mu = float(self.get_argument("mu", default = 0))
        var = float(self.get_argument("var", default = .1))

        if not key:
            self.set_status(401)
            self.write("Key not given")
            return

        __EXP__ = Experiment(exp_id, key)

        rewards = np.array([0])
        reward_over_time = np.array([])
        regret = np.array([0])

        if __EXP__.is_valid():
            for i in range(N):
                # Generate context
                context = {}

                # Get action

                action = __EXP__.run_action_code(context)

                # Generate reward

                y = -(action["x"] - c)**2 + c2 + np.random.normal(mu, var)
                #y = 15 + 8*action["x"] + 10*action["x"]**2 + np.random.normal(mu, var)

                reward = {"y" : y}

                # Set reward
                __EXP__.run_reward_code(context, action, reward)
                
                # Save stats
                rewards = np.append(rewards, y)
                tmp_rot = (rewards[-1] + y) / (i+1)
                reward_over_time = np.append(reward_over_time, tmp_rot)
                regret = np.append(regret, (regret[-1] + (c2 - y)))

                #self.write("n = {}, Regret is: {}, reward = {} <br>".format(i,regret[-1], rewards[-1]))


            # Now save the data together with a timestamp in the logs
            # To read out the Numpy array data out again, use array =
            # pickle.loads(record['feature'])

            # FOR FUTURE, the json_tricks package might be interesting
            if log_stats == True:
                print("Logging data")
                __EXP__.log_data({
                    "type" : "evaluation",
                    "time" : int(time.time()),
                    "experiment" : exp_id,
                    "N" : N,
                    "c" : c,
                    "c2" : c2,
                    "rewards" : Binary(_pickle.dumps(rewards, protocol = 2), subtype = 128),
                    "reward_over_time" : Binary(_pickle.dumps(reward_over_time, protocol = 2), subtype = 128),
                    "regret" : Binary(_pickle.dumps(regret, protocol = 2), subtype = 128)
                    })

                self.write(json.dumps({'simulate':'success','experiment':exp_id}))
        else:
            self.set_status(401)
            self.write("Key is not valid for this experiment")
            return



#class Offline(tornado.web.Requesthandler):
