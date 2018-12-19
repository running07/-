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
        data1, data2 = yield [self.get_info(), self.get_info()]
        data3_4=yield dict(data3=self.get_info(),data4=self.get_info())
        self.write_response(data1)
        self.write_response(data2)
        self.write_response(data3_4['data3'])
        self.write_response(data3_4['data4'])

    def write_response(self, data):
        if not data:
            self.send_error(500)
        else:
            cip = data['cip']
            cname = data['cname']
            self.write(u'<p>id地址：%s, 城市名称：%s</p>' % (cip, cname))

    @tornado.gen.coroutine
    def get_info(self):
        client = AsyncHTTPClient()
        response = yield client.fetch('http://pv.sohu.com/cityjson?ie=utf-8')
        if response.error:
            dict_data = {}
        else:
            pattern = re.compile(r'.*=(.*);')
            data = pattern.findall(response.body)[0]
            dict_data = json.loads(data)
        raise tornado.gen.Return(dict_data)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([(r'/', IndexHandler), ], debug=True)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
