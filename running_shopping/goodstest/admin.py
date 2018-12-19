# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from goodstest.models import CategoryInfo, GoodsInfo,CommentInfo


class GoodCategoryInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ttitle', 'isDelete']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'gtitle','ggoods_info', 'gimage', 'gweight', 'gprice', 'gclick', 'gstore', 'gtype']


class CommentInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','content','goods','user','time','likenum']


admin.site.register(CategoryInfo, GoodCategoryInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
admin.site.register(CommentInfo,CommentInfoAdmin)
