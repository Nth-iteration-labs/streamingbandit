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
        
        :returns: A boolean: true if a valid key is provided, false otherwise.
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
        value["exp_id"] = self.exp_id
        self.mongo_db.log_row(value)
        return True
        
    def set_theta(self, thetas, key = None, value = None, name = "_theta"):
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
	#if isinstance(values, __strmBase):
        #    values = values.get_value()	# Not yet tested!
        db_key = "exp:%s:" % (self.exp_id) + name
        if key is not None and value is not None:
            db_key = db_key + ":%s:%s" % (key, value)
        return self.db.set_theta(thetas, db_key)
    
    def get_theta(self, key, value, name = "_theta", all_float = False):
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
        db_key = "exp:%s:" % (self.exp_id) + name
        if key is not None and value is not None:
            db_key = db_key + ":%s:%s" % (key, value)
        if key is not None and value is None:
            all_values = True
        else:
            all_values = False
        return self.db.get_theta(db_key, all_values, all_float)

    def get_log_data(self):
        """ Get all the logged data from the experiment

        :returns dict of dict logs: All the manual logs
        """
        return self.mongo_db.get_log_rows(self.exp_id)
        
    def get_hourly_theta(self):
        """ Get all the hourly logged thetas (if flag is set)

        :returns dict of dict hourly: All the hourly logged thetas
        """
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
        
