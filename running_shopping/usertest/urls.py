# -*- coding:utf-8 -*-
from django.conf.urls import url

from . import views, view_order

urlpatterns = [
    url(r'^login/$', views.login, name='login'),  # 用户登录
    url(r'^login_hander/$', views.login_hander),  # 处理登录
    url(r'^logout/$', views.logout, name='logout'),  # 注销
    url(r'^register/$', views.register, name='register'),  # 注册
    url(r'^base/$', views.base),
    url(r'^register_hander/$', views.register_hander),  # 注册处理
    url(r'^user_exist/$', views.user_exist),

    url(r'^info/$', view_order.info, name='info'),  # 用户中心
    url(r'^order/$', view_order.order, name='order'),  # 用户订单

    url(r'^ordersubmit/$', view_order.ordersubmit),  # 提交订单
    # url(r'^ordersubmit2/$',view_order.ordersubmit2),
    url(r'^site/$', view_order.site, name='site'),  # 收货地址
    url(r'^site_hander/$', view_order.site_hander),  # 处理收货地址
    url(r'^site_modify/$', view_order.site_modify),  # 修还收货地址
    url(r'^address([0-9]+)/$', view_order.useraddress),  # 获取地址信息
    url(r'^set_default([0-9]+)/$', view_order.set_default),  # 设置默认地址

    # 添加评价
    url(r'^addcomment/$', view_order.addcomment),
    url(r'^save_comment/$', view_order.save_comment),
    # 删除订单
    url(r'^delete_order/$', view_order.delete_order),
    # #获取同级下的城市信息
    # url(r'^city([0-9]+)/$',view_order.city()),

    # 三级联动
    # url(r'^index2/$', view_order.index2, name='index2'),
    url(r'^pro/$', view_order.getarea1, name='prolist'),
    url(r'^(?P<pid>\d+)/$', view_order.getarea2),

]
