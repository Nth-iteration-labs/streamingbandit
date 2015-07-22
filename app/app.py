# -*- coding: utf-8 -*-
# Imports of external stuff
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import json,os

# inport Streampy classes
from handlers import corehandlers
from handlers import docshandlers
from handlers import adminhandlers
from handlers import statshandlers
from handlers import managementhandlers

urls = [

    # static pages (index + API reference)
    (r"/", docshandlers.IndexHandler),
    (r"(?i)/reference.html", docshandlers.ReferenceHandler),
    # management interface front-end
    (r"(?i)/management.html", managementhandlers.IndexHandler),

    # action and reward handler (core)
    (r"(?i)/([0-9]+)/getaction.json", corehandlers.ActionHandler),
    (r"(?i)/([0-9]+)/setreward.json", corehandlers.RewardHandler),
     
    # admin / management REST api (REST api for administration of experiments)
    (r"(?i)/admin/exp/defaults.json", adminhandlers.LoadDefaults),
    (r"(?i)/admin/exp/add.json", adminhandlers.AddExperiment),
    (r"(?i)/admin/exp/list.json", adminhandlers.GetListOfExperiments),
    (r"(?i)/admin/exp/([0-9]+)/get.json", adminhandlers.GetExperiment),
    (r"(?i)/admin/exp/([0-9]+)/edit.json", adminhandlers.EditExperiment),
    
    # analytics REST api (REST api for stats / logs)
    (r"(?i)/stats/([0-9]+)/getcurrenttheta.json", statshandlers.WorkInProgress),
    (r"(?i)/stats/([0-9]+)/gethourlytheta.json", statshandlers.WorkInProgress),
               
            
]

settings = dict({
    "template_path": os.path.join(os.path.dirname(__file__),"templates"),
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "debug": True
})

application = tornado.web.Application(urls,**settings)

def main():
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

# Starting Server:
if __name__ == "__main__":
    main()

# This one works:
# http://localhost:8080/1/getAction.json?context={}&key=12321
# http://localhost:8080/1/setReward.json?key=12321&reward=1&action={}
