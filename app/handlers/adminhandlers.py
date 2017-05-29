# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import random

import logging
logger = logging.getLogger("myLogger") 

from db.database import Database


class AddExperiment(tornado.web.RequestHandler):
    
    def get(self):
        raise tornado.web.HTTPError(status_code=404, log_message="invalid call")
    
    def delete(self):
        raise tornado.web.HTTPError(status_code=404, log_message="invalid call")
    
    
    def post(self):
        """ Create a new experiment
        
        :requires: A secure cookie obtained by logging in.
        :param string name: Name of the experiment
        :param string getaction: String of python code for get action code
        :param string setreward: String of python code for set reward code
        :param bool adviceid: Bool indicating whether adviceIds are used
        :param bool hourly: Bool indicating whether the state of Theta should be stored hourly. 
        :returns: A JSON of the form:
            { id : the assigned experiment id, 
             name : the name of the experiment (checked for duplicates),
             error : (optional) error message }
        :raises AUTH_ERROR: If no secure cookie available.
        """
        if self.get_secure_cookie("user"):
            exp_obj = {}
            exp_obj["name"] = self.get_body_argument("name")
            exp_obj["getAction"] = self.get_body_argument("getaction")
            exp_obj["setReward"] = self.get_body_argument("setreward")
            exp_obj["hourlyTheta"] = self.get_body_argument("hourly")
            exp_obj["advice_id"] = self.get_body_argument("advice_id")
            if exp_obj["advice_id"] is True:
                exp_obj["delta_days"] = self.get_body_argument("delta_days")
                exp_obj["default_reward"] = self.get_body_argument("default_reward")
        
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


class DeleteExperiment(tornado.web.RequestHandler):
    
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
        if self.get_secure_cookie("user"):
            db = Database()
            response = db.delete_experiment(exp_id)
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")
        

class GetListOfExperiments(tornado.web.RequestHandler):
    
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
        if self.get_secure_cookie("user"):
            db = Database()
            response = db.get_all_experiments()
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")
        
        
class GetExperiment(tornado.web.RequestHandler):
    
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
        if self.get_secure_cookie("user"):
            db = Database()
            response = db.get_one_experiment(exp_id)
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")

        
class EditExperiment(tornado.web.RequestHandler):
    
    def get(self):
        self.write_error(400)   # we really need nicer error handling
    
    def post(self, exp_id):
        """ Retrieve a list of experiments running on this server
       
        :requires: A secure cookie obtained by logging in.
        :param string name: Name of the experiment
        :param string getaction: String of python code for get action code
        :param string setreward: String of python code for set reward code
        :param bool adviceid: Bool indicating whether adviceIds are used
        :param bool hourly: Bool indicating whether the state of Theta should be stored hourly (apscheduler)
        :returns: A JSON containing error yes / no.
        :raises AUTH_ERROR: If no secure cookie avaiable.
        """
        if self.get_secure_cookie("user"):
            exp_obj = {}
            exp_obj["name"] = self.get_body_argument("name")
            exp_obj["getAction"] = self.get_body_argument("getaction")
            exp_obj["setReward"] = self.get_body_argument("setreward")      
            exp_obj["hourlyTheta"] = self.get_body_argument("hourly")
            exp_obj["advice_id"] = self.get_body_argument("advice_id")
            if exp_obj["advice_id"] is True:
                exp_obj["delta_days"] = self.get_body_argument("delta_days")
                exp_obj["default_reward"] = self.get_body_argument("default_reward")
        
            db = Database()
            response = {}
            response["id"] = db.edit_experiment(exp_obj, exp_id)
            self.write(json.dumps(response))
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
            json_data=open("./libs/defaults.json").read()
            data = json.loads(json_data)
            self.write(data)
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
            json_data=open("./libs/defaults.json").read()
            raw=json.loads(json_data)       
            data={}
            data["name"] = raw["defaults"][default_id]["name"]
            data["getAction"]=open("./libs/defaults/"+raw["defaults"][default_id]["getActionCode"]).read()
            data["setReward"]=open("./libs/defaults/"+raw["defaults"][default_id]["setRewardCode"]).read()
            self.write(data)
        else:
            self.write("AUTH_ERROR")
