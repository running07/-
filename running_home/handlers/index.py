# -*- coding:utf-8 -*-
from tornado.web import RequestHandler
from basehandler import BaseHandler
import logging


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        print self.db
        print self.redis
        logging.debug('denug')
        logging.info('info')
        logging.warning('warning')
        logging.error('error')

        self.write('ok')
