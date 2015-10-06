# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from core.experiment import Experiment
        
class GetHourlyTheta(tornado.web.RequestHandler):
    
    def get(self, exp_id):
        """ Get a dict of all logged thetas
        
        :param int exp_id: The experiment ID for the thetas that are to be retrieved.
        
        :returns dict dict hourly: Returns a dict of dicts of hourly thetas.
        """
        if self.get_secure_cookie("user"):
            exp = Experiment(exp_id)
            response = exp.get_hourly_theta()
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")
            
class GetCurrentTheta(tornado.web.RequestHandler):
        
    def get(self, exp_id):
        """ Get the current theta for experiment id exp_id
        
        :param int exp_id: The specific experiment id
        :returns dict theta: The current theta
        """
        if self.get_secure_cookie("user"):
            exp = Experiment(exp_id)
            response = exp.get_theta(exp_id)
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")