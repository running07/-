# -*- coding:utf-8 -*-
import logging
import json
import math
from basehandler import BaseHandler
from running_home.utils.commons import request_login
from running_home.utils.response_code import RET
from running_home import constants
from running_home.utils.qiniu_storage import storage
from running_home.utils.session import Session


class MyHouseHandler(BaseHandler):
    @request_login
    def get(self, *args, **kwargs):
        user_id = self.session.data.get('user_id')
        sql = 'select house_id,title,price,house_info.ctime,index_image_url,name from house_info inner join area_info on house_info.house_area_id = area_info.area_id where house_user_id=%s'
        try:
            ret = self.db.query(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库出错'))
        if not ret:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='没有房屋信息'))
        data = []
        for l in ret:
            item = {
                "house_id": l["house_id"],
                "title": l["title"],
                "price": l["price"],
                "ctime": l["ctime"].strftime("%Y-%m-%d"),
                "img_url": constants.QINIU_URL_PREFIX + l['index_image_url'] if l['index_image_url'] else '',
                "area_name": l['name']
            }
            data.append(item)
        return self.write(dict(errcode=RET.OK, errmsg='OK', houses=data))


class AreaHandler(BaseHandler):

    def get(self, *args, **kwargs):
        try:
            redis_ret = self.redis.get('area_info')
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='redis 数据库出错'))
        if redis_ret:
            logging.info('hit redis area_info')
            ret = '{"errcode":"0","errmsg":"OK","data":%s}' % redis_ret
            return self.write(ret)
        sql = 'select area_id,name from area_info'
        try:
            db_ret = self.db.query(sql)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='mysql 数据库出错'))
        if not db_ret:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='查询无数据'))
        data = []
        for l in db_ret:
            item = {
                "area_id": l["area_id"],
                "name": l["name"]
            }
            data.append(item)
        json_data = json.dumps(data)
        try:
            self.redis.setex('area_info', constants.REDIS_AREA_INFO_EXPIRES_SECONDES, json_data)
        except Exception as e:
            return self.write(dict(errcode=RET.DBERR, errmsg='保存redis出错'))
        return self.write(dict(errcode=RET.OK, errmsg='OK', data=data))


class HouseInfoHandler(BaseHandler):

    def get(self):
        session = Session(self)
        user_id = session.data.get('user_id', -1)
        house_id = self.get_argument('house_id')
        if not house_id:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='缺少数据'))

        try:
            ret = self.redis.get('house_info_%s' % house_id)
        except Exception as e:
            logging.error(e)
            ret = None
        # 如果redis数据库中有数据，先从redis中获得数据
        if ret:
            resp = '{"errcode":"0","errmsg":"OK","data":%s,"user_id":%s}' % (ret, user_id)
            return self.write(resp)

        # 从mysql数据库中取数据
        sql = 'select house_user_id,title,price,address,room_count,acreage,house_unit,capacity,beds,deposit,min_days,max_days,uname,avatar,qqnum ,telephone from house_info inner join  user_profile on house_user_id=user_id where house_id=%s'
        try:
            ret = self.db.get(sql, house_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg=''))

        data = {
            "hid": house_id,
            "user_id": ret["house_user_id"],
            "title": ret["title"],
            "price": ret["price"],
            "address": ret["address"],
            "room_count": ret["room_count"],
            "acreage": ret["acreage"],
            "unit": ret["house_unit"],
            "capacity": ret["capacity"],
            "beds": ret["beds"],
            "deposit": ret["deposit"],
            "min_days": ret["min_days"],
            "max_days": ret["max_days"],
            "user_name": ret["uname"],
            "user_avatar": constants.QINIU_URL_PREFIX + ret["avatar"] if ret.get("avatar") else "",
            "qqnum": ret["qqnum"] if ret["qqnum"] else '',
            "qqhref": "http://wpa.qq.com/msgrd?v=3&uin=%s&site=qq&menu=yes" % ret["qqnum"] if ret["qqnum"] else '',
            "telephone": ret["telephone"] if ret["telephone"] else ''
        }
        # 查询房屋图片信息
        sql = 'select url from house_image where house_id=%s'
        try:
            images = self.db.query(sql, house_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='访问house_image表出错'))
        image_list = []
        for image in images:
            url = constants.QINIU_URL_PREFIX + image["url"]
            image_list.append(url)
        data["images"] = image_list
        # 查询房屋设施
        sql = 'select facility_id from house_facility where house_id=%s'
        try:
            facility_ret = self.db.query(sql, house_id)
        except Exception as e:
            logging.error(e)
            facility_ret = None
        facility_list = []
        if ret:
            for facility_id in facility_ret:
                facility_list.append(facility_id["facility_id"])
        data["facilities"] = facility_list

        # 查询评论
        sql = 'select comment,r_comment,r_utime,order_info.utime,uname,mobile,avatar from order_info inner join user_profile on order_user_id=user_id left join reply_comment on order_id=r_order_id where house_id=%s and status=7 or status=4 and comment is not null'
        try:
            comment_ret = self.db.query(sql, house_id)
        except Exception as e:
            logging.error(e)

            return self.write(dict(errcode=RET.DBERR, errmsg='评论出错'))
        comment_list = []
        if comment_ret:
            for comment in comment_ret:
                if comment["avatar"]:
                    avatar = constants.QINIU_URL_PREFIX + comment["avatar"]
                else:
                    avatar = 'https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdpKbFgRLnicuLIJpPDE77OmWfVoAbGBdyQ5qGf3pLILa42DeHDfb1hLNsonr9lLUld3jy6bBystw/132'
                item = {
                    "user_name": comment["uname"] if comment.get("uname") else "匿名用户",
                    "content": comment["comment"],
                    "r_comment": comment["r_comment"],
                    "r_utime": comment["r_utime"].strftime("%Y-%m-%d %H-%M-%S") if comment.get('r_utime') else '',
                    "ctime": comment["utime"].strftime("%Y-%m-%d %H-%M-%S"),
                    "avatar": avatar
                }
                comment_list.append(item)
        data["comments"] = comment_list
        # 把数据改成json对象，存到redis数据库中
        json_data = json.dumps(data)
        try:
            self.redis.setex('house_info_%s' % house_id, constants.REDIS_HOUSE_INFO_EXPIRES_SECONDES, json_data)
        except Exception as e:
            logging.error(e)
        resp = '{"errcode":"0","errmsg":"OK","data":%s,"user_id":%s}' % (json_data, user_id)
        # resp = {"errcode":"0","errmsg":"OK","data":json_data,"user_id":user_id}
        return self.write(resp)

    @request_login
    def post(self, *args, **kwargs):
        # 获取参数
        user_id = self.session.data.get('user_id')
        title = self.json_data.get("title")
        price = self.json_data.get("price")
        area_id = self.json_data.get("area_id")
        address = self.json_data.get("address")
        room_count = self.json_data.get("room_count")
        acreage = self.json_data.get("acreage")
        unit = self.json_data.get("unit")
        capacity = self.json_data.get("capacity")
        beds = self.json_data.get("beds")
        deposit = self.json_data.get("deposit")
        min_days = self.json_data.get("min_days")
        max_days = self.json_data.get("max_days")
        facility = self.json_data.get("facility")

        if not all((user_id, title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit,
                    min_days, max_days)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数缺失'))
        try:
            price = int(price) * 100
            deposit = int(deposit) * 100
            # area_id = int(area_id)
            # room_count = int(room_count)
            # acreage = int(acreage)
            # capacity = int(capacity)
            # min_days = int(min_days)
            # max_days = int(max_days)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数错误'))
        try:

            sql = 'insert into house_info (house_user_id,title,price,house_area_id,address,room_count,acreage,house_unit,capacity,beds,deposit,min_days,max_days) values (%(house_user_id)s,%(title)s,%(price)s,%(house_area_id)s,%(address)s,%(room_count)s,%(acreage)s,%(house_unit)s,%(capacity)s,%(beds)s,%(deposit)s,%(min_days)s,%(max_days)s)'
            house_id = self.db.execute(sql, house_user_id=user_id, title=title, price=price, house_area_id=area_id,
                                       address=unicode(address), room_count=room_count, acreage=acreage,
                                       house_unit=unicode(unit),
                                       capacity=capacity, beds=unicode(beds), deposit=deposit, min_days=min_days,
                                       max_days=max_days)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="插入房屋信息错误"))
        f_sql = 'insert into house_facility (house_id,facility_id) values'
        sql_var = []
        vals = []
        for facility_id in facility:
            sql_var.append("(%s,%s)")
            vals.append(house_id),
            vals.append(facility_id)
        f_sql += ','.join(sql_var)
        vals = tuple(vals)
        print f_sql
        print vals
        try:
            self.db.execute(f_sql, *vals)
        except Exception as e:
            logging.error(e)
            self.db.execute('delete from house_info where house_id=%s', house_id)
            return self.write(dict(errcode=RET.DBERR, errmsg="插入房屋设施信息错误"))
        return self.write(dict(errcode=RET.OK, errmsg='OK', house_id=house_id))


class HouseImageHandler(BaseHandler):
    def post(self, *args, **kwargs):
        house_id = self.get_argument('house_id')
        image_data = self.request.files.get('house_image')[0]['body']
        filenmae = storage(image_data)
        print type(house_id)
        print type(filenmae)
        if not filenmae:
            return self.write(dict(errcode=RET.THIRDERR, errmsg='上传图片错误'))
        try:
            sql = 'update house_info set index_image_url =%s where house_id=%s and index_image_url is null;insert into house_image (house_id,url) values (%s,%s)'
            self.db.execute(sql, filenmae, house_id, house_id, filenmae)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库错误'))
        image_ulr = constants.QINIU_URL_PREFIX + filenmae
        return self.write(dict(errcode=RET.OK, errmsg='OK', url=image_ulr))


class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        try:
            ret = self.redis.get('home_page_data')
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            json_house = ret
        else:
            try:
                sql = 'select house_id,title,order_count,index_image_url from house_info order by order_count desc limit %s'
                ret = self.db.query(sql, constants.INDEX_HOUSE_COUNT)
            except Exception as e:
                logging.error(e)

                return self.write(dict(errcode=RET.DBERR, errmsg='访问house_info表出错'))
            data = []
            for l in ret:
                if l.get('index_image_url'):
                    item = {
                        "house_id": l["house_id"],
                        "title": l["title"],
                        "img_url": constants.QINIU_URL_PREFIX + l["index_image_url"]
                    }
                    data.append(item)
            json_house = json.dumps(data)
            try:
                self.redis.setex('house_page_data', constants.INDEX_HOUSE_EXPIRES_SECONDS, json_house)
            except Exception as e:
                logging.error(e)
        # 区域信息
        try:
            ret = self.redis.get('area_info')
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            json_area = ret
        else:
            try:
                sql = 'select area_id,name from area_info'
                area_ret = self.db.query(sql)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, errmsg='访问area_info表出错'))
            data = []
            for area in area_ret:
                item = {"area_id": area["area_id"], "name": area["name"]}
                data.append(item)
            json_area = json.dumps(data)
            try:
                self.redis.setex("area_info", constants.INDEX_AREA_EXPIRES_SECONDS, json_area)
            except Exception as e:
                logging.error(e)
        reps = '{"errcode":"0","errmsg":"OK","houses":%s,"areas":%s}' % (json_house, json_area)
        return self.write(reps)


class HouseListHandelr(BaseHandler):

    def get(self, *args, **kwargs):
        '''

        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
        '''
        area_id = self.get_argument('aid', '')
        start_date = self.get_argument('sd', '')
        end_date = self.get_argument('ed', '')
        sort_key = self.get_argument('sk', 'new')
        page = self.get_argument('p', '1')
        print '==================', page

        sql = 'select distinct title,a.house_id,price,room_count,address,order_count,avatar,index_image_url,c.ctime from house_info a inner join user_profile b on house_user_id =user_id left join order_info c on a.house_id=c.house_id '
        sql_total_count = 'select count(distinct a.house_id) count from house_info a inner join user_profile b on house_user_id =user_id left join order_info c on a.house_id=c.house_id'

        sql_where = []  # 用来保存sql语句的where条件
        sql_params = {}  # 用来保存sql查询所需的动态数据

        if start_date and end_date:
            sql_part = "((begin_date>%(end_date)s or end_date<%(start_date)s) " \
                       "or (begin_date is null and end_date is null))"
            sql_where.append(sql_part)
            sql_params["start_date"] = start_date
            sql_params["end_date"] = end_date
        elif start_date:
            sql_part = "(end_date<%(start_date)s or (begin_date is null and end_date is null))"
            sql_where.append(sql_part)
            sql_params["start_date"] = start_date
        elif end_date:
            sql_part = "(begin_date>%(end_date)s or (begin_date is null and end_date is null))"
            sql_where.append(sql_part)
            sql_params["end_date"] = end_date
        if area_id:
            sql_area = 'house_area_id=%(area_id)s'
            sql_where.append(sql_area)
            sql_params["area_id"] = area_id
        if sql_where:
            sql += ' where '
            sql += ' and '.join(sql_where)
            sql_total_count += ' where '
            sql_total_count += ' and '.join(sql_where)
        try:
            ret = self.db.get(sql_total_count, **sql_params)
        except Exception as e:
            logging.error(e)
            total_page = -1
        else:
            print ret
            total_page = int(math.ceil(ret["count"] / float(constants.HOUSE_LIST_PAGE_CAPACITY)))
        page = int(page)
        if page > total_page:
            return self.write(dict(errcode=RET.OK, errmsg='没有数据', data=[], total_page=total_page))
        # 排序
        if sort_key == 'new':
            sql += ' order by a.ctime desc'
        elif sort_key == 'booking':
            sql += ' order by order_count desc'
        elif sort_key == 'price-inc':
            sql += ' order by price asc'
        elif sort_key == 'price-des':
            sql += ' order by price desc'

        # 分页
        if page == 1:
            sql += ' limit %s' % constants.HOUSE_LIST_PAGE_CAPACITY
        else:
            sql += ' limit %s ,%s' % (
                (page - 1) * constants.HOUSE_LIST_PAGE_CAPACITY, constants.HOUSE_LIST_PAGE_CAPACITY)
        print sql
        print area_id
        print sql_params

        # 查询数据
        try:
            ret = self.db.query(sql, **sql_params)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='访问数据库出错'))
        data = []
        if ret:
            for l in ret:
                house = {
                    "house_id": l["house_id"],
                    "title": l["title"],
                    "price": l["price"],
                    "room_count": l["room_count"],
                    "address": l["address"],
                    "order_count": l["order_count"],
                    "avatar": constants.QINIU_URL_PREFIX + l["avatar"] if l.get("avatar") else '',
                    "image_url": constants.QINIU_URL_PREFIX + l["index_image_url"] if l.get("index_image_url") else ''
                }
                data.append(house)
        return self.write(dict(errcode=RET.OK, errmsg='OK', data=data, total_page=total_page))


class HouseRedisListHandelr(BaseHandler):

    def get(self, *args, **kwargs):
        '''

        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
        '''
        area_id = self.get_argument('aid', '')
        start_date = self.get_argument('sd', '')
        end_date = self.get_argument('ed', '')
        sort_key = self.get_argument('sk', 'new')
        page = self.get_argument('p', '1')
        page = int(page)
        print '==================', page

        # 优先从REDIS中取数据
        try:
            redis_key = 'house_%s_%s_%s_%s' % (start_date, end_date, area_id, sort_key)
            ret = self.redis.hget(redis_key, page)
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
            print 'hite redis', redis_key
            return self.write(ret)

        sql = 'select distinct title,a.house_id,price,room_count,address,order_count,avatar,index_image_url,a.ctime,telephone,qqnum from house_info a inner join user_profile b on house_user_id =user_id  '
        sql_total_count = 'select count(distinct a.house_id) count from house_info a inner join user_profile b on house_user_id =user_id left join order_info c on a.house_id=c.house_id'

        sql_where = []  # 用来保存sql语句的where条件
        sql_params = {}  # 用来保存sql查询所需的动态数据

        if start_date and end_date:
            sql_part = "((begin_date>%(end_date)s or end_date<%(start_date)s) " \
                       "or (begin_date is null and end_date is null))"
            sql_where.append(sql_part)
            sql_params["start_date"] = start_date
            sql_params["end_date"] = end_date
        elif start_date:
            sql_part = "(end_date<%(start_date)s or (begin_date is null and end_date is null))"
            sql_where.append(sql_part)
            sql_params["start_date"] = start_date
        elif end_date:
            sql_part = "(begin_date>%(end_date)s or (begin_date is null and end_date is null))"
            sql_where.append(sql_part)
            sql_params["end_date"] = end_date
        if area_id:
            sql_area = 'house_area_id=%(area_id)s'
            sql_where.append(sql_area)
            sql_params["area_id"] = area_id
        if sql_where:
            sql += ' where '
            sql += ' and '.join(sql_where)
            sql_total_count += ' where '
            sql_total_count += ' and '.join(sql_where)
        try:
            ret = self.db.get(sql_total_count, **sql_params)
        except Exception as e:
            logging.error(e)
            total_page = -1
        else:
            print ret
            total_page = int(math.ceil(ret["count"] / float(constants.HOUSE_LIST_PAGE_CAPACITY)))

        if page > total_page:
            return self.write(dict(errcode=RET.OK, errmsg='没有数据', data=[], total_page=total_page))
        # 排序
        if sort_key == 'new':
            sql += ' order by a.ctime desc'
        elif sort_key == 'booking':
            sql += ' order by order_count desc'
        elif sort_key == 'price-inc':
            sql += ' order by price asc'
        elif sort_key == 'price-des':
            sql += ' order by price desc'

        # 分页
        # if page == 1:
        #     sql += ' limit %s' % constants.HOUSE_LIST_PAGE_CAPACITY
        # else:
        #     sql += ' limit %s ,%s' % (
        #         (page - 1) * constants.HOUSE_LIST_PAGE_CAPACITY, constants.HOUSE_LIST_PAGE_CAPACITY)
        print sql
        print area_id
        print sql_params

        # 查询数据
        try:
            ret = self.db.query(sql, **sql_params)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='访问数据库出错'))
        data = []
        if ret:
            # print len(ret),'===================='
            for l in ret:
                house = {
                    "house_id": l["house_id"],
                    "title": l["title"],
                    "price": l["price"],
                    "room_count": l["room_count"],
                    "address": l["address"],
                    "order_count": l["order_count"],
                    "telephone": l["telephone"],
                    "qqnum": l["qqnum"],
                    "avatar": constants.QINIU_URL_PREFIX + l["avatar"] if l.get("avatar") else '',
                    "image_url": constants.QINIU_URL_PREFIX + l["index_image_url"] if l.get("index_image_url") else ''
                }
                data.append(house)
        print data
        # current_page_data=data[ :constants.HOUSE_LIST_PAGE_CAPACITY*page]
        house_data = {}
        # house_data[page]=json.dumps(dict(errcode=RET.OK,errmsg='OK',data=current_page_data,total_page=total_page))
        # 多出来的数据存到redis
        i = 0
        while 1:
            page_data = data[constants.HOUSE_LIST_PAGE_CAPACITY * (i):constants.HOUSE_LIST_PAGE_CAPACITY * (i + 1)]
            if not page_data:
                break
            # print page_data
            house_data[i + 1] = json.dumps(dict(errcode=RET.OK, errmsg='OK', data=page_data, total_page=total_page))
            i += 1
        # print len(data)
        # print data
        # print house_data
        try:
            redis_key = 'house_%s_%s_%s_%s' % (start_date, end_date, area_id, sort_key)
            self.redis.hmset(redis_key, house_data)
            self.redis.expire(redis_key, constants.REDIS_HOUSE_LIST_EXPIRES_SECONDS)
        except Exception as e:
            logging.error(e)

        return self.write(house_data[page])
