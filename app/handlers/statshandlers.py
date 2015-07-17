# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web


class WorkInProgress(tornado.web.RequestHandler):
    
    def get (self):
        self.write("The statistics are still work in progress..")
