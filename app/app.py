#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Imports of external stuff that is needed
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import json,os,yaml
import logging
import logging.handlers

# import scheduling ingredients
from apscheduler.schedulers.tornado import TornadoScheduler
from core.jobs import *
# import Streampy classes
from handlers import corehandlers
from handlers import adminhandlers
from handlers import statshandlers
from handlers import managementhandlers
from handlers import evalhandlers

dir = os.path.dirname(__file__)
f = open(os.path.join(dir,'config.cfg'),'r')
settings = yaml.load(f)
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
    (r"(?i)/(?P<exp_id>\w+)/getaction.json", corehandlers.ActionHandler),
    (r"(?i)/(?P<exp_id>\w+)/setreward.json", corehandlers.RewardHandler),

    # Adminstration API
    (r"(?i)/admin/exp/add.json", adminhandlers.AddExperiment),
    (r"(?i)/admin/exp/list.json", adminhandlers.GetListOfExperiments),
    (r"(?i)/admin/exp/defaults.json", adminhandlers.ListDefaults),
    (r"(?i)/admin/exp/default/(?P<default_id>\w+)/get.json", adminhandlers.GetDefault),
    (r"(?i)/admin/exp/(?P<exp_id>\w+)/get.json", adminhandlers.GetExperiment),
    (r"(?i)/admin/exp/(?P<exp_id>\w+)/delete.json", adminhandlers.DeleteExperiment),
    (r"(?i)/admin/exp/(?P<exp_id>\w+)/edit.json", adminhandlers.EditExperiment),
    (r"(?i)/admin/exp/(?P<exp_id>\w+)/resetexperiment", adminhandlers.ResetExperiment),
    (r"(?i)/admin/user/add.json", adminhandlers.AddUser),

    # Statistics API
    (r"(?i)/stats/(?P<exp_id>\w+)/currenttheta.json", statshandlers.GetCurrentTheta),
    (r"(?i)/stats/(?P<exp_id>\w+)/hourlytheta.json", statshandlers.GetHourlyTheta),
    (r"(?i)/stats/(?P<exp_id>\w+)/log.json", statshandlers.GetLog),
    (r"(?i)/stats/(?P<exp_id>\w+)/rewardlog.json", statshandlers.GetRewardLog),
    #(r"(?i)/stats/(?P<exp_id>\w+)/summary.json", statshandlers.GetSummary),

    # Login API
    (r"(?i)/login.secure", managementhandlers.LogInHandler),
    (r"(?i)/logout", managementhandlers.LogOutHandler),
               
    # Simulation API
    (r"(?i)/eval/(?P<exp_id>\w+)/simulate", evalhandlers.Simulate),
]

tornadoConfig = dict({
    "template_path": os.path.join(os.path.dirname(__file__),"templates"),
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "debug": True,   # Should get from config?
    "cookie_secret":"12"
})

application = tornado.web.Application(urls,**tornadoConfig)

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
