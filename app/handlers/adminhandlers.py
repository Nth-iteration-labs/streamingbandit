# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json
import random
import os

from handlers.basehandler import BaseHandler, ExceptionHandler

from db.database import Database
from db.users import Users


class GenerateExperiments(BaseHandler):
    
    def get(self):
        """ Retrieve a list of experiments running on this server
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp                                             |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :returns: A JSON containing exp_id and name pairs.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        user = self.get_current_user()
        if user: 
            db = Database()
            response = db.get_all_experiments(int(user))
            self.write(json.dumps(response))
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

    def post(self):
        """ Create a new experiment
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp                                             |
        | {'name' : NAME, 'getcontext' : CODE, 'getaction' : CODE,           |
        |   'getreward' : CODE, 'setreward' : CODE, 'advice_id' : True,      |
        |   'hourly' : True, 'delta_days' : DELTA_DAYS,                      |
        |   'default_reward' : DEFAULT_REWARD}                               |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param string name: Name of the experiment.
        :param string getcontext: String of python code for get context code.
        :param string getaction: String of python code for get action code.
        :param string getreward: String of python code for get reward code.
        :param string setreward: String of python code for set reward code.
        :param bool hourly: Bool indicating whether the state of Theta should be stored hourly. 
        :param bool advice_id: Bool indicating whether the getAdvice and setReward calls should return an advice_id.
        :param int delta_days: If advice_id is True, supply this to give the number of days that an advice_id should be stored.
        :param dict default_reward: If advice_id is True, supply this to give the default reward for advice_id's that are over their delta_days limit.
        :returns: A JSON of the form:
            { id : the assigned experiment id, 
             name : the name of the experiment (checked for duplicates),
             error : (optional) error message }
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        user = self.get_current_user()
        if user:
            data = tornado.escape.json_decode(self.request.body)
            exp_obj = {}
            exp_obj["user_id"] = int(user)
            exp_obj["name"] = data["name"]
            exp_obj["getContext"] = data["getcontext"]
            exp_obj["getAction"] = data["getaction"]
            exp_obj["getReward"] = data["getreward"]
            exp_obj["setReward"] = data["setreward"]
            exp_obj["hourlyTheta"] = data["hourly"]
            exp_obj["advice_id"] = data["advice_id"]
            if exp_obj["advice_id"] in ["true", "True", "y", "yes"]:
                exp_obj["advice_id"] = True
            if exp_obj["advice_id"] is True:
                exp_obj["delta_days"] = data["delta_days"]
                exp_obj["default_reward"] = data["default_reward"]
        
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
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)


class UpdateExperiment(BaseHandler):
    
    def get(self, exp_id):
        """ Retrieve a specific experiment running on this server
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp/EXP_ID                                      |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param int exp_id: Experiment ID for the experiment that is to be retrieved.
        :returns: A JSON containing all the info for the expriment.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                db = Database()
                response = db.get_one_experiment(exp_id)
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

    def delete(self, exp_id):
        """ Delete an experiment

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp/EXP_ID                                      |
        +--------------------------------------------------------------------+
        
        :requires: A secure cookie obtained by logging in.
        :param int exp_id: The ID of the experiment to be deleted.
        :returns: A JSON showing the deleted experiment.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                db = Database()
                response = db.delete_experiment(exp_id)
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

    def put(self, exp_id):
        """ Edit an experiment
       
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp/EXP_ID                                      |
        | {'name' : NAME, 'getcontext' : CODE, 'getaction' : CODE,           |
        |   'getreward' : CODE, 'setreward' : CODE, 'advice_id' : True,      |
        |   'hourly' : True, 'delta_days' : DELTA_DAYS,                      |
        |   'default_reward' : DEFAULT_REWARD}                               |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param string name: Name of the experiment.
        :param string getcontext: String of python code for get context code.
        :param string getaction: String of python code for get action code.
        :param string getreward: String of python code for get reward code.
        :param string setreward: String of python code for set reward code.
        :param bool hourly: Bool indicating whether the state of Theta should be stored hourly.
        :param bool advice_id: Bool indicating whether the getAdvice and setReward calls should return an advice_id.
        :param int delta_days: If advice_id is True, supply this to give the number of days that an advice_id should be stored.
        :param dict default_reward: If advice_id is True, supply this to give the default reward for advice_id's that are over their delta_days limit.
        :returns: A JSON indicating success.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        user = self.get_current_user()
        if user: 
            if self.validate_user_experiment(exp_id):
                data = tornado.escape.json_decode(self.request.body)
                exp_obj = {}
                exp_obj["user_id"] = int(user)
                exp_obj["name"] = data["name"]
                exp_obj["getContext"] = data["getcontext"]
                exp_obj["getAction"] = data["getaction"]
                exp_obj["getReward"] = data["getreward"]
                exp_obj["setReward"] = data["setreward"]
                exp_obj["hourlyTheta"] = data["hourly"]
                exp_obj["advice_id"] = data["advice_id"]
                if exp_obj["advice_id"] in ["true", "True", "y", "yes"]:
                    exp_obj["advice_id"] = True
                if exp_obj["advice_id"] is True:
                    exp_obj["delta_days"] = data["delta_days"]
                    exp_obj["default_reward"] = data["default_reward"]
            
                db = Database()
                response = {}
                response["id"] = db.edit_experiment(exp_obj, exp_id)
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)
        
class ListDefaults(tornado.web.RequestHandler):
    
    def get(self):
        """ Get the list with default available experiments.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp/defaults                                    |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :returns: A JSON with the default experiments.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_secure_cookie("user"):
            folderdata = os.listdir("./defaults")
            folderdata = [x.replace("_"," ") for x in folderdata]
            folders = dict(enumerate(folderdata))
            self.write(folders)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)
 
       
class GetDefault(tornado.web.RequestHandler):
    
    def get(self, default_id):
        """ Retrieve properties of a default experiment.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp/defaults/DEFAULT_ID                         |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param int default_id: The ID of the default experiment.
        :returns: A JSON containing the experiment properties.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """ 
        if self.get_secure_cookie("user"):
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
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)


class ResetExperiment(BaseHandler):

    def get(self, exp_id):
        """ Reset the theta of an experiment.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/exp/EXP_ID/resetexperiment?key=KEY              |
        | &theta_key=THETA_KEY&theta_value=THETA_VALUE                       |
        +--------------------------------------------------------------------+

        :requires: A secure cookie obtained by logging in.
        :param int exp_id: The experiment ID.
        :param string key: The key of the experiment.
        :param string theta_key (optional): The key for theta used when setting \
        theta in the setReward and getAction code.
        :param string theta_value (optional): The value for theta used when \
        setting theta in the setReward and getAction code.
        :raises 401: If the theta_key or theta_value does not exist or is not valid.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_secure_cookie("user"):
            if self.validate_user_experiment(exp_id):
                key = self.get_argument("key", default = False)
                theta_key = self.get_argument("theta_key", default = False)
                theta_value = self.get_argument("theta_value", default = False)
                __EXP__ = Experiment(exp_id, key)

                status = __EXP__.delete_theta(key = theta_key, value = theta_value)
                if status == True:
                    self.write(json.dumps({'status':'success'}))
                else:
                    raise ExceptionHandler(reason = "Theta_key or theta_value could not be validated.", status_code = 401)
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

class AddUser(BaseHandler):

    def post(self):
        """ Add a user to StreamingBandit.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/user                                            |
        | {'username' : USERNAME, 'password' : PASSWORD}                     |
        +--------------------------------------------------------------------+

        :param string username: The preferred username.
        :param string password: The preferred password.
        :returns: JSON indicating success.
        :raises 400: If user with username already exists.
        """
        users = Users()
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        user_id = users.create_user(username, password)
        if user_id is False:
            raise ExceptionHandler(reason = "User already exists.", status_code = 400)
        else:
            self.write(json.dumps({'status' : 'success'}))
