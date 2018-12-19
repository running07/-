# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usertest.models import UserInfo,UserAddressInfo

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','uname','upwd','umail','isDelete']

class UserAddrInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','']


from models import AreaInfo


class AreaInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','atitle']
    # list_filter = ('province',)


admin.site.register(AreaInfo,AreaInfoAdmin)
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(UserAddressInfo)
