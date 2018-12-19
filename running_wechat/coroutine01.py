# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.httpclient import AsyncHTTPClient
import re
import json
import tornado.gen


class IndexHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        client = AsyncHTTPClient()
        response = yield client.fetch('http://pv.sohu.com/cityjson?ie=utf-8')
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
    tornado.options.parse_command_line()
    app = tornado.web.Application([(r'/', IndexHandler), ], debug=True)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
