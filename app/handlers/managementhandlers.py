# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import yaml

from handlers.basehandler import BaseHandler

from db.users import Users

class LogInHandler(BaseHandler):

    def post(self):
        # Get config:
        users = Users()
        
        # Check:
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_id = users.get_user_info(username, password)
        if user_id:
            self.set_secure_cookie("user", str(user_id))
        else:
            # Add user feedback!
            self.write("Wrong username or password!")
       
class LogOutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("user")
