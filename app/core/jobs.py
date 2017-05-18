# -*- coding: utf-8 -*-
from core.experiment import Experiment
from db.database import Database
from datetime import datetime
from db.mongolog import MongoLog

def log_theta():
    """ For every experiment, if Theta logging flag is set. Log theta from
    redis to mongodb.

    """
    redis_db = Database()
    mongo_db = MongoLog()
    experiment_ids = redis_db.get_experiment_ids()
    for experiment_id in experiment_ids:
        exp = Experiment(experiment_id)
        if exp.properties['hourlyTheta'] == "True":
            theta = exp.get_theta()
            theta['exp_id'] = experiment_id
            mongo_db.log_hourly_theta(theta)
            print("We did it, we stored some stuff!")

def tick():
    print('Tick! The time is: %s' % datetime.now())
