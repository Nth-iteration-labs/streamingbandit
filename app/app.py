#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Imports of external stuff that is needed
import tornado.escape
import tornado.ioloop
import tornado.web
import logging
import os,yaml
import logging.handlers

# import scheduling ingredients
from apscheduler.schedulers.tornado import TornadoScheduler
from core.jobs import *
# import Streampy classes
from handlers import corehandlers
from handlers import adminhandlers
from handlers import statshandlers
from handlers import loginhandlers
from handlers import evalhandlers
from handlers import basehandler

from pymongo import MongoClient
from redis import Redis

import builtins

dir = os.path.dirname(__file__)
f = open(os.path.join(dir,'config.cfg'),'r')
env=os.getenv('env', 'default')
config = yaml.load(f, Loader=yaml.FullLoader)
settings = config[env]
f.close()

########## Logging ##########
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

access_log = logging.getLogger("tornado.access")
access_log.setLevel(settings["log.level"])
app_log = logging.getLogger("myLogger")
app_log.setLevel(settings["log.level"])

ch = logging.StreamHandler()
ch.setLevel(settings["log.console.level"])
ch.setFormatter(formatter)

logHandlerAccess = logging.handlers.RotatingFileHandler(settings["log.access"], maxBytes=4096, backupCount=2)
logHandlerApp = logging.handlers.RotatingFileHandler(settings["log.app"], maxBytes=4096, backupCount=2)

logHandlerAccess.setFormatter(formatter)
logHandlerApp.setFormatter(formatter)

access_log.addHandler(logHandlerAccess)
access_log.addHandler(ch)
app_log.addHandler(logHandlerApp)
app_log.addHandler(ch)
   
app_log.info("Starting application {0}".format( settings["listen.port"]))

########## Handlers ##########
urls = [
    # Core API
    (r"(?i)/getaction/(?P<exp_id>\w+)", corehandlers.ActionHandler),
    (r"(?i)/setreward/(?P<exp_id>\w+)", corehandlers.RewardHandler),

    # Adminstration API
    (r"(?i)/exp", adminhandlers.GenerateExperiments),

    (r"(?i)/exp/defaults", adminhandlers.ListDefaults),

    (r"(?i)/exp/defaults/(?P<default_id>\w+)", adminhandlers.GetDefault),

    (r"(?i)/exp/(?P<exp_id>\w+)", adminhandlers.UpdateExperiment),

    (r"(?i)/exp/(?P<exp_id>\w+)/resetexperiment", adminhandlers.ResetExperiment),

    (r"(?i)/user", adminhandlers.AddUser),

    # Statistics API
    (r"(?i)/stats/(?P<exp_id>\w+)/currenttheta", statshandlers.GetCurrentTheta),
    (r"(?i)/stats/(?P<exp_id>\w+)/hourlytheta", statshandlers.GetHourlyTheta),
    (r"(?i)/stats/(?P<exp_id>\w+)/log", statshandlers.GetLog),
    (r"(?i)/stats/(?P<exp_id>\w+)/actionlog", statshandlers.GetActionLog),
    (r"(?i)/stats/(?P<exp_id>\w+)/rewardlog", statshandlers.GetRewardLog),
    (r"(?i)/stats/(?P<exp_id>\w+)/simulationlog", statshandlers.GetSimulationLog),
    (r"(?i)/stats/(?P<exp_id>\w+)/summary", statshandlers.GetSummary),

    # Login API
    (r"(?i)/login", loginhandlers.LogInHandler),
    (r"(?i)/logout", loginhandlers.LogOutHandler),
               
    # Simulation API
    (r"(?i)/eval/(?P<exp_id>\w+)/simulate", evalhandlers.Simulate),

    # Index
    (r"(?i)/", basehandler.IndexHandler)
]

# Instantiate DB clients
redis_server = Redis(settings['redis_ip'], settings['redis_port'], decode_responses = True)
mongo_client = MongoClient(settings['mongo_ip'], settings['mongo_port'])

tornado_config = dict({
    "template_path": os.path.join(os.path.dirname(__file__),"templates"),
    "debug": True,   # Should get from config?
    "cookie_secret":"12",
    "default_handler_class":basehandler.BaseHandler,
    "redis_server" : redis_server,
    "mongo_client" : mongo_client
})

builtins.tornado_config = tornado_config

application = tornado.web.Application(urls,**tornado_config)

def main():
    # Use the above instantiated scheduler
    # Set Tornado Scheduler
    scheduler = TornadoScheduler()
    # Use the imported jobs, every 60 minutes
    scheduler.add_job(log_theta, 'interval', minutes=60, misfire_grace_time=3600)
    scheduler.add_job(advice_time_out, 'interval', minutes=60, misfire_grace_time=3600)
    scheduler.start()
    application.listen(settings["listen.port"])
    tornado.ioloop.IOLoop.instance().start()

# Starting Server:
if __name__ == "__main__":
    main()
