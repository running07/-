# -*- coding:utf-8 -*-
import os

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    template_path=os.path.join(os.path.dirname(__file__), 'html'),
    cookie_secret='2Jli4Gg/SuG1Ftm+vyuBuwcIy0XMfUxAp2IK4azQEC8=',
    xsrf_cookies=True,
    debug=True,
    autoload=True,
)

db_options = dict(
    host='192.168.0.106',
    # database='tornado_running',
    database='tornado_running',
    user='root',
    password='mysql'
)
redis_options = dict(
    host='192.168.0.106',
    port=6379
)

# 日志配置
log_path = os.path.join(os.path.dirname(__file__), 'Log/tornado.log')
log_level = 'debug'


passwd_hash_key='SzUI88yUTpC/lCZHzyxZWCv4LG8/0Ux/sUhP1H3DRTM='