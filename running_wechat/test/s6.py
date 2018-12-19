# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
from tornado import gen
import tornado_mysql

@gen.coroutine # 注意需要写上装饰器
def get_user(user):
    # 异步非阻塞，Task操作的函数，连接数据库，注意语法结构
    conn = yield tornado_mysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123', db='tornadoTest',
                                       charset='utf8')
    cur = conn.cursor()
    # yield cur.execute("SELECT name,email FROM web_models_userprofile where name=%s", (user,))
    yield cur.execute("select sleep(10)")
    row = cur.fetchone()
    cur.close()
    conn.close()
    raise gen.Return(row) # 注意task函数的返回值


class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    @gen.coroutine
    def post(self, *args, **kwargs):
        user = self.get_argument('user')
        data = yield gen.Task(get_user, user) # 执行Task函数，内部还是返回future对象。Task函数上第一个参数是要执行的函数，第二个是参数
        if data:
            print(data)
            self.redirect('http://www.baidu.com')
        else:
            self.render('login.html')

    #原始方案，请求来了，连接数据库，等待操作完成，关闭连接！
    # def post(self, *args, **kwargs):
    #     user = self.get_argument('user')
    #     # 连接数据库: IO耗时
    #     # 查询语句： IO耗时
    #     # 获取结果
    #     data = {'id':1,'user':'alex'}
    #     if data:
    #         print(data)
    #         self.redirect('http://www.baidu.com')
    #     else:
    #         self.render('login.html')


application = tornado.web.Application([
    (r"/login", LoginHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

