"""Jindong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import view

urlpatterns = [

    url(r'^page1/', view.page1),
    url(r'^page2/', view.page2),
    url(r'^index$',view.index),#首页
    url(r'^sign$',view.sign),#登陆
    url(r'^login$',view.login),#注册
    url(r'^regist$',view.user_regist),#注册处理
    url(r'^sign_ctr$',view.user_sign),#登陆处理
    url(r'^add_index$',view.add_goods_index),#添加货物的首页
    url(r'^add_show$',view.show_goods),#显示添加的货物
    url(r'^add_goods$',view.add_goods),#实现添加货物的功能
    url(r'^search$',view.search),#实现搜索功能
    url(r'^gouwu$',view.shopcar),#购物车处理
    url(r'^goumai$',view.check_out),#购买物处理
    url(r'^add_car$',view.add_shopcar),#添加到购物车
    url(r'^jiesuan$',view.jiesuan),#结算功能

    # 分割线 *****************************************
    # url(r'zhuce$',view.zhuce),
    url(r'^zhuce$',view.zhuce),
    url(r'^zhuce1$',view.zhuce1),
    #用户登录
    # url(r'Ydenglu$',view.Ydenglu),
    #管理员登录
    #跳登录页面
    url(r'^gdenglu$',view.gdenglu),
    url(r'shuaxinyanzhengma$',view.SXyanzhengma),
    #判断登录是否成功
    url(r'^gdenglu1$',view.gdenglu1),
    #退出登录
    url(r'^tuichu$',view.tuichu),
    #分页查询
    url(r'^gdenglu2$', view.gdenglu2),

    #管理员删除商品
    url(r'^gsshanchu$',view.gsshanchu),

    #管理员修改商品
    url(r'^gsxiugai1$',view.gsxiugai1),
    url(r'^gsxiugai2$',view.gsxiugai2),

    #管理员增加商品
    url(r'^add_shangping1$',view.add_shangping1),
    url(r'^add_shangping2$',view.add_shangping2),

    #管理员拉黑用户
    url(r'^gsyonghu$',view.gsyonghu),
    #管理员修改用户
    url(r'^gyxiugai1$', view.gyxiugai1),
    url(r'^gyxiugai2$', view.gyxiugai2),

    #管理员忘记密码
    #跳至忘记密码页面
    url(r'^gwjmm1$', view.gwjmm1),
    #判断验证密保是否正确
    url(r'^gwjmm2$',view.gwjmm2),
    #修改密码页面（修改成功返回登录页面）
    url(r'^gwjmm3$',view.gwjmm3),

    url(r'^my_info$',view.myinfo),#进入我的信息页
    url(r'^change$',view.change_info),#修改我的信息
]
