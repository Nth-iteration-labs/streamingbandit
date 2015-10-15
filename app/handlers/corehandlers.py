# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from core.experiment import Experiment

class ActionHandler(tornado.web.RequestHandler):
           
    def get(self, exp_id):
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
            
            if self.settings['debug']:
                self.write(json.dumps({'action':response, 'context':context}))
            else:
                self.write(json.dumps({'action':response}))
                
        else:
            self.set_status(401)       # Needs proper error handling
            self.write("invalid key")
            return

class RewardHandler(tornado.web.RequestHandler):

    def get(self, exp_id):
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
            context = json.loads(self.get_argument("context", default="{}"))
            action = json.loads(self.get_argument("action", default="{}"))
            reward = json.loads(self.get_argument("reward", default="{}"))
            
            __EXP__.run_reward_code(context, action, reward)
            
            if self.settings['debug']:
                self.write(json.dumps({'status':'success', 'action':action,'context':context, 'reward':reward}))
            else: 
                self.write(json.dumps({'status':'success'}))
        else:
            self.write_error(400) # Needs proper error handling

            
