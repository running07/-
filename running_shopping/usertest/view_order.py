# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from usertest.models import UserAddressInfo, UserInfo, AreaInfo
from goodstest.models import CommentInfo
from goodstest.models import GoodsInfo
from ordertest.models import OrderDetailInfo, OrderInfo
from user_decorate import login_fun
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.paginator import Paginator


@login_fun
def info(request):
    # 用户信息
    userid = request.session.get('pid')
    default_id = UserInfo.user.get(pk=userid).default_id
    if default_id != 0:
        cuseraddress = UserAddressInfo.useraddress.get(pk=default_id)
        pro = AreaInfo.objects.get(pk=cuseraddress.upro).atitle
        city = AreaInfo.objects.get(pk=cuseraddress.ucity).atitle
        disc = AreaInfo.objects.get(pk=cuseraddress.udisc).atitle
        address = pro + city + disc + cuseraddress.uaddress

    else:
        cuseraddress = ''
        address = ''
    user = UserInfo.user.get(pk=userid)

    # 最近浏览
    goodsids = user.goodsids
    id_list = goodsids.split(',')
    print '=================id_list', id_list
    # id_list = request.session.get('id_list', [])
    goods_list = []
    for id in id_list:
        if id:
            goods = GoodsInfo.goods.get(pk=id)
            goods_list.append(goods)
    # goods_list=GoodsInfo.goods.filter(pk__in=id_list)
    context = {'user': user, 'addressinfo': cuseraddress, 'address': address, 'goods_list': goods_list}
    return render(request, 'usertest/user_center_info.html', context)


@login_fun
def order(request):
    pid = request.session.get('pid')
    # 获取当前页数
    pag = request.GET.get('pag', 1)
    statu = request.GET.get('statu', u'0')
    sort_bar = [{'id': u'0', 'name': u'待付款'}, {'id': u'1', 'name': u'待收货'},
                {'id': u'2', 'name': u'待评价'}, {'id': u'3', 'name': u'已完成'}]
    orderlist = OrderInfo.objects.filter(ouser_id=pid, statu=statu).order_by('-odate')
    # 创建分页对象，每页两个数据
    paginator = Paginator(orderlist, 2)
    page = paginator.page(pag)
    # length=page.len()
    orderinfo = page.object_list
    address_list = []
    # 组合收货地址
    for item in orderinfo:
        oaddress = item.oaddress
        pro_id = oaddress.upro
        city_id = oaddress.ucity
        disc_id = oaddress.udisc
        pro = AreaInfo.objects.get(pk=pro_id).atitle
        city = AreaInfo.objects.get(pk=city_id).atitle
        disc = AreaInfo.objects.get(pk=disc_id).atitle
        uaddress = oaddress.uaddress
        address = pro + city + disc + uaddress
        address_list.insert(0, address)

    # 根据页数，设置分页跳转样式
    pagenum = paginator.num_pages - 4
    range_page = [1, 2, 3, 4, 5, 6]
    if page.number < pagenum:
        range_page2 = range(page.number, page.number + 4)
    else:
        range_page2 = range(paginator.num_pages - 4, paginator.num_pages + 1)

    context = {'paginator': paginator,
               'page': page,
               'pagenum': pagenum,
               'range_page': range_page,
               'range_page2': range_page2,
               'address_list': address_list,
               'sort_bar': sort_bar,
               'statu': statu,

               }

    return render(request, 'usertest/user_center_order.html', context)


# 提交订单
def ordersubmit(request):
    oid = request.GET.get('oid')

    order = OrderInfo.objects.get(oid=oid)
    order.statu += 1
    order.save()
    return JsonResponse({'statu': order.statu})
    # return response


# 添加评价
def addcomment(request):
    oid = request.GET.get('oid')
    order = OrderInfo.objects.get(oid=oid)
    orderdetails = order.orderdetailinfo_set.all()
    data = []
    comment_ids = []
    for detail in orderdetails:
        id = detail.goods.pk
        title = detail.goods.gtitle
        comment_ids.append(id)
        data.append({'id': id, 'title': title})
    # data=1
    request.session['comment_ids'] = comment_ids
    return JsonResponse({'data': data})


# 保存评论
def save_comment(request):
    oid = request.POST.get('oid')
    print 'save_comment', oid
    order = OrderInfo.objects.get(oid=oid)
    order.statu = 3
    order.save()
    orderdetails = order.orderdetailinfo_set.all()
    pid = request.session.get('pid')
    for detail in orderdetails:
        id = detail.goods.pk
        print '==============id', id
        id = str(id)
        comment = CommentInfo()
        comment.content = request.POST.get(id)
        grade = request.POST.get('gid' + id)
        comment.grade = grade
        print '============grade', grade
        comment.goods_id = id
        comment.user_id = pid
        comment.save()
    return redirect('/user/order/?statu=3')


# 删除订单
def delete_order(request):
    try:
        oid = request.GET.get('oid')
        OrderInfo.objects.get(oid=oid).delete()
    except Exception as e:
        flag = 0
    else:
        flag = 1
    return JsonResponse({'flag': flag})


@login_fun
def site(request):
    # 设为默认地址

    userid = request.session.get('pid')
    cuser = UserInfo.user.get(pk=userid)
    id = request.COOKIES.get('address_id')
    print 'type  id->', type(id)
    if id:
        cuser.default_id = id
        cuser.save()

    # 默认地址
    userid = request.session.get('pid')
    default_id = UserInfo.user.get(pk=userid).default_id
    if default_id != 0:
        cuseraddress = UserAddressInfo.useraddress.get(pk=default_id)
        pro = AreaInfo.objects.get(pk=cuseraddress.upro).atitle
        city = AreaInfo.objects.get(pk=cuseraddress.ucity).atitle
        disc = AreaInfo.objects.get(pk=cuseraddress.udisc).atitle
        caddress = pro + city + disc + cuseraddress.uaddress
    else:
        cuseraddress = ''
        caddress = ''
    print 'caddress->', caddress

    # 其他地址
    useraddressinfos = UserAddressInfo.useraddress.filter(userid_id=userid).exclude(pk=default_id)
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
        address_list.append(
            {'another_name': another_name, 'uaddress': uaddress, 'urecipients': urecipients, 'uaddphone': uaddphone,
             'pk': pk, })

    context = {"address_list": address_list, "cuseraddress": cuseraddress, 'caddress': caddress}
    return render(request, 'usertest/user_center_site.html', context)


# 新增地址
def site_hander(request):
    # 用POST获得三级地址，市区市动态创建的，获取不到，所以把三级地址，保存在cookies中
    # pro_id = request.COOKIES.get('pro_id')
    # city_id = request.COOKIES.get('city_id')
    # disc_id = request.COOKIES.get('disc_id')
    # pro = AreaInfo.objects.get(pk=pro_id).atitle
    # city = AreaInfo.objects.get(pk=city_id).atitle
    # disc = AreaInfo.objects.get(pk=disc_id).atitle
    pro_id = request.POST.get('pro_id')
    city_id = request.POST.get('city_id')
    disc_id = request.POST.get('disc_id')
    another_name = request.POST.get('another_name')
    urecipients = request.POST.get('urecipients')
    uaddress = request.POST.get('uaddress')
    upostcode = request.POST.get('upostcode')
    uaddphone = request.POST.get('uaddphone')
    # uaddress = pro + city + disc + uaddress
    userid = request.session.get('pid')

    # print 'address', userid
    useraddress = UserAddressInfo.museraddress.create_useraddress(another_name, urecipients,
                                                                  pro_id, city_id, disc_id, uaddress, upostcode,
                                                                  uaddphone, userid)
    # 如果没有默认地址，新增地址设为默认地址
    cuser = UserInfo.user.get(pk=userid)
    if cuser.default_id == 0:
        print 'default_id'
        cuser.default_id = useraddress.pk
        cuser.save()
    # response = HttpResponseRedirect('/user/site')
    # if not request.COOKIES.has_key('address_id'):
    #     response.set_cookie('address_id', useraddress.pk)
    # request.session.get('address_id',useraddress.pk)
    return redirect('usertest:site')


# 设置默认地址
def set_default(request, id):
    userid = request.session.get('pid')
    cuser = UserInfo.user.get(pk=userid)
    id = int(id)
    print 'type  id->', type(id)
    cuser.default_id = id
    cuser.save()
    return JsonResponse({'user': userid, "default_id": id})


# #获取同级下的城市信息
# def city(request,id):
#     id=int(id)
#     aparea_id=AreaInfo.objects.get(pk=id).aParea_id
#     prolist = AreaInfo.objects.filter(aParea_id=aparea_id)
#     list = []
#     for item in prolist:
#         id = item.pk
#         title = item.atitle
#         list.append([id, title])
#     return JsonResponse({'data': list})

# 保存修改后的地址信息
def site_modify(request):
    # 被修改地址的pk
    modify_id = request.session.get('modify_id')
    modify_id = int(modify_id)
    pid = request.session.get('pid')
    default_id = UserInfo.user.get(pk=pid).default_id
    modify_address = UserAddressInfo.useraddress.get(pk=modify_id)
    modify_address.another_name = request.POST.get('another_name')
    modify_address.urecipients = request.POST.get('urecipients')
    modify_address.upro = request.POST.get('pro_id')
    modify_address.ucity = request.POST.get('city_id')
    modify_address.udisc = request.POST.get('disc_id')
    modify_address.uaddress = request.POST.get('uaddress')
    modify_address.upostcode = request.POST.get('upostcode')
    modify_address.uaddphone = request.POST.get('uaddphone')
    modify_address.save()
    print type(modify_id), type(default_id)
    print 'modify_id', modify_id, 'default_id', default_id
    gid = request.GET.get('gid', '')
    num = request.GET.get('num', '')

    if request.GET.has_key('order'):
        return redirect('/order?gid=' + gid + '&num=' + num)
    else:
        return redirect('usertest:site')


# jaax 获取被修改地址的信息，存到JsonResponse
def useraddress(request, id):
    address = UserAddressInfo.useraddress.get(pk=id)
    another_name = address.another_name
    urecipients = address.urecipients
    upro = address.upro
    ucity = address.ucity
    udisc = address.udisc
    uaddress = address.uaddress
    upostcode = address.upostcode
    uaddphone = address.uaddphone
    upro_name = AreaInfo.objects.get(pk=upro).atitle
    ucity_name = AreaInfo.objects.get(pk=ucity).atitle
    udisc_name = AreaInfo.objects.get(pk=udisc).atitle
    content = {'another_name': another_name, 'urecipients': urecipients, 'upro': upro,
               'upro_name': upro_name, 'ucity': ucity, 'ucity_name': ucity_name, 'udisc': udisc,
               'udisc_name': udisc_name, "uaddress": uaddress, 'upostcode': upostcode, 'uaddphone': uaddphone}
    request.session['modify_id'] = id
    return JsonResponse(content)


# 三级联动
# def index2(request):
#     return render(request, 'areatest/index2.html')

# 把筛选数据传到网页中，在jquery $.get()调用
def getarea1(request):
    prolist = AreaInfo.objects.filter(aParea__isnull=True)
    list = []
    for item in prolist:
        id = item.id
        title = item.atitle
        list.append([id, title])
    return JsonResponse({'data': list})


# 把筛选数据传到网页中，在jquery $.get()调用
def getarea2(request, pid):
    prolist = AreaInfo.objects.filter(aParea_id=pid)
    list = []
    for item in prolist:
        id = item.pk
        title = item.atitle
        list.append([id, title])
    return JsonResponse({'data': list})


def address(request):
    pro_id = request.COOKIES.get('pro_id')
    city_id = request.COOKIES.get('city_id')
    disc_id = request.COOKIES.get('disc_id')
    print pro_id, city_id, disc_id
    return JsonResponse({'HAH': pro_id})
