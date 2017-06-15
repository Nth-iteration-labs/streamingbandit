# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import yaml

from db.database import Database

class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def validate_user_experiment(self, exp_id):
        db = Database()
        user_id = int(self.get_current_user())
        properties = db.get_one_experiment(exp_id)
        if int(properties['user_id']) == user_id:
            return True
        else:
            return False
