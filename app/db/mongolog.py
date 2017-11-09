# -*- coding: utf-8 -*-
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import gridfs
import ast
import json

import builtins

class MongoLog:
    """ A class to simply log stuff to MongoDB.
    
    ...note: Watch out with the use of this
    class in different settings. If you use this for different types of
    logging, things will get very messy as everything will be in the same
    database.
    """
    def __init__(self):
        self.mongo_client = builtins.tornado_config['mongo_client']
            
    def log_row(self, value):
        """ Simply log the value that is given in the logs database.

        :param dict value: A dictionary that is to be saved.
        """
        # Get collection that belongs to this function.
        self.logs_db = self.mongo_client['logs']
        self.logs = self.logs_db[str(value['exp_id'])]
        self.logs.insert_one(value)
        return True

    def get_log_rows(self, exp_id, limit):
        """ Retrieve all the logged rows for a certain experiment.

        :param int exp_id: The specified experiment.
        :returns list dict logs: All the logs for that belong to the experiment.
        """
        self.logs_db = self.mongo_client['logs']
        self.logs = self.logs_db[str(exp_id)]
        self.log_rows = []
        for row in self.logs.find({}, {'_id': False}).sort('_id', DESCENDING).limit(limit):
            self.log_rows.append(row)
        return self.log_rows

    def log_simulation(self, exp_id, sim_data):
        """ Log all the interactions of one simulation run.

        :param int exp_id: The specified experiment.
        :param dict sim_data: The full simluation run as a dict of dicts.
        :returns True: If executed correctly.
        """
        self.sim_db = self.mongo_client['simulations']
        self.fs = gridfs.GridFS(self.sim_db)
        self.fs.put(json.dumps(sim_data).encode("UTF-8"), filename = str(exp_id))
        return True

    def get_simulation_log(self, exp_id, limit):
        """ Return all the logged simulation data
        
        :param int exp_id: The specified experiment.
        :returns list of dicts logs: All the simulation runs for that experiment.
        """
        self.sim_db = self.mongo_client['simulations']
        self.fs = gridfs.GridFS(self.sim_db)
        self.sim_log_rows = []
        for row in self.fs.find({"filename" : str(exp_id)}).sort("uploadDate", -1).limit(limit):
            self.sim_log_rows.append(json.loads(row.read().decode("UTF-8")))
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
        
    def get_hourly_theta(self, exp_id, limit):
        """ This function is for retrieving all the hourly thetas of an experiment
        
        :param int exp_id: The specified experiment
        :returns list dict hourly: All the hourly thetas that belong to this experiment.
        """
        self.theta_logs_db = self.mongo_client['hourly_theta']
        self.theta_logs = self.theta_logs_db[str('exp_id')]
        self.thetas = []
        for theta in self.theta_logs.find({}, {'_id': False}).sort('_id', DESCENDING).limit(limit):
            self.thetas.append(theta)
        return self.thetas

    def log_getaction(self, exp_id, context, action):
        # Use MongoDB database called getaction and per exp_id 1 collection
        self.getaction_db = self.mongo_client['getaction']
        self.getaction_logs = self.getaction_db[str(exp_id)]
        self.getaction_logs.insert_one({"context":context,"action":action,"date":datetime.utcnow().isoformat()})
        return True
    
    def get_getaction_log(self, exp_id, limit):
        # Use mongoDB database called getaction and per exp_id 1 collection
        self.getaction_db = self.mongo_client['getaction']
        self.getaction_logs = self.getaction_db[str(exp_id)]
        self.getactions = []
        cursor = self.getaction_logs.find({}, {'_id': False}).sort('_id', DESCENDING).limit(limit)
        for document in cursor:
            self.getactions.append(document)
        return self.getactions

    def log_setreward(self, exp_id, context, action, reward):
        # Use MongoDB database called setreward and per exp_id 1 collection
        self.setreward_db = self.mongo_client['setreward']
        self.setreward_logs = self.setreward_db[str(exp_id)]
        self.setreward_logs.insert_one({"context":context,"action":action,"reward":reward,"date":datetime.utcnow().isoformat()})
        return True

    def get_setreward_log(self, exp_id, limit):
        # Use mongoDB database called setreward and per exp_id 1 collection
        self.setreward_db = self.mongo_client['setreward']
        self.setreward_logs = self.setreward_db[str(exp_id)]
        self.setrewards = []
        cursor = self.setreward_logs.find({}, {'_id': False}).sort('_id', DESCENDING).limit(limit)
        for document in cursor:
            self.setrewards.append(document)
        return self.setrewards

    def log_deleted_experiment(self, obj):
        self.archive = self.mongo_client['archive']
        self.archive_log = self.archive['deleted_experiments']
        self.archive_log.insert_one(obj)
        return True
