# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

import builtins

class Advice:

    def __init__(self):
        self.mongo_client = builtins.tornado_config['mongo_client']
        self.mongo_db = self.mongo_client['advices']
        self.advices = self.mongo_db['advices']

    def log_advice(self, action, context):
        context['date'] = datetime.utcnow()
        context['action'] = action
        context['exp_id'] = exp_id
        advice_id = self.advices.insert_one(context)
        return str(advice_id.inserted_id)

    def get_advice(self, advice_id):
        context = self.advices.find_one_and_delete({'_id' : ObjectId(advice_id), 'exp_id': exp_id})
        if context is not None:
            del context['_id']
            del context['date']
            del context['exp_id']
            action = context['action']
            del context['action']
            return {'context': context, 'action': action}
        else:
            return False
