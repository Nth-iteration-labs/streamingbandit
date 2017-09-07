# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
from bson import json_util
import json

from core.experiment import Experiment

class ActionHandler(tornado.web.RequestHandler):
           
    def get(self, exp_id): # Documentation needs update to advice_id
        """ Get an action given a context for a specific exp_id
        
        +----------------------------------------------------------------+
        | Example                                                        |
        +================================================================+
        |http://example.com/1/getAction.json?key=XXXX&context={'age': 25}|
        +----------------------------------------------------------------+
        
        
        :param int exp_id: Experiment ID as specified in the url
        :param JSON context: The context to be evaluated. 
        :param string key: The key corresponding to the experiment.
        
        :returns: A JSON of the form: {"action": XX}
        :raises AuthErorr: 401 Invalid key
        """
        key = self.get_argument("key", default = False)
        
        if not key:
            self.set_status(401)
            self.write("invalid key")
            return
        
        __EXP__ = Experiment(exp_id, key)
        
        if __EXP__.is_valid():
            context = json.loads(self.get_argument("context", default="{}"))  
            response = __EXP__.run_action_code(context)
            
            if __EXP__.properties['advice_id'] == "True":
                advice_id = __EXP__.gen_advice_id(response.copy(), context.copy())

            # If that is the case, generate an advice_id using the functions in db.advice
            # Or make a function in the Experiment class who will do this for you
            # Return the advice_id and action response
            if self.settings['debug'] and __EXP__.properties['advice_id'] == "True":
                self.write(json.dumps({'action':response, 'context':context, 'advice_id':advice_id}, default = json_util.default))
            elif self.settings['debug']:
                self.write(json.dumps({'action':response, 'context':context}))
            else:
                self.write(json.dumps({'action':response}))
                
        else:
            self.set_status(401)       # Needs proper error handling
            self.write("invalid key")
            return

class RewardHandler(tornado.web.RequestHandler):

    def get(self, exp_id): # Documentation needs update to advice_id
        """ Update the parameters for a given experiment

        +----------------------------------------------------------------+
        | Example                                                        |
        +================================================================+
        |http://example.com/1/setReward.json?key=XXXX&context={'age': 25}|
        |&action={'action':'A'}&reward={'click':1}                       |
        +----------------------------------------------------------------+

        :param int exp_id: Experiment ID as specified in the url
        :param JSON context: The context to train on.
        :param JSON action: The action to train on.
        :param JSON reward: The reward for the experiment.
        :param string key: The key corresponding to the experiment.

        :returns: A JSON of the form: {"status":true}
        :raises KeyError: 400 Error if Key is not valid.
        """
        key = self.get_argument("key", default = False)
        __EXP__ = Experiment(exp_id, key)

        if __EXP__.is_valid():
            if self.get_argument("advice_id", default = "") == "":
                context = json.loads(self.get_argument("context", default="{}"))
                action = json.loads(self.get_argument("action", default="{}"))
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
            __EXP__.log_setreward_data(contex, action, reward)
            
            if self.settings['debug']:
                self.write(json.dumps({'status':'success', 'action':action, 'context':context, 'reward':reward}))
            else: 
                self.write(json.dumps({'status':'success'}))
        else:
            self.write_error(400) # Needs proper error handling
