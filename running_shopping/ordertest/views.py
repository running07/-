# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse
from usertest.models import UserInfo, UserAddressInfo, AreaInfo
from goodstest.models import GoodsInfo
from carttest.models import CartInfo
from ordertest.models import OrderInfo, OrderDetailInfo
import time
import random
from django.db import transaction
from usertest.user_decorate import login_fun


@login_fun
def place_order(request):
    pid = request.session.get('pid')

    # 收货地址，默认为默认地址，更改地址存到session shipping_address中
    if request.session.has_key('shipping_address'):
        default_id = request.session.get('shipping_address')
    else:
        default_id = UserInfo.user.get(pk=pid).default_id
    print 'pid========', pid
    address_info = UserAddressInfo.useraddress.get(pk=default_id)
    pro = AreaInfo.objects.get(pk=address_info.upro).atitle
    city = AreaInfo.objects.get(pk=address_info.ucity).atitle
    disc = AreaInfo.objects.get(pk=address_info.udisc).atitle
    # 构建默认地址
    address = pro + city + disc + address_info.uaddress
    # 构建其他地址
    useraddressinfos = UserAddressInfo.useraddress.filter(userid_id=pid).exclude(pk=default_id)
    address_list = []
    for item in useraddressinfos:
        print 'item-id==========', item.pk, item.udisc
    for item in useraddressinfos:
        pro = AreaInfo.objects.get(pk=item.upro).atitle
        city = AreaInfo.objects.get(pk=item.ucity).atitle
        disc = AreaInfo.objects.get(pk=item.udisc).atitle
        uaddress = pro + city + disc + item.uaddress
        urecipients = item.urecipients
        uaddphone = item.uaddphone
        another_name = item.another_name
        pk = item.pk
        # 构建其他地址
        address_list.append(
            {'another_name': another_name, 'uaddress': uaddress, 'urecipients': urecipients, 'uaddphone': uaddphone,
             'pk': pk, })
    # 购物车提交商品
    gid = request.GET.get('gid','')
    if gid!='':

        #立即购买
        gid = request.GET.get('gid')
        num = request.GET.get('num')
        num = int(num)
        print '==========type num', type(num)
        goods = GoodsInfo.goods.get(pk=gid)
        totalmoney = goods.gprice * num
        count = 1
        total_list = ''
        carts = ''
        flag = 1
    else:
        #购物车
        idstr = request.COOKIES.get('orderids')
        ids = idstr.split(',')
        print 'ids->', ids
        list = []
        for i in ids:
            if i:
                list.append(i)
        carts = CartInfo.objects.filter(pk__in=list).order_by('-pk')
        count = len(carts)
        total_list = []
        totalmoney = 0
        for cart in carts:
            money = cart.cgoods.gprice * cart.count
            total_list.insert(0, money)
            totalmoney += money
        goods = ''
        num = ''
        flag = 0
    # 商品详情提交订单
    context = {'title': '提交订单',
               'address_info': address_info,
               'address_list': address_list,
               'address': address,
               'carts': carts,
               'total_list': total_list,
               'count': count,
               'totalmoney': totalmoney,
               'goods': goods,
               'num': num,
               'flag': flag,
               }
    return render(request, 'ordertest/place_order.html', context)

#/order/order_hander/?flag={{ flag }}&gid={{ goods.pk }}&num={{ num }}
#按钮，提交订单
#cflag 是否提交订单
#flag为购买方式，购物车flag=0和立即购买flag=1
#购物车付款失败，订单为为未付款，确认为已支付
#立即购买，确认为付款，提交订单，订单状态为已支付，不确认，跳到物品详情
@transaction.atomic()
@login_fun
def order_hander(request):
    pid = request.session.get('pid')
    # 用户是否确认付款，否，则为支付
    cflag = request.COOKIES.get('flag')
    print cflag
    if cflag == 'true':
        cflag = 1
    else:
        cflag = 0
    flag = request.GET.get('flag')
    gid=request.GET.get('gid')
    num=request.GET.get('num')

    # 地址id
    if request.session.has_key('shipping_address'):
        default_id = request.session.get('shipping_address')
    else:
        default_id = UserInfo.user.get(pk=pid).default_id
    # 商品


    print '------------flag',flag
    #flag 为购物状态，0 代表购物车购买，1 代表立即购买
    #cfalg 为是否付款，1 表示付款，0 表示为付款
    if flag == u'0':
        # 设置日志段点
        # 购物车购买方式
        tran_id = transaction.savepoint()
        try:
            idstr = request.COOKIES.get('orderids')
            ids = idstr.split(',')

            list = []
            for i in ids:
                if i:
                    list.append(int(i))
            carts = CartInfo.objects.filter(pk__in=list)
            print 'list id->', list

            # 订单
            order = OrderInfo()
            id1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
            id2 = str(random.randrange(1000, 9999))
            oid = id1 + id2
            order.oid = oid
            # order.odate =
            order.statu = cflag
            order.oaddress_id = default_id
            order.ouser_id = pid
            order.save()


            # 订单详情
            totalmoney = 0
            # count = len(carts)
            for cart in carts:
                orderdatail = OrderDetailInfo()
                orderdatail.goods = cart.cgoods
                orderdatail.money = cart.cgoods.gprice * cart.count
                orderdatail.count = cart.count
                orderdatail.order_id = oid
                totalmoney += orderdatail.money
                orderdatail.save()

            order = OrderInfo.objects.get(oid=oid)
            order.omoney = totalmoney
            order.save()

            # 删除购物车信息

            for id in list:
                CartInfo.objects.get(pk=id).delete()

            # transaction.savepoint_commit(tran_id)
        except Exception as e:
            print '======e.message', e
            transaction.savepoint_rollback(tran_id)
            return redirect('carttest:cart')
        else:
            print u'提交'
            transaction.savepoint_commit(tran_id)
        return redirect('usertest:order')
    else:
        # 立即购买方式
        if cflag:
            # 订单
            order = OrderInfo()
            id1 = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
            id2 = str(random.randrange(1000, 9999))
            oid = id1 + id2
            order.oid = oid
            # order.odate =
            order.statu = cflag
            order.oaddress_id = default_id
            order.ouser_id = pid
            order.save()

            #订单详情

            orderdatail = OrderDetailInfo()
            goods=GoodsInfo.goods.get(pk=gid)
            orderdatail.goods =goods
            orderdatail.money = goods.gprice *int(num)
            orderdatail.count = 1
            orderdatail.order_id = oid
            totalmoney = goods.gprice *int(num)
            orderdatail.save()
            order = OrderInfo.objects.get(oid=oid)
            order.omoney = totalmoney
            order.save()
            return redirect('/user/order?statu=1')
        else:
            return redirect('/detail_'+gid)


# 改变收货地址
def alter_site(request):
    shipping_address = request.POST.get('site')
    print 'shipping_address', shipping_address
    request.session['shipping_address'] = shipping_address
    gid=request.GET.get('gid','')
    num=request.GET.get('num','')
    return redirect('/order?gid='+gid+'&num='+num)


# 商品详情页立即购买
@login_fun
def detail_order(request):
    # gid = request.GET.get('gid')
    # num = request.GET.get('num')
    # pid = request.session.get('pid')
    # cart = CartInfo()
    # cart.cuser_id = pid
    # cart.cgoods_id = int(gid)
    # cart.count = int(num)
    # cart.save()
    # cid=cart.pk

    print 'detail_order================='
    return JsonResponse({'cid': 1})
