# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from db.database import Database

class AddExperiment(tornado.web.RequestHandler):
    
    def get(self):
        self.write("404 ERROR")   # we really need nicer error handling
    
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
        
        # Firt retrieve the POST arguments:
        exp_obj = {}
        exp_obj["name"] = self.get_body_argument("name")
        exp_obj["getAction"] = self.get_body_argument("getaction")
        exp_obj["setReward"] = self.get_body_argument("setreward")
        exp_obj["adviceID"] = self.get_body_argument("adviceid")
        exp_obj["hourly"] = self.get_body_argument("hourly")

        # Then insert into database (returns the ID):
        db = Database() 
        insertid = db.insert_experiment(exp_obj)
    
        # Set the JSON response:      
        response = {}
        response["name"] = exp_obj["name"]
        response["id"] = insertid
        response["error"] = False
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
        self.write("404 ERROR")   # we really need nicer error handling
    
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
        # Build object:
        exp_obj = {}
        exp_obj["name"] = self.get_body_argument("name")
        exp_obj["getAction"] = self.get_body_argument("getaction")
        exp_obj["setReward"] = self.get_body_argument("setreward")
        exp_obj["adviceID"] = self.get_body_argument("adviceid")
        exp_obj["hourly"] = self.get_body_argument("hourly")        
        
        # Edit
        db = Database()
        response = {}
        response["id"] = db.edit_experiment(exp_obj, exp_id)
        self.write(json.dumps(response))


class ListDefaults(tornado.web.RequestHandler):
    
    # Load the file of defaults and return a list of their names:
    def get(self):
        json_data=open("./libs/defaults.json").read()
        data = json.loads(json_data)
        self.write(data)
        
class GetDefaultCodeByName(tornado.web.RequestHandler):
    
    # Load 
    def get(self):
        json_data=open("./libs/defaults.json").read()
        data = json.loads(json_data)
        self.write(data)
    
