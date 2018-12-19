# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from models import CartInfo
from usertest.user_decorate import login_fun


# 添加装饰器，若用户没有登录，跳转到登录页面
@login_fun
def cart(request):
    # 从session信息中取出用户id
    pid = request.session.get('pid')
    carts = CartInfo.objects.filter(cuser_id=pid).order_by('-pk')
    # print '8888888888888888->',len(carts)
    context = {'title': '购物车', 'carts': carts, 'len': len(carts)}
    return render(request, 'carttest/cart.html', context)


# 添加商品
@login_fun
def addcart(request, gid, count):
    if request.session.has_key('pid'):
        gid = int(gid)
        count = int(count)
        # print '================gid count',gid,count
        pid = request.session.get('pid')
        # 查看购物车中是否有同样的商品，
        # 若有，改变购物车商品数量，
        # 没有则创建
        carts = CartInfo.objects.filter(cuser_id=pid, cgoods_id=gid)
        if carts:
            cart = carts[0]
            cart.count += count
        else:
            cart = CartInfo()
            cart.cuser_id = pid
            cart.cgoods_id = gid
            cart.count = count
        cart.save()  # 保存信息
        # 判断请求类型，如是在商品详情页（detail）添加，页面不跳转，
        # 如是在其他页面，页面跳转到购物车页面（cart）
        if request.is_ajax():
            return JsonResponse({'islogin': 1})
        else:
            return HttpResponseRedirect('/cart')
    else:
        return JsonResponse({'islogin': 0})


# 统计用户购物车商品，存到JsonResponse 中
def item(request):
    pid = request.session.get('pid')
    carts = CartInfo.objects.filter(cuser_id=pid)
    list = []
    for cart in carts:
        list.append(cart.pk)

    return JsonResponse({'data': list})


# 购物车商品数量改变，修改数据库信息
def alter(request, id, num):
    id = int(id)
    num = int(num)
    cart = CartInfo.objects.get(pk=id)
    try:
        count1 = cart.count
        cart.count = num

        cart.save()
        data = {'count': 0}
    except Exception as e:
        data = {'count': count1}
    return JsonResponse(data)


# blur 输入数据错误，JsonResponse 保存之前商品数量
def error(request, id):
    count = CartInfo.objects.get(pk=id).count

    return JsonResponse({'count': count})


# 删除购物车信息
def delete_item(request, id):
    id = int(id)
    try:
        print 'begin'
        cart = CartInfo.objects.get(pk=id)
        print cart.pk
        cart.delete()
        print 'delete'
        content = {'flag': 1}
    except Exception as e:
        content = {'flag': 0}

    return JsonResponse(content)


# 获取用户购物车数量
def goods_count(request):
    pid = request.session.get('pid')
    carts = CartInfo.objects.filter(cuser_id=pid)
    return JsonResponse({'count': len(carts)})
