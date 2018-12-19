# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import re
import json


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        client = AsyncHTTPClient()
        client.fetch('http://pv.sohu.com/cityjson?ie=utf-8', callback=self.on_response)

    def on_response(self, response):
        if response.error:
            self.send_error(500)
        else:
            pattern = re.compile(r'.*=(.*);')
            data = pattern.findall(response.body)[0]
            dict_data = json.loads(data)
            cip = dict_data['cip']
            cname = dict_data['cname']
            self.write(u'ip地址：%s,城市名称：%s' % (cip, cname))
            self.write('haha')
        self.finish()


if __name__ == '__main__':
    app = tornado.web.Application([(r'/', IndexHandler), ], debug=True)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
