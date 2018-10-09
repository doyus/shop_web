# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2018-08-23 11:35:09
# @Last Modified by:   Marte
# @Last Modified time: 2018-09-28 15:52:13
from django.http import HttpResponse
import os
from django.db.models import Q
from . import settings
import base64
from django.shortcuts import render,redirect
from . models import Shangping
from . models import Yonghu
from . models import Gouwuche
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Count,Min,Max,Sum,Avg
import json
from django.shortcuts import render_to_response
import math
from django.http import HttpResponseRedirect
from .yanzhengma import *
from django.http import JsonResponse
from utils.pay import AliPay
import time

#支付
@csrf_exempt
def get_ali_object():
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2016092100565140"  #  APPID （沙箱应用）

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    # notify_url = "http://47.94.172.250:8804/page2/"
    notify_url = "http://127.0.0.1:8000/page2/"

    # 支付完成后，跳转的地址。
    return_url = "http://127.0.0.1:8000/gouwu/"

    merchant_private_key_path = "keys/app_private_2048.txt" # 应用私钥
    alipay_public_key_path = "keys/alipay_public_2048.txt"  # 支付宝公钥
    # merchant_private_key_path = "keys/pri" # 应用私钥
    # alipay_public_key_path = "keys/pub"  # 支付宝公钥

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay

#支付
@csrf_exempt
def page1(request):
    # 根据当前用户的配置，生成URL，并跳转。
    money = float(request.POST.get('money'))

    alipay = get_ali_object()

    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="京东ceo董宇鹏哈哈哈哈",  # 商品简单描述
        out_trade_no="x2" + str(time.time()),  # 用户购买的商品订单号（每次不一样） 20180301073422891
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）

    return redirect(pay_url)

# 支付
@csrf_exempt
def page2(request):
    alipay = get_ali_object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        # post_dict有10key： 9 ，1
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')

    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        return HttpResponse('支付成功')





#首页地址
def index(req):
    print('来了')
    if req.COOKIES.get('is_log'):
        return render(req,'index2.html')
    else:
        return render(req,'index.html')

# 登路入口
def sign(req):
    return render(req,'sign_in.html')

# 注册入口
def login(req):
    return render(req,'login.html')

# 用户注册
@csrf_exempt
def user_regist(request):
    print('22222222')
    tel = request.POST['tel']
    name = request.POST['name']
    username = request.POST['username']
    pwd = request.POST['pwd']
    sex = request.POST['sex']
    if  Yonghu.objects.filter(username=username) or Yonghu.objects.filter(phone=tel):
        return HttpResponse('注册失败')
    else:
        create = Yonghu.objects.create(phone=tel,name=name,username=username,passwordd=pwd,sex=sex)
        return render(request,'redirect.html')

# 首页登陆以后界面
@csrf_exempt
def user_sign(request):
    if request.method == 'POST':
        x = request.POST['dusername']
        y = request.POST.get('pawd')
        print(x,y)

        if Yonghu.objects.filter(username=x) and Yonghu.objects.filter(passwordd=y):

            response= render_to_response('index2.html', {'doname':x})
            response.set_cookie('is_log','true')
            return response
        else:

            return render(request,'redirect2.html')

# 添加货物demo
@csrf_exempt
def add_goods(request):
    if request.method == "POST":
        price = request.POST['price']
        shop_name = request.POST.get('s_name')
        speck = request.POST.get('s_desc')
        f = request.FILES.get('img')
        filepath = os.path.join(settings.MEDIA_ROOT,f.name)
        print(filepath)
        print(f.name)
        ff = '\static\img\\'+f.name
        print(ff)

        Shangping.objects.create(num=price,name=shop_name,speck=ff,img=speck)
        with open(filepath,'wb') as fp:
            for info in f.chunks():
                fp.write(info)
                return HttpResponse('添加成功')

    else:
        return HttpResponse('上传失败！')
    return render(request,'add_shop.html')

# 添加货物入库
def add_goods_index(request):
    return render(request,'add_shop.html')

# 显示添加的货物demo
@csrf_exempt
def show_goods(request):
    list = Shangping.objects.all()
    lists = []
    for var in list:
        dic = {}
        dic['id1'] = var.name

        dic['id2'] = var.num
        dic['id3'] = var.speck

        dic['id4'] = var.img
        lists.append(dic)
    return render(request,'add_shop.html',{'list':lists})


# 搜索功能
def search(request):
    if request.method == 'GET':
        kname = request.GET.get('nam', '')
        keywords = request.GET.get('keywords', '')
        list = Shangping.objects.filter(Q(name__icontains=keywords)|Q(img__icontains=keywords))

        lists = []
        for var in list:
            dic = {}
            dic['id'] = var.id
            dic['id1'] = var.name
            dic['id2'] = var.num
            dic['id3'] = var.speck

            dic['id4'] = var.img
            lists.append(dic)
        return render(request,'course-list.html',{'list':lists,'kname':kname})


# 购物车显示页
def shopcar(request):
    name = request.GET.get('name2')
    # num = Gouwuche.objects.all()
    num = Gouwuche.objects.filter(go1=name)
    lst = []
    for var in num:
        lst.append(var.gnum)
    print(lst)
    lists = []
    for var in lst:
        dic = {}

        dic['id'] = Shangping.objects.get(id=var).id
        dic['id1'] = Shangping.objects.get(id=var).name #名称
        dic['id2'] = Shangping.objects.get(id=var).num #单价
        dic['id3'] = Shangping.objects.get(id=var).speck #图片


        lists.append(dic)
    # print(lists)
    return render(request,'shopcar.html',{'list':lists,'doname':name})


# 购买页面
def check_out(request):
    id1 = request.GET.get('idd')
    print(id1)
    n = Shangping.objects.get(id=id1)

    print('aaaaaaaaaaaaaaaaaaa')
    print(n)
    id = n.id
    name = n.name
    count = n.num
    img = n.speck
    des = n.img

    return render(request,'shop.html',{'name':name,'count':count,'des':des,'img':img,'id':id})


# 添加到购物车功能
def add_shopcar(request):
    id1 = request.GET.get('idd')
    na = request.GET.get('own')
    try:

        Gouwuche.objects.filter(id=id1).get()
        return render(request,'zhongjian.html',{'t':'（已添加）'})
    except Exception:
        x = request.get_full_path()
        Gouwuche.objects.create(gnum=id1,go1=na,go2='a',go3='a')
        return render(request,'zhongjian.html',{'t':'（已添加）'})

# 结算功能
@csrf_exempt
def jiesuan(request):
    if request.method == "POST":
        price = request.POST.get('dxt')
        price = price.split('-')
        length = len(price)
        nameid = price[-1]
        total_price = price[-2]
        list_shop = price[0:length-2]
        list_name = Gouwuche.objects.filter(go1=nameid)
        for i in list_name:
            for u in range(len(list_shop)):
                if str(i.gnum) == list_shop[u]:
                    Gouwuche.objects.filter(gnum=list_shop[u],go1=nameid).delete()
                    print('删除成功')
                else:
                    print('删除失败')
        price_user = Yonghu.objects.get(username=nameid).password
        print(price_user)
        balance = int(price_user) - int(total_price)
        Yonghu.objects.filter(username=nameid).update(password=str(balance))
        return HttpResponse('购买成功')

#我的信息展示
def myinfo(request):
    usern = request.GET.get('userN')
    var = Yonghu.objects.get(username=usern)
    lists = []

    dic = {}
    dic['id'] = var.id
    dic['username'] = var.username
    dic['balance'] = var.password
    dic['addr'] = var.shouhuo

    dic['tel'] = var.phone
    dic['sex'] = var.sex
    dic['pwd'] = var.passwordd
    lists.append(dic)
    return render(request,'my_jd.html',{'list':lists,'usern':usern})

#修改用户信息
@csrf_exempt
def change_info(request):
    usern = request.POST.get('id')
    s = request.POST.get('balance')
    print(s)
    var  = Yonghu.objects.get(id=usern)
    # var.id = request.POST.get('id')
    var.username = request.POST.get('username')
    print(request.POST.get('username'))
    var.password = request.POST.get('balance')

    var.shouhuo = request.POST.get('addr')

    var.phone = request.POST.get('tel')
    var.sex = request.POST.get('sex')
    var.passwordd = request.POST.get('pwd')
    var.save()
    return render(request,'a.html')

# *************************************************************************************************


#管理员用户注册
def zhuce(request):
    return render(request,'landing.html')
def zhuce1(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    passwordd  = request.POST.get('passwordd')
    db = Yonghu()
    db.username = username
    db.password = password
    db.passwordd = passwordd
    db.save()
    return render(request,'landing.html')



#用户登录
# def Ydenglu(request):
#管理员
#跳至登录页面
#全局变量验证码
yanzhengma1 = ''
@csrf_exempt
def gdenglu(request):
    s = shengcheng()
    global yanzhengma1
    yanzhengma1 = s
    return render(request,'gdenglu.html',{'img':'/static/img/yanzhengma.jpg'})


#刷新验证码
def SXyanzhengma(request):
    s = shengcheng()
    global yanzhengma1
    yanzhengma1 = s
    p = '/static/img/yanzhengma.jpg'
    return HttpResponse(json.dumps(p))
#判断密码是否正确
#
@csrf_exempt
def gdenglu1(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    yanzhengma = request.POST.get('yanzhengma')
    global yanzhengma1
    if str(yanzhengma) == str(yanzhengma1):
        if username=='aaa' and password=='666':
            # m = Guanliyuan.objects.filter(username=username)
            request.session['session'] = 'admin'
            return render(request,'logain.html')
        else:
            return HttpResponse('密码错误哦')
    else:
        # return HttpResponse('验证码输入错误')
        return render(request,'gdenglu.html',{'list':'验证码输入错误'})


#退出登录
def tuichu(request):
    del request.session['session']
    return HttpResponse('退出成功')


#分页查询
def gdenglu2(request):
    s = request.session.get('session')
    if s == 'admin':
        list_user = []
        list_user2 = []
        list_user3=[]
        page_count = 5
        cur_page = int(request.GET.get('page'))
        queryset = Shangping.objects.all().count()
        # 总页数
        if queryset % 5 == 0:
            num_page = queryset / 5
        else:
            num_page = (queryset // 5) + 1
        cur_page1 = cur_page
        # 当前页前一页
        d_qianyi = cur_page1 - 1
        # 当前页后一页
        d_houyi = cur_page1 + 1
        start = (cur_page1 - 1) * 5
        end = cur_page1 * 5
        list3 = Shangping.objects.all()
        for i in list3:
            # dict1 = {}
            num = i.num
            name = i.name
            speck = i.speck
            manage = i.manage
            img = i.img
            id = i.id
            dict1 = {'num': num, 'name':name, 'speck': speck, 'manage': manage,'img':img,'id':id}
            list_user.append(dict1)
        list_user1 = list_user[start:end]

        page_countt = 5
        cur_pagee = int(request.GET.get('pagee'))
        querysett = Yonghu.objects.all().count()
        # 总页数
        if querysett % 5 == 0:
            num_pagee = querysett / 5
        else:
            num_pagee = (querysett // 5) + 1
        cur_page11 = cur_pagee
        # 当前页前一页
        d_qianyii = cur_page11 - 1
        # 当前页后一页
        d_houyii = cur_page11 + 1
        startt = (cur_page11 - 1) * 5
        endd = cur_page11 * 5
        list3 = Yonghu.objects.all()
        for i in list3:
            # dict1 = {}
            username = i.username
            password = i.password
            shouhuo = i.shouhuo
            phone = i.phone
            name = i.name
            sex = i.sex
            id = i.id
            sd = ''
            passwordd= i.passwordd
            gouwu = Gouwuche.objects.filter(go1 = username)
            list9=[]
            for i in gouwu:
                shangping = Shangping.objects.get(id = i.gnum)
                sname = shangping.name
                sd = shangping.num
                sspeck = shangping.speck
                simg = shangping.img
                smanage = shangping.manage
                dict2 = {'sname':sname,'sspeck':sspeck,'simg':simg,'smanage':smanage,'sd':sd}
                list9.append(dict2)

            dict1 = {'username': username, 'sd':sd, 'id':id,'password':password,'shouhuo':shouhuo,'phone':phone, 'name': name, 'sex': sex, 'passwordd': passwordd,
                     'list9':list9}
            list_user2.append(dict1)

        list_userr = list_user2[startt:endd]
        return render(request, 'guanliyuanzhanshi.html',
                      {'list': list_user1,
                       'list1':list_userr,
                       #第一个分页信息
                       'page_count': page_count, 'cur_page1': cur_page1, 'queryset': queryset,
                       'num_page': num_page, 'd_qianyi': d_qianyi, 'd_houyi': d_houyi,
                        #第二个分页信息
                       'page_countt': page_countt, 'cur_page11': cur_page11, 'querysett': querysett,
                       'num_pagee': num_pagee, 'd_qianyii': d_qianyii, 'd_houyii': d_houyii,
                       })
    else:
        return HttpResponse('请登录')


#删除商品
def gsshanchu(request):
    id = request.GET['num']
    Shangping.objects.filter(id=id).delete()
    return render(request,'logain.html')


#修改商品
def gsxiugai1(request):
    id = request.GET['num']
    db = Shangping.objects.get(id=id)
    num = db.num
    name = db.name
    speck = db.speck
    manage = db.manage
    img = db.img
    id = db.id
    dict1 = {'num': num, 'name': name, 'speck': speck, 'manage': manage, 'img': img, 'id': id}
    return render(request,'gshangpingxiugai.html',{'list1':dict1})


def gsxiugai2(request):
    num = request.POST['num']
    name = request.POST['name']
    speck = request.POST['speck']
    manage = request.POST['manage']
    id = request.POST['id']
    db = Shangping.objects.get(id=id)
    db.num = num
    db.name = name
    db.speck = speck
    db.manage = manage
    db.save()
    return render(request,'logain.html')


#新增商品
def add_shangping1(request):
    return render(request,'gadd_s.html')


def add_shangping2(request):
    if request.method == "POST":
        num = request.POST['num']
        name = request.POST.get('name')
        speck = request.POST.get('speck')
        manage = request.POST.get('manage')
        f = request.FILES.get('imgg')  # 在FILES中接收文件
        # 文件在服务器端的路径
        filepath = os.path.join(settings.MEDIA_ROOT, f.name)
        # filepath = os.path.join(settings.MEDIA_ROOT, f.name)
        # filepath = os.path.join('\static\img\\',f.name)

        ff = '..\statics\img\\' + f.name

        Shangping.objects.create(num=num, name=name, speck=speck, img=ff,manage=manage)
        with open(filepath, 'wb') as fp:
            for info in f.chunks():
                fp.write(info)  # chunks是以文件流的方式来接受文件，分段写入
                return render(request, 'logain.html')

    else:
        return HttpResponse('上传失败！')


#修改用户
def gyxiugai1(request):
    id = request.GET['id']
    db = Yonghu.objects.get(id=id)
    username = db.username
    password = db.password
    shouhuo = db.shouhuo
    phone = db.phone
    name = db.name
    sex = db.sex
    passwordd = db.passwordd
    dict1 = {'username':username,'password':password,'shouhuo':shouhuo,'phone':phone,'name':name,'sex':sex,'passwordd':passwordd,'id': id}
    return render(request,'gyyonghuxiugai.html',{'list1':dict1})


def gyxiugai2(request):
    id = request.POST['id']
    username = request.POST['username']
    password = request.POST['password']
    shouhuo = request.POST['shouhuo']
    phone = request.POST['phone']
    name = request.POST['name']
    sex = request.POST['sex']
    passwordd = request.POST['passwordd']
    db = Yonghu.objects.get(id=id)
    db.username = username
    db.password = password
    db.shouhuo =  shouhuo
    db.phone = phone
    db.name = name
    db.sex = sex
    db.passwordd=passwordd
    db.save()
    return render(request,'logain.html')


#拉黑用户
def gsyonghu(request):
    id = request.GET['id']
    Yonghu.objects.filter(id=id).delete()
    return render(request,'logain.html')


#管理员忘记密码
#跳至忘记密码验证页面
def gwjmm1(request):
    return render(request,'gwjmm.html')


def gwjmm2(request):

    username = request.POST.get('username')
    passwordd = request.POST.get('passwordd')
    if Guanliyuan.objects.filter(username = username,passwordd=passwordd):
        list1 = []
        dict1 = {'username':username}

        return render(request,'gwjmmxiugai.html',{'list1':dict1})
    else:
        return HttpResponse('输入错误')


#修改管理员数据库的密码并返回主页
def gwjmm3(request):
    username = requet.POST.get('username')
    password = requet.POST.get('password')
    db = Guanliyuan.objects.filter(username=username)[0]
    db.password = password
    db.save()
    return render(requet,'index.html')

