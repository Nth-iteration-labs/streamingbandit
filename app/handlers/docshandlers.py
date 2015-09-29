# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("index.html")

class ReferenceHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("reference.html")
