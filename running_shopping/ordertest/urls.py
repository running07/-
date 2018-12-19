# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^$', views.place_order, name='place_order'),#提交订单
    url(r'^order_hander/$',views.order_hander),#订单处理
    url(r'^alter_site/$',views.alter_site),#改变收货地址
    url(r'^detail_order/$',views.detail_order)#订单详情
]