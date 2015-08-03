# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
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
        
        Input (POST) arguments: (self.get_body_argument("name"))
        name : Name of the experiment
        getaction : String of python code for get action code
        setreward : String of python code for set reward code
        adviceid : Bool indicating whether adviceIds are used
        hourly : Bool indicating whether the state of Theta should be stored hourly (apscheduler)
        
        Returns:
        A JSON Blob containing
        id : the assigned experiment id
        name : the name of the experiment (checked for duplicates)
        error : (optional) error message
        """
        exp_obj = {}
        exp_obj["name"] = self.get_body_argument("name")
        exp_obj["getAction"] = self.get_body_argument("getaction")
        exp_obj["setReward"] = self.get_body_argument("setreward")

        db = Database() 
        insertid = db.insert_experiment(exp_obj)
        
        response = {}
        response["name"] = exp_obj["name"]
        response["id"] = insertid
        response["error"] = False
        self.write(json.dumps(response))

class DeleteExperiment(tornado.web.RequestHandler):
    
    def get(self, exp_id):
        """ Delete an experiment given an experiment id
        
        Input argument:
            exp_id : The ID of the experiment to be deleted
        
        Returs:
        A JSON Blob indicating the response
        """
        db = Database()
        response = db.delete_experiment(exp_id)
        self.write(json.dumps(response))
        

class GetListOfExperiments(tornado.web.RequestHandler):
    
    def get(self):
        """ Retrieve a list of experiments running on this server
        
        Input (GET) arguments (Optional): 
            max : integer indicating the max length of the list
        
        Returns:
        A JSON Blob containing a list of expid : name pairs, or a single entry
        """
        db = Database()
        response = db.get_all_experiments()
        self.write(json.dumps(response))
        
        
class GetExperiment(tornado.web.RequestHandler):
    
    def get(self, exp_id):
        """ Retrieve a specific experiment running on this server
        
        Input arguments : 
        id : String experiment ID (in Query string)
        
        Returns:
        A JSON Blob containing all the info for the expriment
        """
        db = Database()
        response = db.get_one_experiment(exp_id)
        self.write(json.dumps(response))

        
class EditExperiment(tornado.web.RequestHandler):
    
    def get(self):
        self.write_error(400)   # we really need nicer error handling
    
    def post(self, exp_id):
        """ Retrieve a list of experiments running on this server
        
        Input (POST) arguments: (self.get_body_argument("name"))
        name : Name of the experiment
        getaction : String of python code for get action code
        setreward : String of python code for set reward code
        adviceid : Bool indicating whether adviceIds are used
        hourly : Bool indicating whether the state of Theta should be stored hourly (apscheduler)
        
        Returns:
        A JSON Blob containing error yes / no
        """
        exp_obj = {}
        exp_obj["name"] = self.get_body_argument("name")
        exp_obj["getAction"] = self.get_body_argument("getaction")
        exp_obj["setReward"] = self.get_body_argument("setreward")      
        
        db = Database()
        response = {}
        response["id"] = db.edit_experiment(exp_obj, exp_id)
        self.write(json.dumps(response))




class ListDefaults(tornado.web.RequestHandler):
    
    def get(self):
        json_data=open("./libs/defaults.json").read()
        data = json.loads(json_data)
        self.write(data)
        
class GetDefault(tornado.web.RequestHandler):
    
    def get(self, default_id):
        # first the name of the experiment
        json_data=open("./libs/defaults.json").read()
        raw=json.loads(json_data)       
        data={}
        data["name"] = raw["defaults"][default_id]["name"]
        data["getAction"]=open("./libs/defaults/"+raw["defaults"][default_id]["getActionCode"]).read()
        data["setReward"]=open("./libs/defaults/"+raw["defaults"][default_id]["setRewardCode"]).read()
        self.write(data)
    
