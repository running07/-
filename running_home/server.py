# -*- coding:utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import torndb
import redis
import config

import logging

from urls import handler
from tornado.options import options, define

define('port', default=9000, type=int)


class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handler, **config.settings)
        self.db = torndb.Connection(**config.db_options)
        self.redis=redis.StrictRedis(**config.redis_options)


def main():

    #日志配置
    # options.log_file_prefix=config.log_path
    # options.logging=config.log_level
    options.parse_command_line()
    #端口号
    port = options.port
    # app=tornado.web.Application(handler,**config.settings)
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    # http_server.bind(port)
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
