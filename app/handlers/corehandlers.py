# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from core.experiment import Experiment

class ActionHandler(tornado.web.RequestHandler):
           
    def get(self, exp_id):
        """ Get an action given a context for a specific exp_id
        
        Input arguments:
        exp_id: Experiment ID as specified in the url
        context: string of JSON object which obtains the context. This is assumed to be passed in the query string 
        key: part of the JSON object        
        
        Returns:
        A JSON object containing "action": XX
        Or an object containing "error": ...
        """
        context = json.loads(self.get_argument("context", default="{}"))
        key = self.get_argument("key", default = False)
        
        __EXP__ = Experiment(exp_id, key)
        
        if __EXP__.is_valid():
            response = __EXP__.run_action_code(context)
            self.write(json.dumps({'status':'success', 'action':response}))
        else:
            self.write_error(400)       # Needs proper error handling

class RewardHandler(tornado.web.RequestHandler):

    def get(self, exp_id):
        """ Update the parameters for a given experiment

        Input arguments:
        exp_id: Experiment ID as specified in the url
        context: in JSON get
        action: in JSON get
        reward: in JSON get
        key: in JSON get

        Returns:
        A JSON object containing "status":true
        Or an object containing "error": ...
        """
        key = self.get_argument("key", default = False)
        __EXP__ = Experiment(exp_id, key)

        if __EXP__.is_valid():
            context = json.loads(self.get_argument("context", default="{}"))
            action = json.loads(self.get_argument("action", default="{}"))
            reward = float(self.get_argument("reward", default=0))
            __EXP__.run_reward_code(context, action, reward)
            self.write(json.dumps({'status':'success','_debug': {'action':action,'context':context}}))  
        else:
            self.write_error(400)       # Needs proper error handling
