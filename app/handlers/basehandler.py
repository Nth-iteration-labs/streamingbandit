# -* coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
import yaml
import json
import traceback

from db.database import Database

class ExceptionHandler(tornado.web.HTTPError):

    pass

class BaseHandler(tornado.web.RequestHandler):

    def get(self):
        raise ExceptionHandler(reason = "Not found.", status_code = 404)
    
    def delete(self):
        raise ExceptionHandler(reason = "Not found.", status_code = 404)

    def post(self):
        raise ExceptionHandler(reason = "Not found.", status_code = 404)

    def put(self):
        raise ExceptionHandler(reason = "Not found.", status_code = 404)

    def options(self, *args, **kwargs):
        self.set_status(204)

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Headers', 'origin, content-type, accept, authorization, x-total-count, content-range')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def validate_user_experiment(self, exp_id):
        db = Database()
        user_id = int(self.get_current_user())
        properties = db.get_one_experiment(exp_id)
        if not properties:
            return False
        if int(properties['user_id']) == user_id:
            return True
        else:
            return False
    
    def write_error(self, status_code, **kwargs): 
        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)
            self.finish(json.dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                    'traceback': lines,
                }
            }))
        else:
            self.finish(json.dumps({
                'error': {
                    'code': status_code,
                    'message': self._reason,
                }
            }))

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")
