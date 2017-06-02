# -*- coding: utf-8 -*-
from core.experiment import Experiment
from db.database import Database
from datetime import datetime, timedelta
from db.mongolog import MongoLog
from db.advice import Advice

def log_theta():
    """ For every experiment, if Theta logging flag is set. Log theta from
    redis to mongodb.

    """
    redis_db = Database()
    mongo_db = MongoLog()
    experiment_ids = redis_db.get_experiment_ids()
    for experiment_id in experiment_ids:
        exp = Experiment(experiment_id)
        if exp.properties["hourlyTheta"] == "True":
            theta = exp.get_theta()
            theta["exp_id"] = experiment_id
            mongo_db.log_hourly_theta(theta)

def advice_time_out():
    """ For every experiment, if the advice_id flag is set, we want to
    check whether certain advice_id's have timed out according to the
    experiment's own settings.
    """
    redis_db = Database()
    advice_db = Advice()
    experiment_ids = redis_db.get_experiment_ids()
    for experiment_id in experiment_ids:
        # Check experiment properties
        exp = Experiment(experiment_id)
        if exp.properties["advice_id"] == "True":
            # Get all the advices for this experiment
            # Check whether or not the date has exceeded the time-out rate
            delta_days = exp.properties["delta_days"]
            advices_retrieved = advice_db.advices.find({"date":{"$lt":datetime.utcnow()-timedelta(days=delta_days)}})
            for adv in advices_retrieved:
                log = exp.get_by_advice_id(str(adv["_id"]))
                reward = exp.properties["default_reward"]
                exp.run_reward_code(adv["context"],adv["action"],reward)
