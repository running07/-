# -*- coding:utf-8 -*-
import logging
from basehandler import BaseHandler
from running_home.utils.commons import request_login
from running_home.utils.response_code import RET
from running_home.utils.qiniu_storage import storage
from running_home import constants


class ProfileHandler(BaseHandler):
    @request_login
    def get(self, *args, **kwargs):




        user_id = self.session.data.get('user_id')
        try:
            sql = 'select uname,mobile,avatar,qqnum,telephone from user_profile where user_id=%s'
            ret = self.db.get(sql, user_id)
            if ret['avatar']:
                image_url = constants.QINIU_URL_PREFIX + ret['avatar']
            else:
                image_url = ''
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库错误'))

        else:
            qqnum=ret["qqnum"] if ret["qqnum"] else ''
            telephone=ret["telephone"] if ret["telephone"] else ''

            return self.write(dict(errcode=RET.OK, errmsg='ok',
                                   data=dict(user_id=user_id, name=ret['uname'], mobile=ret['mobile'],
                                             avatar=image_url,qqnum=qqnum,telephone=telephone)))


class AlterNameandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        name = self.json_data.get('name')

        if not name:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数缺失'))
        try:
            sql = 'update user_profile set uname=%s where user_id=%s'
            self.db.execute_rowcount(sql, name, user_id)
            self.session.data['name'] = name
            self.session.save()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库错误'))

        return self.write(dict(errcode=RET.OK, errmag='OK'))

class AlterQQnumandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        qqnum = self.json_data.get('qqnum')

        if not qqnum:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数缺失'))
        try:
            sql = 'update user_profile set qqnum=%s where user_id=%s'
            self.db.execute_rowcount(sql, qqnum, user_id)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库错误'))
        #qq号码改变，更新redis中房屋信息，
        try:
            sql='select house_id from house_info where house_user_id=%s'
            ret=self.db.query(sql,user_id)
        except Exception as e:
            ret=[]
            logging.error(e)
        print ret
        if ret:
            try:
                for l in ret:
                    key="house_info_%s" %l["house_id"]
                    print key
                    self.redis.delete(key)
            except Exception as e:
                logging.error(e)




        return self.write(dict(errcode=RET.OK, errmag='OK'))

class AlterTelephonenumandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        telephone = self.json_data.get('telephone')

        if not telephone:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数缺失'))
        try:
            sql = 'update user_profile set telephone=%s where user_id=%s'
            self.db.execute_rowcount(sql, telephone, user_id)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库错误'))
        # 咨询热线改变，更新redis中房屋信息，
        try:
            sql = 'select house_id from house_info where house_user_id=%s'
            ret = self.db.query(sql, user_id)
        except Exception as e:
            ret = []
            logging.error(e)
        print ret
        if ret:
            try:
                for l in ret:
                    key = "house_info_%s" % l["house_id"]
                    print key
                    self.redis.delete(key)
            except Exception as e:
                logging.error(e)
        return self.write(dict(errcode=RET.OK, errmag='OK'))


class UploadAvatarHandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        files = self.request.files.get('avatar')
        if files:
            avatar = files[0]['body']
        else:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='未传图片'))
        try:
            filename = storage(avatar)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR, errmsg='上传失败'))
        sql = 'update user_profile set avatar=%s where user_id=%s'
        try:
            self.db.execute_rowcount(sql, filename, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库保存错误'))
        return self.write(dict(errcode=RET.OK, errmsg='OK', data="%s%s" % (constants.QINIU_URL_PREFIX, filename)))


class AuthHandler(BaseHandler):
    @request_login
    def get(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        sql = 'select user_id,real_name,id_card from user_profile where user_id=%s'
        try:
            ret = self.db.get(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='访问数据库出错'))
        self.write(dict(errcode=RET.OK, errmsg='OK', data=dict(real_name=ret['real_name'], id_card=ret['id_card'])))

    @request_login
    def post(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        real_name = self.json_data.get('real_name')
        id_card = self.json_data.get('id_card')
        print 'real_name',real_name
        print 'daa',self.json_data
        sql = 'update user_profile set real_name=%s,id_card=%s where user_id=%s'
        try:
            self.db.execute_rowcount(sql, real_name, id_card, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='更新数据库错误'))
        else:
            return self.write(dict(errcode=RET.OK, errmsg='OK'))
