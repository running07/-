# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # 主页
    url(r'^list_([0-9]+)/$', views.listgoods, name='list'),  # 列表页
    url(r'^detail_([0-9]+)/$', views.detail, name='detail'),  # 商品详情页
    url(r'^search/$', views.MySearchView()),  # 商品搜索
    url(r'^addlike/$', views.addlike),
    url(r'^adddislike/$', views.adddislike),

]
