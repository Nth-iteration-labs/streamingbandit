# -*- coding: utf-8 -*-
from core.experiment import Experiment
from db.database import Database

def log_theta():
    """ For every experiment, if Theta logging flag is set. Log theta from
    redis to mongodb.

    """
    redis_db = Database()
    experiment_ids = redis_db.get_experiment_ids()
    for experiment_id in experiment_ids:
        exp = Experiment(experiment_id)
        exp.log_data(exp.get_theta())
