# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect


# 装饰器，根据用户登录状态，实现页面跳转
def login_fun(func):
    def wrapper(request, *args, **kwargs):
        # 用户登录，
        if request.session.has_key('pid'):
            return func(request, *args, **kwargs)
        # 用户没有登录，跳转到登录页面
        else:
            url = request.get_full_path()
            response = HttpResponseRedirect('/user/login')
            # 设置当前url,登录户，跳转到当前url
            response.set_cookie('url', url)
            return response

    return wrapper
