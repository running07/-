# -*- coding:utf-8 -*-
import json
import logging
import datetime
from basehandler import BaseHandler
from running_home.utils.response_code import RET
from running_home import constants
from running_home.utils.commons import request_login


class OrderHandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        house_id = self.json_data.get('house_id')
        start_date = self.json_data.get('start_date')
        end_date = self.json_data.get('end_date')

        # 判断参数是否齐全
        if not all((house_id, start_date, end_date)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='缺少数据'))
        # 判断是否为房东预订房间
        try:
            sql = 'select house_user_id,price from house_info where house_id=%s'
            house_ret = self.db.get(sql, house_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='没有房源信息'))
        if user_id == house_ret['house_user_id']:
            return self.write(dict(errcode=RET.ROLEERR, errmsg='房东不能预订房间'))
        # 判断预订日期
        days = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date,
                                                                                              "%Y-%m-%d")).days + 1
        if days <= 0:
            return self.write({"errcode": RET.PARAMERR, "errmsg": "date params error"})
        # 判断用户下单期间，没有其他人下单
        try:
            sql = 'select count(*) counts from order_info where house_id=%s and begin_date<%s and end_date>%s'
            ret = self.db.get(sql, house_id, start_date, end_date)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='访问order_info表出错'))
        if int(ret["counts"]) > 0:
            return self.write(dict(errcode=RET.DATAERR, errmsg='暂时没有符合条件的房间'))
        amount = days * house_ret["price"]
        # 保存订单
        try:
            sql = 'insert into order_info(order_user_id,house_id,begin_date,end_date,days,house_price,amount) values(%(order_user_id)s,%(house_id)s,%(begin_date)s,%(end_date)s,%(days)s,%(house_price)s,%(amount)s);update house_info set order_count=order_count+1 where house_id=%(house_id)s;'
            self.db.execute(sql, order_user_id=user_id, house_id=house_id, begin_date=start_date, end_date=end_date,
                            days=days, house_price=house_ret['price'], amount=amount)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='order_info插入数据出错'))
        return self.write(dict(errcode=RET.OK, errmsg='OK'))


class MyOrderHandler(BaseHandler):
    @request_login
    def get(self):
        user_id = self.session.data.get('user_id')
        role = self.get_argument('role', '')
        try:
            if role == 'landlord':
                sql = 'select order_info.house_id,order_id,title,index_image_url,begin_date,end_date,order_info.ctime,days,amount,status,comment,r_comment from order_info inner join house_info on order_info.house_id=house_info.house_id left join reply_comment on order_id=r_order_id where house_user_id=%s order by order_info.ctime desc'
            else:
                sql = 'select order_info.house_id, order_id,title,index_image_url,begin_date,end_date,order_info.ctime,days,amount,status,comment,r_comment from order_info inner join house_info on order_info.house_id=house_info.house_id left join reply_comment on order_id=r_order_id where order_user_id=%s order by order_info.ctime desc'
            ret = self.db.query(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='访问数剧库出错'))
        date = []
        if ret:
            for l in ret:
                house = {
                    "house_id":l["house_id"],
                    "order_id": l["order_id"],
                    "title": l["title"],
                    "img_url": constants.QINIU_URL_PREFIX + l["index_image_url"] if l.get('index_image_url') else '',
                    "start_date": l["begin_date"].strftime("%Y-%m-%d"),
                    "end_date": l["end_date"].strftime("%Y-%m-%d"),
                    "ctime": l["ctime"].strftime("%Y-%m-%d"),
                    "days": l["days"],
                    "amount": l["amount"],
                    "status": l["status"],
                    "comment": l["comment"] if l["comment"] else '',
                    "r_comment":l["r_comment"] if l.get("r_comment") else ''
                }
                date.append(house)
        return self.write(dict(errcode=RET.OK, errmsg='OK', orders=date))


class AcceptHandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        order_id = self.json_data.get('order_id')
        user_id = self.session.data.get('user_id')
        if not all((order_id, user_id)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='缺少数据'))
        try:
            sql = 'update order_info set status=3 where order_id=%(order_id)s and status=0 and order_info.house_id in (select house_info.house_id from house_info where house_user_id=%(user_id)s)'
            self.db.execute(sql, order_id=order_id,user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='修改数据错误'))
        return self.write(dict(errcode=RET.OK, errmsg='OK'))


class RejecttHandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        order_id = self.json_data.get('order_id')
        user_id = self.session.data.get('user_id')
        reject_reason=self.json_data.get('reject_reason')
        if not all((order_id, user_id)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='缺少数据'))
        try:
            sql = 'update order_info set status=6, comment=%(comment)s where order_id=%(order_id)s and status=0 and order_info.house_id in (select house_info.house_id from house_info where house_user_id=%(user_id)s)'
            self.db.execute(sql, comment=reject_reason,order_id=order_id,user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='修改数据错误'))
        return self.write(dict(errcode=RET.OK, errmsg='OK'))

class ReplytHandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        order_id = self.json_data.get('order_id')
        user_id = self.session.data.get('user_id')
        reply_text=self.json_data.get('reply_text')
        if not all((order_id, user_id)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='缺少数据'))
        try:
            sql='insert into reply_comment (r_order_id,r_comment) values(%(order_id)s,%(comment)s)'
            sql2='update order_info set status=7  where order_id=%(order_id)s and status=4'


            self.db.execute(sql, comment=reply_text,order_id=order_id)
            self.db.execute(sql2,order_id=order_id)

        except Exception as e:
            logging.error(e)

            return self.write(dict(errcode=RET.DBERR, errmsg='修改数据错误'))

        # 更新redis数据库house_info
        try:
            ret = self.db.get('select house_id from order_info where order_id=%s', order_id)
            if ret:
                self.redis.delete('house_info_%s', ret['house_id'])
            else:
                print '========================'
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.REQERR, errmsg='REDIS'))

        return self.write(dict(errcode=RET.OK, errmsg='OK'))

class OrderCommentHandler(BaseHandler):
    @request_login
    def post(self, *args, **kwargs):
        user_id=self.session.data['user_id']
        order_id=self.json_data.get('order_id')
        comment=self.json_data.get('comment')
        #判断数据是否齐全
        if not all((user_id,order_id,comment)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='参数缺少'))
        try:
            sql='update order_info set status=4 ,comment=%(comment)s where order_id=%(order_id)s and order_user_id=%(user_id)s and status=3'
            self.db.execute(sql,comment=comment,order_id=order_id,user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR,errmsg='更新order_info 表出错'))
        #
        #更新redis数据库house_info
        try:
            ret=self.db.get('select house_id from order_info where order_id=%s',order_id)
            if ret:
                self.redis.delete('house_info_%s',ret['house_id'])
            else:
                print '========================'
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.REQERR, errmsg='REDIS'))
        return self.write(dict(errcode=RET.OK,errmsg='OK'))

