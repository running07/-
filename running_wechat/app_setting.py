# -*- coding:utf-8 -*-
import tornado.web
import torndb
import os


class Application(tornado.web.Application):
    def __init__(self, handlers):

        # handlers 供子类重写
        handlers = handlers

        # setting文件
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'statics'),
            static_url_prefix='/running/',
            log_path=os.path.join(os.path.dirname(__file__), 'logs/log'),

            # cookie_secret='JArhbLQvSYi6zQUH4JGQUwsicJsZvkdltUIFZ8ebl5Q=',
            # xsrf_cookies=True,
            login_url='/login',
            debug=True,
            autoescape=None,

        )

        super(Application, self).__init__(handlers, **settings)

        # 创建一个全局mysql连接实例供handler使用
        self.db = torndb.Connection(
            host='192.168.0.120',
            # database='tornado_running',
            database='shopping',
            user='root',
            password='mysql'
        )
