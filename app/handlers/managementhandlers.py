# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import yaml

from handlers.basehandler import BaseHandler, ExceptionHandler

from db.users import Users

class LogInHandler(BaseHandler):

    def post(self):
        """ Handler to login and retrieve a secure cookie.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/login                                           |
        +--------------------------------------------------------------------+

        :param string username: Experiment ID as specified in the url.
        :param string password: The number of simulation draws.
        :raises 401: If wrong username or password.
        """
        # Get config:
        users = Users()
        
        data = tornado.escape.json_decode(self.request.body)

        # Check:
        username = data["username"]
        password = data["password"]
        user_id = users.get_user_info(username, password)
        if user_id:
            self.set_secure_cookie("user", str(user_id))
            self.finish()
        else:
            # Add user feedback!
            raise ExceptionHandler(reason="Wrong username or password!", status_code=401)
       
class LogOutHandler(BaseHandler):
    
    def get(self):
        """ Handler to logout and clear the set secure cookie.

        +--------------------------------------------------------------------+
        | Example                                                            |
        +====================================================================+
        | http://example.com/logout                                          |
        +--------------------------------------------------------------------+
        """
        # Does this need an exceptionhandler or something?
        self.clear_cookie("user")
        self.finish()
