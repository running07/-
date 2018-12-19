# -*- coding:utf-8 -*-
import sys
sys.path.append('../')
import json
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler
from running_home.utils.session import Session
class BaseHandler(RequestHandler):

    def get_current_user(self):
        self.session = Session(self)
        return self.session.data

    def initialize(self):

        pass

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json ; charset=UTF-8")

    def prepare(self):

        # 解析json数据
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_data = json.loads(self.request.body)

        else:
            self.json_data = {}


    def write_error(self, status_code, **kwargs):
        pass

    def on_finish(self):
        pass

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis




class StaticHandler(StaticFileHandler):
    # 自定义静态文件处理类，在用户获取html时设置_xsrf的cookie
    def __init__(self, *args, **kwargs):
        super(StaticHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
