# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import yaml

from handlers.basehandler import BaseHandler

from db.users import Users

# Management.html (index)
class IndexHandler(BaseHandler):
    
    def get(self):
        """ Renders the HTML of the management interface.
        
        Input: none
        Output: HTML template file management.html
        """
        if not self.current_user:
            self.redirect("/login.html", 302)
            return
        else:
            self.render("management.html")
            return


# Login.html
class LogInHandler(BaseHandler):
    
    def get(self):
        self.render("login.html", warning="")

    def post(self):
        # Get config:
        users = Users()
        
        # Check:
        username = self.get_argument("username")
        password = self.get_argument("password")
        user_id = users.get_user_info(username, password)
        if user_id:
            self.set_secure_cookie("user", str(user_id))
            self.redirect("management.html")
        else:
            # Add user feedback!
            self.render("login.html", warning="Wrong username or password!")
       
# Logout.html      
class LogOutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("user")
        self.redirect("/", 302)
        
