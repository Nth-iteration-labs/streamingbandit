# -*- coding: utf-8 -*-
from pymongo import MongoClient
import yaml

class Advice:

    def __init__(self):
        f = open("config.cfg",'r')
        settings = yaml.load(f)
        self.mongo_client = MongoClient(settings['mongo_ip'], settings['mongo_port'])
        self.mongo_db = self.mongo_client['logs']
        self.logs = self.mongo_db['logs']

        f.close()
            
    def log_row(self, value):
        self.logs.insert_one(value)
        return True
        
