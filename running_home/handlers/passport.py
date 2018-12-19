# -*- coding:utf-8 -*-
import re
import logging
import hashlib

from basehandler import BaseHandler
from running_home.utils.response_code import RET
from running_home import config
from running_home.utils.session import Session
from running_home.utils.commons import request_login


class RegisterHandler(BaseHandler):
    def post(self, *args, **kwargs):
        mobile = self.json_data.get('mobile')
        phonecode = self.json_data.get('phonecode')
        password = self.json_data.get('password')

        # 判断三个数据是否都有
        if not all([mobile, phonecode, password]):
            self.write(dict(errcode=RET.PARAMERR, errmsg='参数不完整'))
        # 判断手机号码格式
        if not re.match(r'1\d{10}', mobile):
            self.write(dict(errcode=RET.PARAMERR, errmsg='手机格式不正确'))
        # 判断手机验证码是否正确
        try:
            real_phonecode = self.redis.get('sms_code_%s' % mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='查询验证码错误'))
        if not real_phonecode:
            return self.write(dict(errcode=RET.DBERR, errmsg='验证码过期11'))
        if real_phonecode != phonecode:
            return self.write(dict(errcode=RET.DATAERR, errmsg='验证码错误'))
        # 删除手机验证码id
        try:
            self.redis.delete('sms_code_%s' % mobile)
        except Exception as e:
            logging.error(e)
        # 保存数据，同时判断手机号是否已经存在
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        sql = 'insert into user_profile (uname,mobile,passwd) values(%(uname)s,%(mobile)s,%(passwd)s)'
        try:
            user_id = self.db.execute(sql, uname=mobile, mobile=mobile, passwd=password)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg='手机号已注册'))

        session = Session(self)
        session.data['user_id'] = user_id
        session.data['uname'] = mobile
        session.data['passwd'] = password
        try:
            session.save()
        except Exception as e:
            logging.error(e)
        return self.write(dict(errcode=RET.OK, errmsg='注册成功'))


class LoginHandler(BaseHandler):
    def post(self, *args, **kwargs):
        mobile = self.json_data.get('mobile')
        passwd = self.json_data.get('password')

        # 判断数据完整
        if not all([mobile, passwd]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数不完整'))
        if not re.match(r'1\d{10}', mobile):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='手机号码格式不正确'))
        sql = 'select user_id, uname,passwd from user_profile where mobile=%s'
        try:
            ret = self.db.get(sql, mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库错误'))
        passwd = hashlib.sha256(passwd + config.passwd_hash_key).hexdigest()
        if ret and ret.get('passwd') == unicode(passwd):
            try:
                self.session = Session(self)
                self.session.data['user_id'] = ret['user_id']
                self.session.data['uname'] = ret['uname']
                self.session.data['passwd'] = passwd
                self.session.save()
            except Exception as e:
                logging.error(e)
            else:

                return self.write(dict(errcode=RET.OK, errmsg='登录成功'))

        else:
            return self.write(dict(errcode=RET.UNKOWNERR, errmsg='手机号码或密码错误'))


class CheckLoginHandler(BaseHandler):

    def get(self):
        if self.get_current_user():
            name=self.session.data.get('uname') if self.session.data.get('uname') else self.session.data.get('user_id')
            self.write(dict(errcode=RET.OK, errmsg='Ture', data={'name':name }))
        else:
            self.write(dict(errcode=RET.SESSIONERR, errmsg='Fales'))


class LoginoutHandler(BaseHandler):
    @request_login
    def get(self):
        self.session.clear()
        print 'iiiiiiii'
        return self.write(dict(errcode=RET.OK, errmsg='推测成功'))
