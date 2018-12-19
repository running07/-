# -*- coding:utf-8 -*-
import os
from handlers.basehandler import StaticHandler
from handlers.index import IndexHandler

from handlers.verify_code import PicCodeHandler, SMSCodeHandler
from handlers.passport import RegisterHandler, LoginHandler, CheckLoginHandler, LoginoutHandler
from handlers.profile import ProfileHandler, AlterNameandler, UploadAvatarHandler, AuthHandler
from handlers import verify_code,passport,profile,order,house

handler = [
    # (r'/', IndexHandler),
    (r'/api/piccode', verify_code.PicCodeHandler),
    (r'/api/smscode', verify_code.SMSCodeHandler),
    (r'/api/register', passport.RegisterHandler),
    (r'/api/login', passport.LoginHandler),
    (r'/api/check_login', passport.CheckLoginHandler),
    (r'/api/logout', passport.LoginoutHandler),
    (r'/api/profile', profile.ProfileHandler),
    (r'/api/profile/name', profile.AlterNameandler),
    (r'/api/profile/telephone',profile.AlterTelephonenumandler),
    (r'/api/profile/qq',profile.AlterQQnumandler),
    (r'/api/profile/avatar', profile.UploadAvatarHandler),
    (r'/api/profile/auth', profile.AuthHandler),
    (r'/api/house/my',house.MyHouseHandler),
    (r'/api/house/area',house.AreaHandler),
    (r'/api/house/info',house.HouseInfoHandler),
    (r'/api/house/image',house.HouseImageHandler),
    (r'/api/house/index',house.IndexHandler),
    (r'/api/house/list',house.HouseListHandelr),
    (r'/api/house/list2',house.HouseRedisListHandelr),
    (r'/api/order',order.OrderHandler),
    (r'/api/order/my',order.MyOrderHandler),
    (r'/api/order/accept',order.AcceptHandler),
    (r'/api/order/reject',order.RejecttHandler),
    (r'/api/order/comment',order.OrderCommentHandler),
    (r'/api/order/reply',order.ReplytHandler),
    (r'/(.*)', StaticHandler, dict(path=os.path.join(os.path.dirname(__file__), 'html'), default_filename='index.html'))
]
