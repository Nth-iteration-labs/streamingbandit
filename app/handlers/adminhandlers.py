# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import random
import os

import logging
logger = logging.getLogger("myLogger") 

from handlers.basehandler import BaseHandler

from db.database import Database
from db.users import Users


class AddExperiment(BaseHandler):
    
    def get(self):
        raise tornado.web.HTTPError(status_code=404, log_message="invalid call")
    
    def delete(self):
        raise tornado.web.HTTPError(status_code=404, log_message="invalid call")
    
    def post(self):
        """ Create a new experiment
        
        :requires: A secure cookie obtained by logging in.
        :param string name: Name of the experiment
        :param string getcontext: String of python code for get context code
        :param string getaction: String of python code for get action code
        :param string getreward: String of python code for get reward code
        :param string setreward: String of python code for set reward code
        :param bool adviceid: Bool indicating whether adviceIds are used
        :param bool hourly: Bool indicating whether the state of Theta should be stored hourly. 
        :param bool advice_id: Bool indicating whether the getAdvice and setReward calls should return an advice_id
        :param int delta_days: If advice_id is True, supply this to give the number of days that an advice_id should be stored
        :param dict default_reward: If advice_id is True, supply this to give the default reward for advice_id's that are over their delta_days limit
        :returns: A JSON of the form:
            { id : the assigned experiment id, 
             name : the name of the experiment (checked for duplicates),
             error : (optional) error message }
        :raises AUTH_ERROR: If no secure cookie available.
        """
        user = self.get_current_user()
        if user:
            exp_obj = {}
            exp_obj["user_id"] = int(user)
            exp_obj["name"] = self.get_argument("name")
            exp_obj["getContext"] = self.get_argument("getcontext")
            exp_obj["getAction"] = self.get_argument("getaction")
            exp_obj["getReward"] = self.get_argument("getreward")
            exp_obj["setReward"] = self.get_argument("setreward")
            exp_obj["hourlyTheta"] = self.get_argument("hourly")
            exp_obj["advice_id"] = self.get_argument("advice_id")
            if exp_obj["advice_id"] in ["true", "True", "y", "yes"]:
                exp_obj["advice_id"] = True
            if exp_obj["advice_id"] is True:
                exp_obj["delta_days"] = self.get_argument("delta_days")
                exp_obj["default_reward"] = self.get_argument("default_reward")
        
            # Generate key (also stored in REDIS)
            exp_obj["key"] = hex(random.getrandbits(42))[2:-1]

            db = Database() 
            insertid = db.insert_experiment(exp_obj)
        
            response = {}
            response["name"] = exp_obj["name"]
            response["id"] = insertid
            response["key"] = exp_obj["key"]
            response["error"] = False
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")


class DeleteExperiment(BaseHandler):
    
    def get(self, exp_id):
        """ Delete an experiment given an experiment id

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/admin/exp/1/delete.json                         |
        +--------------------------------------------------------------------+
        
        :requires: A secure cookie obtained by logging in.
        :param int exp_id: The ID of the experiment to be deleted.
        :returns: A JSON showing the deleted experiment.
        :raises AUTH_ERROR: if no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                db = Database()
                response = db.delete_experiment(exp_id)
                self.write(json.dumps(response))
            else:
                self.write("This experiment does not exist or does not belong to this user ID.") # Better error message?
        else:
            self.write("AUTH_ERROR")
        

class GetListOfExperiments(BaseHandler):
    
    def get(self):
        """ Retrieve a list of experiments running on this server
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/admin/exp/list.json?max=10                      |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param int max: Indicating the max length of the list.
        :returns: A JSON containing a list of {expid : name} pairs
        :raises AUTH_ERROR: If not secure cookie available.
        """
        user = self.get_current_user()
        if user: 
            db = Database()
            response = db.get_all_experiments(int(user))
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")
        
        
class GetExperiment(BaseHandler):
    
    def get(self, exp_id):
        """ Retrieve a specific experiment running on this server
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/admin/exp/1/get.json                            |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param int exp_id: String experiment ID (in Query string)
        :returns: A JSON containing all the info for the expriment.
        :raises AUTH_ERROR: If no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                db = Database()
                response = db.get_one_experiment(exp_id)
                self.write(json.dumps(response))
            else:
                self.write("This experiment does not exist or does not belong to this user ID.") # Better error message?
        else:
            self.write("AUTH_ERROR")

        
class EditExperiment(BaseHandler):
    
    def get(self):
        self.write_error(400)   # we really need nicer error handling
    
    def post(self, exp_id):
        """ Retrieve a list of experiments running on this server
       
        :requires: A secure cookie obtained by logging in.
        :param string name: Name of the experiment
        :param string getcontext: String of python code for get context code
        :param string getaction: String of python code for get action code
        :param string getreward: String of python code for get reward code
        :param string setreward: String of python code for set reward code
        :param bool adviceid: Bool indicating whether adviceIds are used
        :param bool hourly: Bool indicating whether the state of Theta should be stored hourly (apscheduler)
        :param bool advice_id: Bool indicating whether the getAdvice and setReward calls should return an advice_id
        :param int delta_days: If advice_id is True, supply this to give the number of days that an advice_id should be stored
        :param dict default_reward: If advice_id is True, supply this to give the default reward for advice_id's that are over their delta_days limit
        :returns: A JSON containing error yes / no.
        :raises AUTH_ERROR: If no secure cookie avaiable.
        """
        user = self.get_current_user()
        if user: 
            if self.validate_user_experiment(exp_id):
                exp_obj = {}
                exp_obj["user_id"] = int(user)
                exp_obj["name"] = self.get_argument("name")
                exp_obj["getContext"] = self.get_argument("getcontext")
                exp_obj["getAction"] = self.get_argument("getaction")
                exp_obj["getReward"] = self.get_argument("getreward")
                exp_obj["setReward"] = self.get_argument("setreward")
                exp_obj["hourlyTheta"] = self.get_argument("hourly")
                exp_obj["advice_id"] = self.get_argument("advice_id")
                if exp_obj["advice_id"] in ["true", "True", "y", "yes"]:
                    exp_obj["advice_id"] = True
                if exp_obj["advice_id"] is True:
                    exp_obj["delta_days"] = self.get_argument("delta_days")
                    exp_obj["default_reward"] = self.get_argument("default_reward")
            
                db = Database()
                response = {}
                response["id"] = db.edit_experiment(exp_obj, exp_id)
                self.write(json.dumps(response))
            else:
                self.write("This experiment does not exist or does not belong to this user ID.") # Better error message?
        else:
            self.write("AUTH_ERROR")


class ListDefaults(tornado.web.RequestHandler):
    
    def get(self):
        """ Get the list with default available experiments.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/admin/exp/defaults.json                         |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :returns: A JSON with the default experiments.
        :raises AUTH_ERROR: If no secure cookie available.
        """
        if self.get_secure_cookie("user"):
            folderdata=os.listdir("./defaults")
            folders = dict(enumerate(folderdata))
            self.write(folders)
        else:
            self.write("AUTH_ERROR")
 
       
class GetDefault(tornado.web.RequestHandler):
    
    def get(self, default_id):
        """ Retrieve properties of a default experiment.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/admin/exp/default/1/get.json                    |
        +--------------------------------------------------------------------+

        :requires: A secure cookie available by logging in.
        :param int default_id: The ID of the default experiment.
        :returns: A JSON containing the experiment properties.
        :raises AUTH_ERROR: If no secure cookie available.
        """ 
        if self.get_secure_cookie("user"):
            # first the name of the experiment
            folderdata = os.listdir("./defaults")
            folderdata = dict(enumerate(folderdata))
            data={}
            data["name"] = folderdata[default_id]
            data["getContext"] = open("./defaults/"+data["name"]+"/getContext.py").read()
            data["getAction"] = open("./defaults/"+data["name"]+"/getAction.py").read()
            data["getReward"] = open("./defaults/"+data["name"]+"/getReward.py").read()
            data["setReward"] = open("./defaults/"+data["name"]+"/setReward.py").read()
            self.write(data)
        else:
            self.write("AUTH_ERROR")


class ResetExperiment(BaseHandler):
    # Update this such that we require secure_cookie
    def get(self, exp_id):

        if self.get_secure_cookie("user"):
            key = self.get_argument("key", default = False)
            theta_key = self.get_argument("theta_key", default = False)
            theta_value = self.get_argument("theta_value", default = False)
            __EXP__ = Experiment(exp_id, key)

            if __EXP__.is_valid():
                status = __EXP__.delete_theta(key = theta_key, value = theta_value)
                if status == True:
                    self.write(json.dumps({'status':'success'}))
                else:
                    self.write(json.dumps({'status':'key does not exist'}))
            else:
                self.write_error(400)
        else:
            self.write("AUTH_ERROR")

class AddUser(BaseHandler):

    def get(self):
        users = Users()
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_id = users.create_user(username, password)
        if user_id is False:
            self.write("User already exists!")
        else:
            self.write(json.dumps({'status' : 'success'}))
