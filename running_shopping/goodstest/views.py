# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from goodstest.models import CategoryInfo, GoodsInfo, CommentInfo
from usertest.models import UserInfo
from django.http import Http404
from django.views.decorators.cache import cache_page


# 主页，显示所有类别商品，
# 缓存 15分钟
@cache_page(60 * 15)
def index(request):
    content = []
    # 从数据库取数据
    for i in range(1, 6):
        # 最新商品，最热商品
        latest_type = GoodsInfo.goods.filter(gtype_id=i).order_by('-pk')[0:3]
        hottest_type = GoodsInfo.goods.filter(gtype_id=i).order_by('-gclick')[0:4]
        # 商品类别
        list_title = CategoryInfo.category.filter(pk=i)[0].ttitle
        # 保证和前端数据格式一致
        model = 'model0' + str(i)
        href = 'list_' + str(i)
        banner = '/static/images/banner0' + str(i) + '.jpg'
        content.append({'latest_type': latest_type, 'hottest_type': hottest_type,
                        'list_title': list_title, 'model': model, 'href': href, 'banner': banner})
    context = {"content": content, 'title': '主页'}

    return render(request, 'goodstest/index.html', context)


# 商品列表，展示该类的所有商品
def listgoods(request, type):
    # a = 1 + 'a'
    # print 'type=',type,'page=',page,'rank=',rank

    # 从url中取页数和排序规则，默认从第一页开始，默认按商品添加顺序排序
    page_num = request.GET.get('page', 1)
    rank = request.GET.get('rank', u'0')
    # print 'type=', type, 'page=', page_num, 'rank=', rank
    # rank 0： 最新     1：价格    2：点击量
    if rank == u'0':
        order = '-pk'
    elif rank == u'1':
        order = 'gprice'
    else:
        order = '-gclick'
    sort_bar = [{'id': u'0', 'name': '默认'}, {'id': u'1', 'name': '价格'}, {'id': u'2', 'name': '人气'}]

    # 新品推荐
    latest_type = GoodsInfo.goods.filter(gtype_id=type).order_by('-gclick')[0:3]
    # 商品类别
    title = CategoryInfo.category.filter(pk=type)[0].ttitle
    # 符合类别并对商品进行排序
    goods_list = GoodsInfo.goods.filter(gtype_id=type).order_by(order)
    # 建立分页对象，每页显示15个商品
    paginator = Paginator(goods_list, 15)
    # 当前页
    page = paginator.page(page_num)

    # 按页数建立不同样式分页导航
    pagenum = paginator.num_pages - 4
    range_page = [1, 2, 3, 4, 5, 6]
    if page.number < pagenum:
        range_page2 = range(page.number, page.number + 4)
    else:
        range_page2 = range(paginator.num_pages - 4, paginator.num_pages + 1)
    print '***********************************************************************'
    print '===========================', pagenum, range_page2
    context = {'title': title, 'type': type, 'rank': rank, 'paginator': paginator,
               'page': page, 'sort_bar': sort_bar, 'latest_type': latest_type, "range_page": range_page,
               'range_page2': range_page2, 'pagenum': pagenum}
    return render(request, 'goodstest/list.html', context)


# 商品详情，展示商品详细信息
def detail(request, id):
    goods = GoodsInfo.goods.filter(pk=id)[0]
    # 点击量+1
    if 'page' not in request.get_full_path():
        goods.gclick += 1
        goods.save()
    print goods.gtype.ttitle
    goods_list = GoodsInfo.goods.filter(gstore=goods.gstore).exclude(pk=id).order_by('-gclick')[0:2]
    # print '================================',goods_list[0].gtitle,goods_list[1].gtitle

    # 保存最近浏览，若没有登录保存到session里，登录，把session信息存入数据库，清除session信息，
    # 用户已经登录
    if request.session.has_key('pid'):
        pid = request.session.get('pid')
        user = UserInfo.user.get(pk=pid)
        goodsids = user.goodsids
        # if goodsids==0:
        #     goodsids=''
        goodsid_list = goodsids.split(',')

        # 若现在浏览的商品在最近浏览中，则移除该商品，添加到最前面
        if id in goodsid_list:
            goodsid_list.remove(id)
        goodsid_list.insert(0, id)

        if len(goodsid_list) > 5:
            goodsid_list = goodsid_list[0:5]

        # 用户表中的goodsids保存最近浏览的商品，
        # 每个商品用逗号隔开
        ids = ''
        for index in goodsid_list:
            ids = ids + str(index) + ','
        ids = ids[:-1]
        user.goodsids = ids
        user.save()
    # 用户没有登录，保存到session 中，保存类型为列表
    else:
        id_list = request.session.get('id_list', [])

        if id in id_list:
            id_list.remove(id)
            id_list.insert(0, id)
        else:
            id_list.insert(0, id)

        if len(id_list) > 5:
            id_list.pop()

        request.session['id_list'] = id_list
        print '没有登录,csession->', id_list

    # 评论
    grade = request.GET.get('grade', 3)
    gradelist = []
    # 商品评分，0  零颗星，一颗星，差评
    # 1    二颗星  三颗星     中评
    # 2     四颗星     五颗星     好评
    # 3  全部评价
    if grade == u'0':
        gradelist = [0, 1]
        current_grade = 0
    elif grade == u'1':
        gradelist = [2, 3]
        current_grade = 1
    elif grade == u'2':
        gradelist = [4, 5]
        current_grade = 2
    else:
        gradelist = [0, 1, 2, 3, 4, 5]
        current_grade = 3
    totalnum = CommentInfo.objects.filter(goods_id=id, grade__in=[0, 1, 2, 3, 4, 5]).count()
    num0 = CommentInfo.objects.filter(goods_id=id, grade__in=[0, 1]).count()
    num1 = CommentInfo.objects.filter(goods_id=id, grade__in=[2, 3]).count()
    num2 = CommentInfo.objects.filter(goods_id=id, grade__in=[4, 5]).count()
    discuss_tar = [{'id': 3, 'name': '全部评价', 'num': ''},
                   {'id': 2, 'name': '好评(' + str(num2) + ')'},
                   {'id': 1, 'name': '中评(' + str(num1) + ')'},
                   {'id': 0, 'name': '差评(' + str(num0) + ')'},
                   ]
    # 按要求从数据库中取数据，并按时间排序
    comments = CommentInfo.objects.filter(goods_id=id, grade__in=gradelist).order_by('-time')
    # 建立分页对象，没有四条评论
    paginator = Paginator(comments, 4)
    pag = request.GET.get('page', 1)
    page = paginator.page(pag)

    # 构造分页导航格式
    pagenum = paginator.num_pages - 4
    range_page = [1, 2, 3, 4, 5, 6]
    if page.number < pagenum:
        range_page2 = range(page.number, page.number + 4)
    else:
        range_page2 = range(paginator.num_pages - 4, paginator.num_pages + 1)

    context = {'title': '商品详情', 'goods': goods, 'goods_list': goods_list, 'page': page,
               'range_page': range_page, 'range_page2': range_page2, 'paginator': paginator,
               'discuss_tar': discuss_tar, 'current_grade': current_grade, 'totalnum': totalnum
               }

    return render(request, 'goodstest/detail.html', context)

# 评论认同量加一
def addlike(request):
    cid = request.GET.get('cid')
    comments = CommentInfo.objects.get(pk=cid)
    comments.likenum = comments.likenum + 1
    comments.save()
    return JsonResponse({'flag': 1})

# 不认同评论量加一
def adddislike(request):
    cid = request.GET.get('cid')
    comments = CommentInfo.objects.get(pk=cid)
    comments.dislikenum = comments.dislikenum + 1
    comments.save()
    return JsonResponse({'flag': 1})





from haystack.views import SearchView

class MySearchView(SearchView):
    # 重写 SearchView
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        # rank = self.request.GET.get('rank', u'0')
        # # print 'type=', type, 'page=', page_num, 'rank=', rank
        #

        # context['facets'] = self.results.order_by(order)
        (paginator, page) = self.build_page()
        pagenum = paginator.num_pages - 4

        range_page = [1, 2, 3, 4, 5, 6]
        if page.number < pagenum:
            range_page2 = range(page.number, page.number + 4)
        else:
            range_page2 = range(paginator.num_pages - 4, paginator.num_pages + 1)

        # pagerange=paginator.page_range
        pag = self.request.GET.get('page', 1)
        rank = self.request.GET.get('rank', u'0')

        objectlist = []
        for item in self.results:
            objectlist.append(item.object)

        objectset = set(objectlist)
        objectlist = list(objectset)
        print '=========itemlen', len(objectlist)
        latest_type = sorted(objectlist, key=lambda item: item.gclick, reverse=True)[0:3]
        if rank == u'0':
            order = 'pk'
            objectlist = sorted(objectlist, key=lambda item: item.pk)
        elif rank == u'1':
            order = 'price'
            objectlist = sorted(objectlist, key=lambda item: item.gprice, reverse=True)
        else:
            order = 'click'
            objectlist = sorted(objectlist, key=lambda item: item.gclick, reverse=True)
        sort_bar = [{'id': u'0', 'name': '默认'}, {'id': u'1', 'name': '价格'}, {'id': u'2', 'name': '人气'}]

        print order
        for item in objectlist:
            print item.gprice

        paginator = Paginator(objectlist, 2)
        page = paginator.page(pag)

        context['title'] = '搜索'
        context['range_page'] = range_page
        context['range_page2'] = range_page2
        context['paginator'] = paginator
        context['page'] = page
        context['sort_bar'] = sort_bar
        context['rank'] = rank
        context['latest_type'] = latest_type

        return context
