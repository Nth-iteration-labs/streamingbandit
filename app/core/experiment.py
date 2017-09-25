# -*- coding: utf-8 -*-
from db.database import Database
from db.mongolog import MongoLog 
from db.advice import Advice
from math import sqrt; from itertools import count, islice
import logging

class Experiment():
    """ Class that organizes experiments.
    
    :var int exp_id: The exp_id that is tied to the experiment and the \
    database.
    """
    def __init__(self, exp_id, key = "notUsedForLoopBack"):
        self.db = Database()
        self.mongo_db = MongoLog()
        self.advice_db = Advice()
        self.exp_id = exp_id   # sets the experimentID
        self.properties = self.db.get_one_experiment(self.exp_id)
        self.key = key
        self.valid = False     # should be taken from Redis
    
    def is_valid(self):
        """Checks wheter the exp_id and key match for the current experiment.
        
        :returns: A boolean: true if a valid key is provided, false otherwise.
        """
        key = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "key")
        if key == self.key:
            self.valid = True
        return self.valid

    def run_context_code(self, context = {}):
        """
        """
        self.context = context
        code = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "get_context")
        exec(code)
        return self.context

    def run_action_code(self, context, action = {}):    
        """ Takes get_action code from Redis and executes it
        
        :param dict context: Context is a dictionary with the context for the \
        getAction algorithm
        :param dict action: Action is pre-created such that the exec(code) \
        function can return an action dict for this function (This is because \
        of the behavior of Python.).

        :returns: A dict of action of which the content is \
        determined by the get_action code.
        """
        self.action = action
        self.context = context
        code = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "get_action")
        exec(code)
        return self.action

    def run_get_reward_code(self, context, action, reward = {}):
        """
        """
        self.action = action
        self.context = context
        self.reward = reward
        code = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "get_reward")
        exec(code)
        return self.reward
        
    def run_reward_code(self, context, action, reward):
        """ Takes set_reward code from Redis and executes it

        :param dict context: The context that may be needed for the algorithm.
        :param string action: The action that is needed for the algorith. Is \
        actually free of type, but generally a string is used.
        :param int reward: Generally an int, in 0 or 1. Can be of other type, \
        but must be specified by used algorithm.
        :returns True: If executed correctly.
        """
        self.context = context
        self.action = action
        self.reward = reward
        code = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "set_reward")
        exec(code)
        return True
    
    def log_data(self, value):
        """ Manual logging that is used in the get_action and set_reward codes.

        :param dict value: The value that needs to be logged. Since MongoDB is \
                used, a dictionary is needed.
        :returns True: If executed correctly.
        """
        value["exp_id"] = self.exp_id
        self.mongo_db.log_row(value)
        return True

    def log_simulation_data(self, data):
        """ Log one simulation loop
        
        :param dict data: Dict of dicts with all interactions
        :returns True: If executed correctly
        """
        self.mongo_db.log_simulation(exp_id, data)
        return True

    def log_getaction_data(self, context, action):
        """ Logging for all the get_action calls

        :param dict data: Dict that contains action, and context
        :returns: True if executed correctly
        """
        self.mongo_db.log_getaction(self.exp_id, context, action)
        return True

    def log_setreward_data(self, context, action, reward):
        """ Logging for all the set_reward calls

        :param dict data: Dict that contains action, context and reward
        :returns True: If executed correctly
        """
        self.mongo_db.log_setreward(self.exp_id, context, action, reward)
        return True
        
    def set_theta(self, thetas, key = None, value = None, name = "_theta"):
        """ Set the new theta (parameters) in the database.

        :param dict thetas: The thetas that will eb stored. Typically a \
        dictionary or a class of base.py. The function will check if it is a \
        class and whether it has a get_dict function. It is okay to give a \
        class with these conditions - it will call the get_dict function and \
        store the dictionary.
        :param string key: The key with which the theta will be associated. If \
        only a key is given, all the thetas that belong to that key will be \
        returned. Typically a key distinguishes experiments from each other.
        :param string value: The value with which the theta will be assiocated. \
        Typically the value distinguishes the different versions within an \
        experiment. If no value is given, all thetas belonging to the \
        key/experiment will be returned.
        :param string name: The name of the parameter set.
        """
        try:
           check_dict = getattr(thetas, "get_dict")
        except AttributeError:
           check_dict = False
        if check_dict and callable(check_dict):
            thetas = thetas.get_dict()
        db_key = "exp:%s:" % (self.exp_id) + name
        if key is not None and value is not None:
            db_key = db_key + ":%s:%s" % (key, value)
        return self.db.set_theta(thetas, db_key)
    
    def get_theta(self, key = None, value = None, name = "_theta", all_float = False):
        """ Get the theta (parameters) from the database.

        :param string key: The key with which the theta will be associated. If \
        only a key is given, all the thetas that belong to that key will be \
        returned. Typically a key distinguishes experiments from each other. \
        :param string value: The value with which the theta will be assiocated. \
        Typically the value distinguishes the different versions within an \
        experiment. If no value is given, all thetas belonging to the \
        key/experiment will be returned.
        :param string name: The name of the parameters. Typically theta is \
        okay.
        :param bool all_float: If all_float is True, it will try to convert \
        every value within the theta to a float.

        :returns: A dictionary with the parameter set.
        """
        db_key = "exp:%s:" % (self.exp_id) + name
        all_values = False
        if key is not None and value is not None:
            db_key = db_key + ":%s:%s" % (key, value)
        elif key is not None and value is None:
            db_key = db_key + ":%s" % (key)
            all_values = True
        elif key is None and value is None:
            all_values = True
        return self.db.get_theta(db_key, all_values, all_float)

    def delete_theta(self, key = None, value = None, name = "_theta"):
        db_key = "exp:%s:" % (self.exp_id) + name
        if key is not None and value is not None:
            db_key = db_key + ":%s:%s" % (key, value)
        return self.db.delete_theta(db_key)

    def get_log_data(self):
        """ Get all the logged data from the experiment

        :returns dict logs: Dict of dict of all the manual logs
        """
        return self.mongo_db.get_log_rows(self.exp_id)

    def get_log_simulation_data(self):
        """ Get all the logged data for the simulations of this experiment
        
        :returns dict logs: List of dict of dicts of the simulations
        """
        return self.mongo_db.get_log_simulation(exp_id)

    def get_getaction_log_data(self):
        """ Get all the automatically logged get_action data from the experiment.

        :returns dict logs: Dict of dict of all the get_action logs
        """
        return self.mongo_db.get_getaction_log(self.exp_id)

    def get_setreward_log_data(self):
        """ Get all the automatically logged set_reward data from the experiment.

        :returns dict logs: Dict of dict of all the set_reward logs
        """
        return self.mongo_db.get_setreward_log(self.exp_id)

    def get_summary(self):
        """ Get a summary, consisting of:
            - The number of get_action calls
            - The date of the last get_action call
            - The number of set_reward calls
            - The date of the last set_reward call
        
        :returns dict of dict summary: The complete summary.
        """
        summary = {}
        getactioncalls = self.get_getaction_log_data()
        seq = [x['date'] for x in getactioncalls]
        summary['last_added_get_action'] = max(seq)
        summary['get_action_calls'] = len(getactioncalls)
        setrewardcalls = self.get_setreward_log_data()
        seq = [x['date'] for x in setrewardcalls]
        summary['last_added_set_reward'] = max(seq)
        summary['set_reward_calls'] = len(setrewardcalls)
        return summary
        
    def get_hourly_theta(self):
        """ Get all the hourly logged thetas (if flag is set)

        :returns dict of dict hourly: All the hourly logged thetas
        """
        return self.mongo_db.get_hourly_theta(self.exp_id)
    
    def gen_advice_id(self, action, context):
        return self.advice_db.log_advice(action, context)
    
    def get_by_advice_id(self, _id):
        return self.advice_db.get_advice(_id)

    def debug(self, obj):
        self.context['_debug'] = obj
