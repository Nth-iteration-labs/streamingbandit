# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from core.experiment import Experiment
        
class GetHourlyTheta(tornado.web.RequestHandler):
    
    def get(self, exp_id):
        """ Get a dict of all logged thetas

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/1/getHourlyTheta.json                     |
        +--------------------------------------------------------------------+
        
        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the thetas that are to be retrieved.
        :returns: A JSON of JSONs of hourly logged thetas.
        :raises: AUTH_ERROR if there is no secure cookie available.
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
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/1/getCurrentTheta.json                    |
        +--------------------------------------------------------------------+
        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the theta that is to be retrieved.
        :returns: A JSON of current theta.
        :raises: AUTH_ERROR if there is no secure cookie available.
        """
        if self.get_secure_cookie("user"):
            exp = Experiment(exp_id)
            response = exp.get_theta()
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")

class GetLog(tornado.web.RequestHandler):

    def get(self, exp_id):
        """ Get all the (manually) logged data for experiment exp_id.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/1/getLog.json                             |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the logs that are to be retrieved.
        :returns: A JSON of JSONs of the logs.
        :raises: AUTH_ERROR if there is no secure cookie available.
        """
        if self.get_secure_cookie("user"):
            exp = Experiment(exp_id)
            response = exp.get_log_data()
            self.write(json.dumps(response))
        else:
            self.write("AUTH_ERROR")
