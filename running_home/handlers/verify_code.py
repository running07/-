# -*- coding:utf-8 -*-
import sys

sys.path.append('../')
import logging
import re
import random
import redis
from running_home import constants
from basehandler import BaseHandler
from running_home.utils.captcha.captcha import captcha
from running_home.utils.response_code import RET
from running_home.libs.yuntongxun.SendTemplateSMS import ccp


class PicCodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # 获取当前和上一次验证码id
        pre_code_id = self.get_argument('pre', '')
        cur_code_id = self.get_argument('cur')
        # 获取验证码
        name, text, pic = captcha.generate_captcha()
        # 删除上一次验证码id,把当前验证码id保存到redis中
        try:
            if pre_code_id:
                self.redis.delete('pic_code_id_%s', pre_code_id)
            self.redis.setex('pic_code_id_%s' % cur_code_id, constants.PIC_CODE_EXPIRES_SECONDS, text)
        except  Exception as e:
            logging.error(e)
            self.write('error')
        # 设置Type类型
        self.set_header('Content-Type', 'image/jpg')
        self.write(pic)


class SMSCodeHandler(BaseHandler):
    def post(self, *args, **kwargs):
        # 获取参数
        print '=====',self.json_data
        mobile = self.json_data.get("mobile")
        piccode = self.json_data.get("piccode")
        piccode_id = self.json_data.get("piccode_id")

        #是否全部都有
        if not all ((mobile,piccode,piccode_id)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='参数缺失'))

        if not re.match(r'1\d{10}',mobile):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='手机号码格式不对'))

        #获取图片验证码
        try:
            real_piccode=self.redis.get('pic_code_id_%s'%piccode_id)
        except Exception as e:
            return self.write(dict(errcode=RET.DBERR,errmsg='查询验证码错误'))
        if not real_piccode:
            return self.write(dict(errcode=RET.NODATA,errmsg='验证码过期'))
        #删测图片验证码
        try:
            self.redis.delete('pic_code_id_%s'%piccode_id)
        except Exception as e:
            logging.error(e)
        #验证验证码是否正确
        if real_piccode.lower()!=piccode.lower():
            return  self.write(dict(errcode=RET.DATAERR,errmsg='验证码错误'))

        #验证手机号是否存在


        sms_code = "%06d" % random.randint(1, 1000000)
        try:
            self.redis.setex('sms_code_%s'%mobile,constants.SMS_CODE_EXPIRES_SECONDS,sms_code)
        except Exception as e:
            logging.error(e)
            self.write(dict(errcode=RET.DATAERR,errmsg='数据库错误'))
        #发送短信
        try:
            result=ccp.sendTemplateSMS(mobile,[sms_code,constants.SMS_CODE_EXPIRES_SECONDS/60],1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR,errmsg='发送短信失败'))

        if result:
            self.write(dict(errcode=RET.OK,errmsg='发送成功'))
        else:
            self.write(dict(errcode=RET.UNKOWNERR,errmsg='发送失败'))
