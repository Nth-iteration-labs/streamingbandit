# -*- coding: utf-8 -*-
from pymongo import MongoClient
import yaml

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
        self.logs = self.mongo_db['logs']
        self.logs.insert_one(value)
        return True
        
    def log_hourly_theta(self, value):
        """ This function is for logging the hourly theta

        :param dict value: The dictionary that needs to be added in MongoDB
        """
        # Get collection that belongs to this function
        self.theta_logs = self.mongo_db['hourly_theta']
        self.theta_logs.insert_one(value)
        return True
