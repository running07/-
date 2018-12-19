# -*- coding:utf-8 -*-
import os
import json
import re
from xpinyin import Pinyin
# DIR='../statics/media/'
# for filename in os.listdir(DIR):
#     filename=DIR+filename
#     print filename
# name='statics/media/cjsh.jpg'
# if 'cjsh'in name:
#     print 'ok'
# else:
#     print 'error'






# python_data={'name':"nana","age":12,"address":"address"}
#
list=[{'url': 'http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or47GkHeRPmWGCCUCP1GBT1rz2LseRQgxZnz7IibHlAetFwOpmjE7brOicseVsiaa89nIYGn07n0bWkrA/0?wx_fmt=jpeg', 'update_time': 1541745400, 'media_id': 'Zbt0iqj8qETurZYfjdSMi7GOz-yaQjZt63EbBBM56iw', 'name': 'statics/media/lp.jpg'}]

print len(list)
for i in list:
    print i
item_dict={'item':list}
with open('../media_id2.json','w')as json_dict:
    json.dump(item_dict,json_dict,ensure_ascii=False)
item_dict='''
{
    "item":[
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi33frPr6PD5PwbxVmGuveoM",
            "name":"statics/media/smy.jpg",
            "update_time":1541814342,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ99l651r3qrxUkMbaaAMhRt40pG6jQWONkhzukGWibdvWelBI8oNzfHrA/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi_XTrAAWoisTXZ-QGuh0LG0",
            "name":"statics/media/wzj.jpg",
            "update_time":1541814341,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9zNXrUzoIm5oW4u3A4WmaWm0ibFgaGPmibXLI7HDaJln5Dk2ny4TCaaJQ/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMizUZDIGh-B6APIobWz1sr_Q",
            "name":"statics/media/nkll.jpg",
            "update_time":1541814341,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ98R9jjklnFF3ZOl0mjRoibE50ibtwK1vaQStHZ9j2hicW9PicMArViazM8gA/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi-WmUvJIFAkN1S6y-ZkDiEo",
            "name":"statics/media/sc.jpg",
            "update_time":1541814340,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9WuSqFzDrLQRGLzmwdkVibkfas3vfuaXhcddkHoKPUiaGwjCbOEEtFSGA/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi1NpbyqGCtgEITMjDveYXf0",
            "name":"statics/media/k.jpg",
            "update_time":1541814339,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9abAlnIwsmJV2pvhohAibEtnG3PiaAsicyZzyQmS7euzibOXfj4RHPicwfIw/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMiwvrVfPscQc4G18UjkN7Vbs",
            "name":"statics/media/gjl.jpg",
            "update_time":1541814338,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9V5Giawhx5Z7vWMtyibSxBAQRqQ7hHYLW8lVAbfzY19ZLyKhOlCs7C0fg/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi-pPq4ucpo4FWgSw_mWuK6U",
            "name":"statics/media/pqh.jpg",
            "update_time":1541814337,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9yBrFmIbZIRd2vFvwSiaOUgqicHF2FoXTCicEJcjfHHfJm1QUNE4zfSgTA/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi8a8YY_Ali_lyte1i2S7oN8",
            "name":"statics/media/ys.jpg",
            "update_time":1541814336,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9X3V7vOImU256Uoib0b4R1fgVfY9A5gziaGYMReaiaGFWmG0OaY8icPBjqQ/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi5aT-c5SoDUHiGSF_uxsJkU",
            "name":"statics/media/yg.jpg",
            "update_time":1541814335,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9BENT12TkDJaXIN5xpic2ibCiarSSNWv4DTsqgYXPQgP1hkMoaZ2tBBXKA/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi9qbe-pQt6qEvS6997SHwRk",
            "name":"statics/media/cwj.jpg",
            "update_time":1541814334,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or6GDBShl56Qh1FziaySEuIQ9Dxv2DicxC4y1Vm5XgUXjRJhNHY5BxMQmkan8c3h9TU2suAzgf0b3e3w/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi7GOz-yaQjZt63EbBBM56iw",
            "name":"statics/media/lp.jpg",
            "update_time":1541745400,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or47GkHeRPmWGCCUCP1GBT1rz2LseRQgxZnz7IibHlAetFwOpmjE7brOicseVsiaa89nIYGn07n0bWkrA/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi7xqv8Mn1GFlvYiQDySo_X4",
            "name":"statics/media/my.jpg",
            "update_time":1541745398,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or47GkHeRPmWGCCUCP1GBT1rDSic905o9EZ7Oicwwnyggtf1SnSvXGhaDceT8I1s13wTfdCo211TbK8Q/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMiwySVgB-2knlFIk2Kx_0cZY",
            "name":"statics/media/cjsh.jpg",
            "update_time":1541745397,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or47GkHeRPmWGCCUCP1GBT1rJ74q1QgFMYIWREruAY66ibMu3AG9byspTNrHiaT1Eicxwg7FiaU7TIiagZQ/0?wx_fmt=jpeg"
        },
        {
            "media_id":"Zbt0iqj8qETurZYfjdSMi_4K4P6_z1_78walU7TDrCs",
            "name":"statics/media/gj.jpg",
            "update_time":1541745396,
            "url":"http://mmbiz.qpic.cn/mmbiz_jpg/wXXsibtb5or47GkHeRPmWGCCUCP1GBT1rT6iaJk6uwc2OMEAeC83BtO8rVXd970Mt5PL4IRyvnz8MnACZ0KFJOzA/0?wx_fmt=jpeg"
        }
    ],
    "total_count":14,
    "item_count":14
}'''
print type(item_dict)
# dict_data=json.loads(item_dict)
# print type(dict_data)
# with open('../image_media_id2.json','w')as json_dict:
#     json.dump(item_dict,json_dict,ensure_ascii=False)





# print type(python_data)
# # json.dump(python_data,'data.json')
# with open('data.json', 'w') as json_file:
#     # json_file.write(json.dump(python_data))
#     json.dump(python_data,json_file)
# with open('data.json','r')as json_file:
#     data= json.load(json_file)
#     print type(data)
#     print data
#     if data.get('nam'):
#         print 'ok'
#     else:
#         print 'error'
# pinxin=Pinyin()
# str=u'Lp'
# input_str= pinxin.get_initials(str,u'').lower()
# name='statics/media/lp.jpg'
# pattern=re.compile(r'statics/media/(\w+)')
#
# ret=pattern.search(name)
# if ret:
#     match_str= ret.group(1)
# if match_str==input_str:
#     print 'ok'
# print input_str