# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views, view_order

urlpatterns = [
    # 购物车
    url(r'^$', views.cart, name='cart'),
    # 添加商品
    url(r'addcart(\d+)_(\d+)/$', views.addcart, name='addcart'),
    # 输出用户所以商品
    url(r'^item/$', views.item),
    # 增加或减少商品数量
    url(r'^alter(\d+)_(\d+)/$', views.alter),
    # blur 输入数据错误
    url(r'^error(\d+)/$', views.error),
    # 删除购物车数据
    url(r'^delete_item(\d+)/$', views.delete_item),
    # 获取用户购物车数量
    url(r'^goods_count/$', views.goods_count),

]
