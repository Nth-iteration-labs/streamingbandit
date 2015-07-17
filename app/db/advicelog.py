# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
import yaml
from datetime import datetime

class Advice:

    def __init__(self):
        f = open("config.cfg",'r')
        settings = yaml.load(f)
        self.mongo_client = MongoClient(settings['mongo_ip'], settings['mongo_port'])
        self.mongo_db = self.mongo_client['advice_database']
        self.advices = self.mongo_db['advices']
        self.logs = self.mongo_db['logs']
        f.close()
        
    def log_advice(self, context, action):
        context['date'] = datetime.utcnow()
        context['action'] = action
        advice_id = self.advices.insert_one(context)
        return str(advice_id.inserted_id)
        
    def get_advice(self, advice_id):
        context = self.advices.find_one_and_delete({'_id' : ObjectId(advice_id)})
        if context is not None:
            del context['_id']
            del context['date']
            action = context['action']
            del context['action']
            return {'context':context, 'action':action}
        else:
            return False
            
    def log_row(self, value):
        self.logs.insert_one(value)
        return True
        
