# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import json

from handlers.basehandler import BaseHandler, ExceptionHandler

from core.experiment import Experiment
        
class GetHourlyTheta(BaseHandler):
    
    def get(self, exp_id):
        """ Get a dict of all logged thetas.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/EXP_ID/hourlytheta.json                   |
        +--------------------------------------------------------------------+
        
        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the thetas that are to be retrieved.
        :returns: A list of JSONs of the hourly logged thetas.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                exp = Experiment(exp_id)
                response = exp.get_hourly_theta()
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)
            
class GetCurrentTheta(BaseHandler):
        
    def get(self, exp_id):
        """ Get the current theta.
        
        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/EXP_ID/currenttheta.json                  |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the theta that is to be retrieved.
        :returns: A JSON of the current theta.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                exp = Experiment(exp_id)
                response = exp.get_theta()
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

class GetLog(BaseHandler):

    def get(self, exp_id):
        """ Get all the (manually) logged data.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/EXP_ID/log.json                           |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the logs that are to be retrieved.
        :returns: A list of JSONs of the logs.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                exp = Experiment(exp_id)
                response = exp.get_log_data()
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

class GetActionLog(BaseHandler):

    def get(self, exp_id):
        """ Get all the (automatically) logged getAction data.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/EXP_ID/actionlog.json                     |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the logs that are to be retrieved.
        :returns: A list of JSONs of the logs.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                exp = Experiment(exp_id)
                response = exp.get_getaction_log_data()
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

class GetRewardLog(BaseHandler):

    def get(self, exp_id):
        """ Get all the (automatically) logged setReward data.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/EXP_ID/rewardlog.json                     |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the logs that are to be retrieved.
        :returns: A list of JSONs of the logs.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                exp = Experiment(exp_id)
                response = exp.get_setreward_log_data()
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)

class GetSummary(BaseHandler):

    def get(self, exp_id):
        """ Get a summary, consisting of:
            - The number of getAction calls
            - The date of the last getAction call
            - The number of setReward calls
            - The date of the last setReward call

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/stats/EXP_ID/summary.json                       |
        +--------------------------------------------------------------------+

        :requires: A secure cookie, obtained by logging in.
        :param int exp_id: The experiment ID for the summary that are to be retrieved.
        :returns: A JSON object consisting of the summary.
        :raises 401: If the experiment does not belong to this user or the exp_id is wrong.
        :raises 401: If user is not logged in or if there is no secure cookie available.
        """
        if self.get_current_user():
            if self.validate_user_experiment(exp_id):
                exp = Experiment(exp_id)
                response = exp.get_summary()
                self.write(json.dumps(response))
            else:
                raise ExceptionHandler(reason = "Experiment could not be validated.", status_code = 401)
        else:
            raise ExceptionHandler(reason = "Could not validate user.", status_code = 401)
