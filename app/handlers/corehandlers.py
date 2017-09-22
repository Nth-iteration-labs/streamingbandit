# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
from bson import json_util
import json

from core.experiment import Experiment

from handlers.basehandler import BaseHandler, ExceptionHandler

class ActionHandler(tornado.web.RequestHandler):
           
    def get(self, exp_id): # Documentation needs update to advice_id
        """ Get an action given a context for a specific exp_id.
        
        +----------------------------------------------------------------+
        | Example                                                        |
        +================================================================+
        |http://example.com/EXP_ID/getaction.json?key=KEY&context=CONTEXT|
        +----------------------------------------------------------------+
        
        :param int exp_id: Experiment ID as specified in the url.
        :param string key: The key corresponding to the experiment.
        :param JSON context (optional): The context to be evaluated. 
        :returns: A JSON that standard only includes action. When debug is toggled, \
        it returns the context as well. When Advice ID is toggled, it will also return \
        an Advice ID that can be used to set the reward later on.
        :raises 400: If the key is not supplied.
        :raises 401: If the key or exp_id is invalid.
        """
        key = self.get_argument("key", default = False)
        context = json.loads(self.get_argument("context", default = "{}"))  

        if not key:
            raise ExceptionHandler(reason = "Key not supplied.", status_code = 400)
        
        __EXP__ = Experiment(exp_id, key)
        
        if __EXP__.is_valid():
            response = __EXP__.run_action_code(context)
            
            if __EXP__.properties['advice_id'] == "True":
                advice_id = __EXP__.gen_advice_id(response.copy(), context.copy())

            __EXP__.log_getaction_data(context, response)

            if self.settings['debug'] and __EXP__.properties['advice_id'] == "True":
                self.write(json.dumps({'action':response, 'context':context, 'advice_id':advice_id}, default = json_util.default))
            elif __EXP__.properties['advice_id'] == "True":
                self.write(json.dumps({'action':response, 'advice_id':advice_id}, default = json_util.default))
            elif self.settings['debug']:
                self.write(json.dumps({'action':response, 'context':context}))
            else:
                self.write(json.dumps({'action':response}))
        else:
            raise ExceptionHandler(reason = "Key or exp_id is invalid.", status_code = 401)

class RewardHandler(tornado.web.RequestHandler):

    def get(self, exp_id): # Documentation needs update to advice_id
        """ Update the parameters and set a reward for a given experiment.

        For parameters, there are two options (next to the mandatory key 
        and exp_id). The first option is supplying all the information manually, 
        meaning that you supply the following parameters:
            -   Context
            -   Action
            -   Reward

        +----------------------------------------------------------------+
        | Example                                                        |
        +================================================================+
        |http://example.com/EXP_ID/setreward.json?key=KEY&context=CONTEXT|
        |&action=ACTION&reward=REWARD                                    |
        +----------------------------------------------------------------+

        When you have toggled the Advice ID in the experiment properties (second option), 
        and have received an Advice ID from the getaction call, you only have
        to supply the following parameters:
            -   Advice ID
            -   Reward

        +----------------------------------------------------------------+
        | Example                                                        |
        +================================================================+
        |http://example.com/EXP_ID/setreward.json?key=KEY                |
        |&advice_id=ADVICE_ID&reward=REWARD                              |
        +----------------------------------------------------------------+

        :param int exp_id: Experiment ID as specified in the url.
        :param string key: The key corresponding to the experiment.

        :param JSON context (optional): The context for the current update.
        :param JSON action (optional): The action for the current update.
        :param string advice_id (optional): The advice_id for the current \
        full update loop.
        :param JSON reward: The reward for the current update.
        :returns: A JSON indicating success.
        :raises 400: If key is not supplied.
        :raises 401: If the key or exp_id is invalid.
        """
        key = self.get_argument("key", default = False)

        if not key:
            raise ExceptionHandler(reason = "Key not supplied.", status_code = 400)

        __EXP__ = Experiment(exp_id, key)

        if __EXP__.is_valid():
            if self.get_argument("advice_id", default = "") == "":
                context = json.loads(self.get_argument("context", default = "{}"))
                action = json.loads(self.get_argument("action", default = "{}"))
            else:
                advice_id = self.get_argument("advice_id", default = "")
                log = __EXP__.get_by_advice_id(advice_id)
                if log == False:
                    self.finish("Advice ID does not exist!")
                else:
                    context = log['context']
                    action = log['action']
            reward = json.loads(self.get_argument("reward", default="{}"))
            __EXP__.run_reward_code(context, action, reward)
            __EXP__.log_setreward_data(context, action, reward)
            
            if self.settings['debug']:
                self.write(json.dumps({'status':'success', 'action':action, 'context':context, 'reward':reward}))
            else: 
                self.write(json.dumps({'status':'success'}))
        else:
            raise ExceptionHandler(reason = "Key or exp_id is invalid.", status_code = 401)
