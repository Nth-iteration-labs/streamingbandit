# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import numpy as np
import time

from bson.binary import Binary
import _pickle

from handlers.basehandler import BaseHandler, ExceptionHandler
from core.experiment import Experiment

class Simulate(BaseHandler):

    def get(self, exp_id):
        """ Simulate your experiment based on four scripts, which create a closed feedback loop.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        |http://example.com/eval/EXP_ID/simulate?N=1000                      |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: Experiment ID as specified in the url.
        :param int N: The number of simulation draws.
        :returns: A JSON indicating success.
        :raises 400: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):

                N = int(self.get_argument("N", default = 1000))

                __EXP__ = Experiment(exp_id)

                for i in range(N):
                    # Generate context
                    context = __EXP__.run_context_code()

                    # Get action
                    action = __EXP__.run_action_code(context)

                    # Generate reward
                    reward = __EXP__.run_get_reward_code(context, action)

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
                raise ExceptionHandler(reason="Experiment could not be validated.", status_code=401)
        else:
            raise ExceptionHandler(reason="Could not validate user.", status_code=401)
