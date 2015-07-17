# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    
    def get(self):
        """ Renders the HTML of the management interface.
        
        Input: none
        Output: HTML template file management.html
        """
        self.render("management.html")

