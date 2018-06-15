# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import numpy as np
import random
import time
import contextlib

from bson.binary import Binary
import _pickle

from handlers.basehandler import BaseHandler, ExceptionHandler
from core.experiment import Experiment

global numpy
global random

class Simulate(BaseHandler):

    def get(self, exp_id):
        """ Simulate your experiment based on four scripts, which create a closed feedback loop.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        |http://example.com/eval/EXP_ID/simulate?N=1000&log_stats=True       |
        |&verbose=True&seed=10                                               |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: Experiment ID as specified in the url.
        :param int N: The number of simulation draws.
        :param bool log_stats: Flag for logging the results in the database (default is False)
        :param bool verbose: Flag for displaying the results in the returning JSON object (default is True)
        :param int seed (optional): Set numpy seed.
        :returns: A JSON indicating success when verbose flag is False, and a JSON with all the data when verbose flag is True.
        :raises 400: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):

                N = int(self.get_argument("N", default = 1000))
                log_stats = self.get_argument("log_stats", default = False)
                verbose = self.get_argument("verbose", default = True)
                seed = self.get_argument("seed", default = None)
                if seed is None:
                    seed = np.random.randint(2**32-1, dtype=np.uint32)
                if verbose == "True":
                    verbose = True
                else:
                    verbose = False
                if log_stats == "True":
                    log_stats = True
                else:
                    log_stats = False

                __EXP__ = Experiment(exp_id)

                data = {}

                with self.temp_seed(int(seed)):
                    for i in range(N):
                        # Generate context
                        context = __EXP__.run_context_code()

                        # Get action
                        action = __EXP__.run_action_code(context)

                        # Generate reward
                        reward = __EXP__.run_get_reward_code(context, action)

                        # Set reward
                        __EXP__.run_reward_code(context, action, reward)

                        # Get theta
                        theta = __EXP__.get_theta()
                        
                        # Save stats
                        data[str(i)] = {'context' : context.copy(), 'action' : action.copy(), 'reward' : reward.copy(), 'theta' : theta.copy()}

                        context.clear()
                        action.clear()
                        reward.clear()

                if log_stats == True:
                    __EXP__.log_simulation_data(data.copy())
                data_tmp = data.copy()
                data.clear()

                if verbose == True:
                    self.write(json.dumps({'simulate':'success', 'experiment':exp_id, 'data':data_tmp}))
                else:
                    self.write(json.dumps({'simulate':'success', 'experiment':exp_id, 'theta':theta}))
            else:
                raise ExceptionHandler(reason="Experiment could not be validated.", status_code=401)
        else:
            raise ExceptionHandler(reason="Could not validate user.", status_code=401)
