# -*- coding: utf-8 -*-
from pymongo import MongoClient, ASCENDING, DESCENDING
import yaml
from datetime import datetime

class MongoLog:
    """ A class to simply log stuff to MongoDB.
    
    ...note: Watch out with the use of this
    class in different settings. If you use this for different types of
    logging, things will get very messy as everything will be in the same
    database.
    """
    def __init__(self):
        f = open("config.cfg",'r')
        settings = yaml.load(f)
        self.mongo_client = MongoClient(settings['mongo_ip'], settings['mongo_port'])
        self.mongo_db = self.mongo_client['logs']

        f.close()
            
    def log_row(self, value):
        """ Simply log the value that is given in the logs database.

        :param dict value: A dictionary that is to be saved.
        """
        # Get collection that belongs to this function.
        self.logs_db = self.mongo_client['logs']
        self.logs = self.logs_db[str(value['exp_id'])]
        self.logs.insert_one(value)
        return True

    def get_log_rows(self, exp_id):
        """ Retrieve all the logged rows for a certain experiment.

        :param int exp_id: The specified experiment.
        :returns list dict logs: All the logs for that belong to the experiment.
        """
        self.logs_db = self.mongo_client['logs']
        self.logs = self.logs_db[str(exp_id)]
        self.log_rows = []
        for row in self.logs.find({}, {'_id': False}).sort('_id', ASCENDING):
            self.log_rows.append(row)
        return self.log_rows

    def log_simulation(self, exp_id, sim_data):
        """ Log all the interactions of one simulation run.

        :param int exp_id: The specified experiment.
        :param dict sim_data: The full simluation run as a dict of dicts.
        :returns True: If executed correctly.
        """
        self.sim_db = self.mongo_client['simulations']
        self.sim_logs = self.sim_db[str(exp_id)]
        self.sim_logs.insert_one(sim_data)
        return True

    def get_log_simulation(self, exp_id):
        """ Return all the logged simulation data
        
        :param int exp_id: The specified experiment.
        :returns list of dicts logs: All the simulation runs for that experiment.
        """
        self.sim_db = self.mongo_client['simulations']
        self.sim_logs = self.sim_db[str(exp_id)]
        self.sim_log_rows = []
        for row in self.sim_logs.find({}, {'_id': False}).sort('_id', ASCENDING):
            self.sim_low_rows.append(row)
        return self.sim_log_rows
        
    def log_hourly_theta(self, value):
        """ This function is for logging the hourly theta

        :param dict value: The dictionary that needs to be added in MongoDB
        """
        # Get collection that belongs to this function
        self.theta_logs_db = self.mongo_client['hourly_theta']
        self.theta_logs = self.theta_logs_db[str(value['exp_id'])]
        self.theta_logs.insert_one(value)
        return True
        
    def get_hourly_theta(self, exp_id):
        """ This function is for retrieving all the hourly thetas of an experiment
        
        :param int exp_id: The specified experiment
        :returns list dict hourly: All the hourly thetas that belong to this experiment.
        """
        self.theta_logs_db = self.mongo_client['hourly_theta']
        self.theta_logs = self.theta_logs_db[str('exp_id')]
        self.thetas = []
        for theta in self.theta_logs.find({}, {'_id': False}).sort('_id', ASCENDING):
            self.thetas.append(theta)
        return self.thetas

    def log_getaction(self, exp_id, context, action):
        # Use MongoDB database called getaction and per exp_id 1 collection
        self.getaction_db = self.mongo_client['getaction']
        self.getaction_logs = self.getaction_db[str(exp_id)]
        self.getaction_logs.insert_one({"context":context,"action":action,"date":datetime.utcnow().isoformat()})
        return True
    
    def get_getaction_log(self, exp_id):
        # Use mongoDB database called getaction and per exp_id 1 collection
        self.getaction_db = self.mongo_client['getaction']
        self.getaction_logs = self.getaction_db[str(exp_id)]
        self.getactions = []
        cursor = self.getaction_logs.find({})
        for document in cursor:
            self.getactions.append(document)
        return self.getactions

    def log_setreward(self, exp_id, context, action, reward):
        # Use MongoDB database called setreward and per exp_id 1 collection
        self.setreward_db = self.mongo_client['setreward']
        self.setreward_logs = self.setreward_db[str(exp_id)]
        self.setreward_logs.insert_one({"context":context,"action":action,"reward":reward,"date":datetime.utcnow().isoformat()})
        return True

    def get_setreward_log(self, exp_id):
        # Use mongoDB database called setreward and per exp_id 1 collection
        self.setreward_db = self.mongo_client['setreward']
        self.setreward_logs = self.setreward_db[str(exp_id)]
        self.setrewards = []
        cursor = self.setreward_logs.find({})
        for document in cursor:
            self.setrewards.append(document)
        return self.setrewards
