# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import json
import re
import hashlib
import time
import xmltodict
import tornado.gen

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.options import options, define
# from tornado.httpserver import HTTPRequest
from tornado.httpclient import HTTPRequest
from datetime import datetime
from tornado.httpclient import AsyncHTTPClient
from app_setting import Application
from urllib import quote
from xpinyin import Pinyin

define('port', default=8000, type=int)
WECHAT_TOKEN = 'running'
APPID = 'wx4b0e5c78cb1fb29f'
SERECT = '60eb19d351c28b4b6a8fd69b40cd7b0a'
APPID2 = 'wx7aa4555c797cda6b'
SERECT2 = 'f19af24776eeb3b389c0a4d6a3779483'
cd = 'http://7kp874.natappfree.cc'
URL = 'http://7kp874.natappfree.cc'
MEDIA_GSL = 'zA650XvskhPOsV2iA8BPJIKETTlfcoXSqmeTO5VNlGq14SZ3bCUAYFhU49Fs_oxN'

MEDIA_HY = 'Zbt0iqj8qETurZYfjdSMi7xqv8Mn1GFlvYiQDySo_X4'


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class ChatHandler(WebSocketHandler):
    users = set()

    @tornado.gen.coroutine
    def open(self, *args, **kwargs):
        data = yield self.get_info()
        if not data:
            self.send_error(500)
        else:
            cname = data['cname']
            self.users.add(self)
            for user in self.users:
                user.write_message(u'[%s]--[%s]--[%s] 进入聊天室'
                                   % (cname, self.request.remote_ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    @tornado.gen.coroutine
    def on_message(self, message):
        data = yield self.get_info()
        if not data:
            self.send_error(500)
        else:
            cname = data['cname']
            for user in self.users:
                user.write_message(u'[%s] - [%s] - [%s] -> %s'
                                   % (cname, self.request.remote_ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      message))

    @tornado.gen.coroutine
    def on_close(self):
        data = yield self.get_info()
        if not data:
            self.send_error(500)
        else:
            cname = data['cname']
            self.users.remove(self)
            for user in self.users:
                user.write_message(u'[%s]--[%s]--[%s] 离开聊天室'
                                   % (cname, self.request.remote_ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def check_origin(self, origin):
        return True

    @tornado.gen.coroutine
    def get_info(self):
        client = AsyncHTTPClient()
        response = yield client.fetch("http://pv.sohu.com/cityjson?ie=utf-8")
        if response.error:
            dict_data = ''
        else:
            pattern = re.compile(r'.*=(.*);')
            data = pattern.findall(response.body)[0]
            dict_data = json.loads(data)
        raise tornado.gen.Return(dict_data)


class WechatHandler(RequestHandler):
    # def prepare(self):
    #     # 开发者验证接口
    #     signature = self.get_argument("signature", "")
    #     timestamp = self.get_argument("timestamp", "")
    #     nonce = self.get_argument("nonce", "")
    #
    #     t_list = [WECHAT_TOKEN, timestamp, nonce]
    #     t_list.sort()
    #     t_str = ''.join(t_list)
    #     l_str = hashlib.sha1(t_str).hexdigest()
    #     if l_str != signature:
    #         self.send_error(400)

    def replay_text(self, xml_data):
        list_media = ListMedia()
        name = xml_data.get('Content')
        match_id = yield list_media.get_matchid(name)
        if match_id == 0:
            xml_content = {
                'ToUserName': xml_data.get('FromUserName'),
                'FromUserName': xml_data.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': u'嗯哼~名字都不打对，还想偷看我的秘籍？回复正确的英雄名称如：swk  yyh'
            }
            raise tornado.gen.Return(xmltodict)
        else:
            xml_content = {
                'ToUserName': xml_data.get('FromUserName'),
                'FromUserName': xml_data.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'image',
                "Image": {"MediaId": match_id}
                # 'MediaId': xml_data.get('MediaId', u'未识别')
                # 'Content': xml_data.get('MediaId', u'未识别')
            }
            raise tornado.gen.Return(xml_content)

    def reply_image(self, xml_data):
        input_str = xml_data.get('Content')
        pinxin = Pinyin()
        input_str = pinxin.get_initials(input_str, u'').lower()
        pattern = re.compile(r'statics/media/(\w+)')
        xml_content = {
            'ToUserName': xml_data.get('FromUserName'),
            'FromUserName': xml_data.get('ToUserName'),
            'CreateTime': int(time.time()),
            'MsgType': 'text',
            'Content': u'嗯哼~\n名字都不打对，还想偷看我的秘籍？\n回复正确的英雄名称\n      如:  廉颇、芈月 \n      或   lp 、 my\n就能查看该英雄的备战铭文和视频攻略啦~'
            # 'Content':input_str
        }
        with open('image_media_id2.json', 'r') as json_file:
            item_dict = json.load(json_file)
        for item in item_dict['item']:
            match_str = item['name']
            print '==========================', match_str
            ret = pattern.search(match_str)
            if ret:
                match_str = ret.group(1)
            if input_str == match_str:
                xml_content = {
                    'ToUserName': xml_data.get('FromUserName'),
                    'FromUserName': xml_data.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'image',
                    "Image": {"MediaId": item['media_id']}
                }
        return xml_content

    @tornado.gen.coroutine
    def get_nickname(self, xml_data):
        openid = xml_data.get('FromUserName')
        access_token = yield AccessToken.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
            access_token, openid)
        client = AsyncHTTPClient()
        response = yield client.fetch(url)
        dict_data = json.loads(response.body)
        if dict_data.get('nickname'):
            nickname = dict_data['nickname']
            sex = u'先生' if dict_data.get('sex') == 1 else u'女士'
        else:
            nickname = ''
            sex = ''

        raise tornado.gen.Return(nickname + sex)

    @tornado.gen.coroutine
    def get_api_content(self, xml_data):

        text = xml_data.get('Recognition', u'未识别')
        url = 'http://openapi.tuling123.com/openapi/api/v2'
        data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": text
                }

            },
            "userInfo": {
                "apiKey": "4008cce63c0f4cf8a3b0aba0af766ab5",
                "userId": "running007"
            }
        }

        client = AsyncHTTPClient()
        request = HTTPRequest(url, method='POST', body=json.dumps(data, ensure_ascii=False))
        response = yield client.fetch(request)
        dict_data = json.loads(response.body)
        print type(dict_data["results"][0]['values'])
        data = dict_data["results"][0]["values"]['text']

        xml_content = {
            'ToUserName': xml_data.get('FromUserName'),
            'FromUserName': xml_data.get('ToUserName'),
            'CreateTime': int(time.time()),
            'MsgType': 'text',
            # 'Voice': {"MediaId": xml_data.get('MediaId', u'未识别')}
            # 'Content': xml_data.get('Recognition', u'未识别')
            'Content': data
        }
        raise tornado.gen.Return(xml_content)

    def get(self, *args, **kwargs):
        # 开发者验证接口
        signature = self.get_argument("signature", "")
        timestamp = self.get_argument("timestamp", "")
        nonce = self.get_argument("nonce", "")
        echostr = self.get_argument("echostr", "")
        t_list = [WECHAT_TOKEN, timestamp, nonce]
        t_list.sort()
        t_str = ''.join(t_list)
        l_str = hashlib.sha1(t_str).hexdigest()
        if l_str != signature:
            self.write('error')
        else:
            self.write(echostr)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        data = self.request.body
        xml_data = xmltodict.parse(data)['xml']

        if xml_data.get('MsgType') == 'text':
            xml_content = self.reply_image(xml_data)

        elif xml_data.get('MsgType') == 'image':
            xml_content = {
                'ToUserName': xml_data.get('FromUserName'),
                'FromUserName': xml_data.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'image',
                "Image": {"MediaId": xml_data.get('MediaId', u'未识别')}
                # "Image": {"MediaId": "Zbt0iqj8qETurZYfjdSMi7BVP7vXCtJ6GhTSpxfEZ4I"}
                # 'Image':{'MediaId':'Zbt0iqj8qETurZYfjdSMi7BVP7vXCtJ6GhTSpxfEZ4I'}
                # 'MediaId': xml_data.get('MediaId', u'未识别')
                # 'Content': xml_data.get('MediaId', u'未识别')
            }
        elif xml_data.get('MsgType') == 'voice':

            # xml_content = {
            #     'ToUserName': xml_data.get('FromUserName'),
            #     'FromUserName': xml_data.get('ToUserName'),
            #     'CreateTime': int(time.time()),
            #     'MsgType': 'text',
            #     # 'Voice': {"MediaId": xml_data.get('MediaId', u'未识别')}
            #     # 'Content': xml_data.get('Recognition', u'未识别')
            #     'Content': xml_data.get('FromUserName')
            # }
            xml_content=yield self.get_api_content(xml_data)
        elif xml_data.get('MsgType') == 'video':
            try:
                xml_content = {
                    'ToUserName': xml_data.get('FromUserName'),
                    'FromUserName': xml_data.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'image',
                    'Image': {"MediaId": MEDIA_HY}
                    # 'Content': xml_data.get('Recognition', u'未识别')
                    # 'Content': xml_data.get('MediaId', u'未识别')
                }
            except  Exception as e:
                xml_content = {
                    'ToUserName': xml_data.get('FromUserName'),
                    'FromUserName': xml_data.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': u'视频未识别'
                }

        elif xml_data.get('MsgType') == 'event':
            nickname = yield self.get_nickname(xml_data)
            if xml_data.get('Event') == 'subscribe':

                xml_content = {
                    'ToUserName': xml_data.get('FromUserName'),
                    'FromUserName': xml_data.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': nickname + u'您好，欢迎订阅'
                }
                if xml_data.get('EventKey'):
                    xml_content['Content'] += u'，场景值' + xml_data.get('EventKey')[8:]
            elif xml_data.get('Event') == 'SCAN':
                xml_content = {
                    'ToUserName': xml_data.get('FromUserName'),
                    'FromUserName': xml_data.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': nickname + u'您好，您扫描的场景值为%s' % xml_data.get('EventKey')
                }
            else:
                xml_content = {}


        else:
            xml_content = {
                'ToUserName': xml_data.get('FromUserName'),
                'FromUserName': xml_data.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': u'hello running',
            }

        xml = xmltodict.unparse({'xml': xml_content})
        self.write(xml)


class AccessToken(object):
    _access_token = {'token': None, 'create_time': None, 'expires_in': None}

    @classmethod
    @tornado.gen.coroutine
    def update_access_token(cls):
        client = AsyncHTTPClient()
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            APPID, SERECT)
        response = yield client.fetch(url)
        content = json.loads(response.body)
        token = content.get('access_token')
        if token:
            cls._access_token['token'] = token
            cls._access_token['create_time'] = time.time()
            cls._access_token['expires_in'] = content['expires_in']

    @classmethod
    @tornado.gen.coroutine
    def get_access_token(cls):
        if not cls._access_token['token'] or (
                time.time() - cls._access_token['create_time'] > cls._access_token['expires_in']):
            yield cls.update_access_token()
        raise tornado.gen.Return(cls._access_token['token'])


class TokenHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        token = yield AccessToken.get_access_token()
        print token
        print type(token)
        self.write(token)


class OrcodeHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        token = yield AccessToken.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % token
        scene_id = self.get_argument('sid')
        req_body = '{"expire_seconds": 604800, "action_name": "QR_SCENE","action_info": {"scene": {"scene_id":%s}}' % scene_id
        client = AsyncHTTPClient()
        request = HTTPRequest(url, method='POST', body=req_body)
        response = yield client.fetch(request)
        code_data = json.loads(response.body)
        if code_data.get('errcode'):
            self.write(code_data['errmsg'])
            # self.write(code_data['errcode'])
        else:
            ticket = code_data['ticket']
            self.write('<img src="//mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket)


class UserHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        code = self.get_argument('code')
        # 判断用户是否授权
        if not code:
            self.write('您未授权，无法获取您的信息！')
            return
        # 授权后获得access_token
        client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
            APPID, SERECT, code)
        response = yield client.fetch(url)
        dict_data = json.loads(response.body)
        access_token = dict_data.get('access_token')
        # 获取用户信息
        if access_token:
            openid = dict_data.get('openid')
            url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (access_token, openid)
            response = yield client.fetch(url)
            dict_data = json.loads(response.body)
            if dict_data.get('errcode'):
                self.write(dict_data.get('errmsg', '获取个人信息错误'))
            else:
                self.render('user.html', user=dict_data)
        else:
            self.write(dict_data.get('errmsg', '获取access_token 错误'))


class CreateMenuHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        access_token = yield AccessToken.get_access_token()
        if access_token:
            menu_data = {
                "button": [
                    {
                        "type": "view",
                        "name": "测试个人信息",
                        "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect" % (
                            APPID, quote(URL + '/profile'))
                    },
                    {
                        "name": "菜单",
                        "sub_button": [
                            {
                                "type": "view",
                                "name": "搜索",
                                "url": "http://www.baidu.com"
                            },
                            {
                                "type": "view",
                                "name": "视频",
                                "url": "http://v.qq.com/"
                            }

                        ]
                    }
                ]
            }
            client = AsyncHTTPClient()
            url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
            request = HTTPRequest(url, method='POST', body=json.dumps(menu_data, ensure_ascii=False))
            response = yield client.fetch(request)
            dict_data = json.loads(response.body)
            if 0 == dict_data.get('errcode'):
                self.write('创建菜单成功')
            else:
                self.write('创建菜单失败')
        else:
            self.write('no token')


class ListMedia(object):
    def __init__(self):
        self.access_token = ''

    @tornado.gen.coroutine
    def get_materialcount(self):
        if not self.access_token:
            self.access_token = yield AccessToken.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s' % self.access_token
        client = AsyncHTTPClient()
        response = yield client.fetch(url)
        dict_data = json.loads(response.body)
        # {"voice_count":0,"video_count":0,"image_count":4,"news_count":0}
        if dict_data.get('image_count'):
            raise tornado.gen.Return(dict_data['image_count'])
        else:
            raise tornado.gen.Return(-1)

    @tornado.gen.coroutine
    def get_mediaid_list(self, offset):
        print '1111'
        if not self.access_token:
            self.access_token = yield AccessToken.get_access_token()
        # print 'token', access_token
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % self.access_token
        body = {
            "type": 'image',
            "offset": offset,
            "count": 20
        }
        client = AsyncHTTPClient()
        request = HTTPRequest(url, method='POST', body=json.dumps(body, ensure_ascii=False))
        response = yield client.fetch(request)
        dic_data = json.loads(response.body)
        print 'dict_data', dic_data
        if dic_data.get('item'):
            raise tornado.gen.Return(dic_data['item'])
        else:
            raise tornado.gen.Return('errcode')

    @tornado.gen.coroutine
    def write_image_media_id(self):
        try:
            count = yield self.get_materialcount()
            if count < 0:
                raise tornado.gen.Return('errcode 1')
            count = count / 20 + 1
            item = []
            for index in range(count):
                mediaid_list = yield self.get_mediaid_list(index * 20)
                if mediaid_list == 'errcode':
                    raise tornado.gen.Return('errcode 2')
                if mediaid_list:
                    item += mediaid_list
            item_data = {'item': item}
            with open('image_media_id2.json', 'w')as json_file:
                json.dump(item_data, json_file)
            raise tornado.gen.Return('ok')
        except Exception as e:
            print 'except', e
            raise tornado.gen.Return('message')

    @tornado.gen.coroutine
    def get_matchid(self, name):
        flag = 0
        count = yield self.get_materialcount()
        count = count / 5 + 1
        for index in range(count):
            mediaid_list = yield self.get_mediaid_list(index * 20)
            for item in mediaid_list:
                if name in item['name']:
                    flag = 1
                    raise tornado.gen.Return(item['media_id'])
        if flag == 0:
            raise tornado.gen.Return(0)


class GetMediaidHandelr(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            listMedia = ListMedia()
            dict_data = yield listMedia.get_mediaid_list(0)
            self.write(dict_data)
        except Exception as e:
            self.write(e.message)


class WriteJsonHandelr(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        media = ListMedia()
        message = yield media.write_image_media_id()
        self.write(message)


class ApiHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # apikey = '5617dccf32284218846fea4ef4d9a637'
        url = 'http://openapi.tuling123.com/openapi/api/v2'
        data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": "你好"
                },
                "selfInfo": {
                    "location": {
                        "city": "北京",
                        "province": "北京",
                        "street": "信息路"
                    }
                }

            },
            "userInfo": {
                "apiKey": "5617dccf32284218846fea4ef4d9a637",
                "userId": "run01"
            }
        }

        client = AsyncHTTPClient()
        request = HTTPRequest(url, method='POST', body=json.dumps(data, ensure_ascii=False))
        response = yield client.fetch(request)
        dict_data = json.loads(response.body)
        print type(dict_data["results"][0]['values'])
        data = dict_data["results"][0]["values"]['text']

        self.write(data)


# 继承Application类，重写handlers
class CurrentApplication(Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/chat', ChatHandler),
            (r'/wechat', WechatHandler),
            (r'/token', TokenHandler),
            (r'/code', OrcodeHandler),
            (r'/profile', UserHandler),
            (r'/menu', CreateMenuHandler),
            (r'/get_mediaid', GetMediaidHandelr),
            (r'/write_image_json', WriteJsonHandelr),
            (r'/api', ApiHandler),

        ]
        super(CurrentApplication, self).__init__(handlers)


if __name__ == '__main__':
    options.parse_command_line()
    app = CurrentApplication()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

# https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4b0e5c78cb1fb29f&redirect_uri=http%3A//wzu4ce.natappfree.cc/profile&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect
