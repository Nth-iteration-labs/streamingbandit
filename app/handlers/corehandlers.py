# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from libs.experiment import Experiment

class ActionHandler(tornado.web.RequestHandler):
           
    def get(self, exp_id):
        """ Get an action given a context for a specific exp_id
        
        Input arguments:
        exp_id: Experiment ID as specified in the url
        context: string of JSON object which obtains the context. This is assumed to be passed in the query string 
        key: part of the JSON object        
        
        Returns:
        A JSON object containing "action":XX
        Or an object containing "error": ...
        """
        
        # 1. Get details call:
        self.context = json.loads(self.get_argument("context", default="{}"))
        self.key = self.get_argument("key", default = False)
        
        # 2. Instantiate experiment.
        exp = Experiment(exp_id, self.key)
        
        # 3. Check if valid (key ok? experiment exist in DB?)
        if exp.is_valid():
            self.action = {}
            # 4. retrieve the code of the exepriment and execute:
            self.action = exp.run_action_code(self.context)
            
            # Return advice as JSON
            self.write(json.dumps(self.action))

        else:
            self.write("unknown id")

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
        self.key = self.get_argument("key", default = False)
        exp = Experiment(exp_id, self.key)

        if exp.is_valid():
            self.context = json.loads(self.get_argument("context", default="{}"))
            self.action = json.loads(self.get_argument("action", default="{}"))
            self.reward = float(self.get_argument("reward", default=0))
            exp.run_reward_code(self.context, self.action, self.reward)
            self.write(json.dumps(self.action))  
        else:
            # ERROR MESSAGE
