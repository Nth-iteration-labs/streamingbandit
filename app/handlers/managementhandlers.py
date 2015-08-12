# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import yaml


class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user")


# Management.html (index)
class IndexHandler(BaseHandler):
    
    def get(self):
        """ Renders the HTML of the management interface.
        
        Input: none
        Output: HTML template file management.html
        """
        if not self.current_user:
            self.render("login.html", warning="")
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
        f = open("config.cfg",'r')
        settings = yaml.load(f)
        f.close()
        
        # Check:
        if self.get_argument("name") == settings["admin_pass"]:
            self.set_secure_cookie("user", "VALID")
            self.redirect("management.html")
        else:
            # Add user feedback!
            self.render("login.html", warning="Wrong username")
       
# Logout.html      
class LogOutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("user")
        self.redirect("/", 302)
        