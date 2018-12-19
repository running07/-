# -*- coding:utf-8 -*-
from django.shortcuts import render
from usertest.models import UserInfo,UserAddressInfo,AreaInfo
from goodstest.models import GoodsInfo
def place_order(request):
    pid = request.session.get('pid')
    default_id=UserInfo.user.get(pk=pid).default_id
    print 'pid========',pid
    address_info=UserAddressInfo.useraddress.get(pk=default_id)
    pro=AreaInfo.objects.get(pk=address_info.upro).atitle
    city = AreaInfo.objects.get(pk=address_info.ucity).atitle
    disc = AreaInfo.objects.get(pk=address_info.udisc).atitle
    address=pro+city+disc+address_info.uaddress
    context={'title_name':'提交订单','address_info':address_info,'address':address}
    return render(request,'carttest/place_order.html',context)