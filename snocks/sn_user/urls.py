#coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [

    url(r'^register.html/?$', views.register),# 注册
    url(r'^register_post/?$', views.register_post),# 获取内容
    url(r'^register_exist/?$', views.register_exist),

    url(r'^login.html/?$', views.login),# 登陆页面
    url(r'^login_handle/?$', views.login_handle),
    url(r'^logout/$',views.logout),# 退出

    url(r'^info/?$', views.info),# 用户中心
    url(r'^order(\d*)/?$', views.order),# 用户订单
    url(r'^site/?$', views.site),# 收货地址

    url(r'^order/pay(\d+)/?$', views.pay),# 收货地址
]