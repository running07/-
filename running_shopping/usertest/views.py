# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from models import UserInfo


def base(request):
    return render(request, 'base_bottom.html')


def login(request):
    uname = request.COOKIES.get('uname', '')
    upwd = request.COOKIES.get('upwd', '')
    name_error = request.COOKIES.get('name_error', 0)
    pwd_error = request.COOKIES.get('pwd_error', 0)
    print '====================', uname, 'a', upwd, 'f', name_error, 'f', pwd_error
    context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'name_error': name_error, 'pwd_error': pwd_error, }
    return render(request, 'usertest/login.html', context)


def login_hander(request):
    # 获取表单提交的信息
    name = request.POST.get('username')
    pwd = request.POST.get('pwd')
    remember = request.POST.get('remember')
    # print 'name', name, 'pwd', pwd

    # 对用户提交的密码，加密
    shal = hashlib.sha1(pwd)
    password = shal.hexdigest()
    # 取出用户信息
    userdata = UserInfo.user.filter(uname=name)
    response = HttpResponseRedirect('/user/login')
    # 判断用户是否是从其他页面重定向到登录页面
    url = request.COOKIES.get('url')
    # pathurl=request.get_full_path()
    # print pathurl,'=========='
    # 若没有，则登录后调转的用户中心
    if not url:
        url = '/user/info'
    # print '****************888888888888', url
    response2 = HttpResponseRedirect(url)
    if userdata:
        name_error = 0

        if password == userdata[0].upwd:
            pwd_error = 0
        else:
            pwd_error = 1
    else:
        name_error = 1
        pwd_error = 1
    response.set_cookie('name_error', name_error)
    response.set_cookie('pwd_error', pwd_error)
    # print '******************', name_error, pwd_error
    if remember == '1':
        print '记录cookie'
        response.set_cookie('uname', name)
        response.set_cookie('upwd', pwd)
        response2.set_cookie('uname', name)
        response2.set_cookie('upwd', pwd)
    else:
        print '删除cookie'
        response.set_cookie('uname', '', max_age=-1)
        response.set_cookie('upwd', '', max_age=-1)
        response2.set_cookie('uname', '', max_age=-1)
        response2.set_cookie('upwd', '', max_age=-1)
    # context = {'title': '登录', 'name_error': name_error, 'pwd_error': pwd_error, 'uname': name, 'upwd': password}
    if name_error == 0 and pwd_error == 0:
        request.session['pid'] = userdata[0].pk
        request.session['uname'] = name
        # 处理最近浏览，
        # 取出用户表存储的最近浏览信息
        user = UserInfo.user.get(pk=userdata[0].pk)
        goodsids = user.goodsids
        goodsid_list = goodsids.split(',')
        try:
            goodsid_list.remove('')
        except Exception as e:
            pass
        # 获取用户登录前，浏览的商品信息
        session_list = request.session.get('id_list', [])
        if len(session_list):
            for i in goodsid_list:
                if i not in session_list:
                    session_list.append(i)
            goodsid_list = session_list
            request.session['id_list'] = []
        if len(goodsid_list) > 5:
            goodsid_list = goodsid_list[0:5]
        # 用户表 和 session 中的信息合并
        ids = ''
        for index in goodsid_list:
            ids = ids + str(index) + ','
        ids = ids[:-1]
        user.goodsids = ids
        user.save()

        return response2
    else:
        return response
        # return redirect('usertest:login',context)


# 用户注销
def logout(request):
    request.session.flush()

    return HttpResponseRedirect('/')


def register(request):
    return render(request, 'usertest/register.html', {'title': '注册'})


def register_hander(request):
    name = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')
    shal = hashlib.sha1(pwd)
    password = shal.hexdigest()
    print password
    UserInfo.muser.create_user(name, password, email)
    return redirect('usertest:login')


# 判断用户是否存在
def user_exist(request):
    name = request.GET.get('name')
    print name
    count = UserInfo.user.filter(uname=name).count()
    print count
    return JsonResponse({'count': count})
