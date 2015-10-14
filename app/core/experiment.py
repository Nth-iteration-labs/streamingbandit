# -*- coding: utf-8 -*-
from db.database import Database
from db.mongolog import MongoLog 
from math import sqrt; from itertools import count, islice
import logging

class Experiment():
         
    
    def __init__(self, exp_id, key = "notUsedForLoopBack"):
        self.db = Database()
        self.mongo_db = MongoLog()
        self.exp_id = exp_id   # sets the experimentID
        self.properties = self.db.get_one_experiment(self.exp_id)
        self.key = key
        self.valid = False     # should be taken from Redis
    
    def is_valid(self):
        """Checks wheter the exp_id and key match for the current experiment.
        
        Input arguments:
        none
            
        Returns:
        A boolean: true if a valid key is provided (a prime), false otherwise.
        """
        key = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "key")
        if key == self.key:
            self.valid = True
        return self.valid
    
    def run_action_code(self, context, action={}):    
        """ Takes getAction code from Redis and executes it
        
        :param dict context: Context is a dictionary with the context for the
        getAction algorithm
        :param dict action: Action is pre-created such that the exec(code)
        function can return an action dict for this function (This is because
        of the behavior of Python.).

        :returns dict action: A dict of action of which the content is
        determined by the getAction code.
        """
        self.action = action
        self.context = context
        code = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "getAction")
        #logging.debug(code)
        exec(code)
        return self.action
        
    def run_reward_code(self, context, action, reward):
        """ Takes setReward code from Redis and executes it

        :param dict context: The context that may be needed for the algorithm.
        :param string action: The action that is needed for the algorith. Is
        actually free of type, but generally a string is used.
        :param int reward: Generally an int, in 0 or 1. Can be of other type,
        but must be specified by used algorithm.

        :raises Python error. Currently the error handling is still in
        development.

        :returns true: If executed correctly.
        """
        self.context = context
        self.action = action
        self.reward = reward
        code = self.db.experiment_properties("exp:%s:properties" % (self.exp_id), "setReward")
        exec(code)
        return True
    
    def log_data(self, value):
        """ Raw logging that is used in the getAction and setReward codes.
        
        ... note: Needs less ambiguity when it comes to the use of the specific
        database. As we will use MongoDB for multiple different logging
        purposes.

        :param dict value: The value that needs to be logged. Since MongoDB is
        used, a dictionary is needed.

        :returns true: If executed correctly.
        """
        self.mongo_db.log_row(value)
        return True
        
    def set_theta(self, values, context = None, action=None, all_action=False, all_context=False, name="theta"):
        """ Set the new theta (parameters) in the database.

        :param dict values: The values of the parameters. Typically a
        dictionary.
        :param dict context: The context that belongs to the theta.
        :param dict action: The action which belongs to the theta.
        :param bool all_action: If true, the database will save the theta based
        on the action given.
        :param bool all_context: If true, the database will save the theta
        based on the context given.
        :param string name: The name of the parameter set.
        """
        key = "exp:%s:" % (self.exp_id) +name
        return self.db.set_theta(values, key, context, action, all_action, all_context)
    
    def get_theta(self, context = None, action=None, all_action=False, all_context=False, all_float=False, name="theta"):
        """ Get the theta (parameters) from the database.

        :param dict context: Context that the theta is saved with.
        :param dict action: Action that the theta is saved with.
        :param bool all_action: Set to true if theta is saved depending on
        action.
        :param bool all_context: Set to true if theta is saved depending on
        context.
        :param bool all_float: Set to true if theta needs to be converted to
        float.
        :param string name: The name of the parameters. Typically theta is
        okay.

        :returns dict theta: A dictionary with the parameter set.
        """
        key = "exp:%s:" % (self.exp_id) +name    
        return self.db.get_theta(key, context, action, all_action, all_context, all_float)
        
    def get_hourly_theta(self):
        return self.mongo_db.get_hourly_theta(self.exp_id)
        
    def debug(self, obj):
        self.context['_debug'] = obj
        
    def is_prime(self, n):
        """ Checks if given number is a prima.

        :params int n
        """
        if n < 2: return False
        for number in islice(count(2), int(sqrt(n)-1)):
            if not n%number:
                return False
        return True
        
