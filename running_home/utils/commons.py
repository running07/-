# -*- coding:utf-8 -*-
import functools
from running_home.utils.response_code import RET

def request_login(fun):
    @functools.wraps(fun)
    def wrapper(request_handler_obj,*args,**kwargs):
        if not request_handler_obj.get_current_user():
            request_handler_obj.write(dict(errcode=RET.SESSIONERR,errmsg='用户未登录'))
        else:
            fun(request_handler_obj,*args,**kwargs)
    return wrapper