#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from hashlib import sha1
from . import user_login
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator
# from df_goods import GoodsInfo

# Create your views here.


# 跳转到注册页面
def register(request):
    context = {"title": "注册"}
    return render(request,'html/register.html',context)

# 获取表单提交的内容
def register_post(request):
    # print '2222'
    dict = request.POST
    fname = dict.get('user_name')
    fpwd1 = dict.get('pwd')
    fpwd2 = dict.get('cpwd')
    a = sha1()
    a.update(fpwd2)
    fpwd3 = a.hexdigest()
    femail = dict.get('email')
    data = FreshInfo.objects.create(fname=fname,fpwd=fpwd3,femail=femail)
    data.save()
    # 注册成功 回登陆页面
    return render(request,'html/login.html')

# 获取名字是否重复
def register_exist(request):
    # 获取名字
    uname = request.GET.get('name')
    # uname = request.POST.get('user_name')
    count = FreshInfo.objects.filter(fname=uname).count()
    # print count
    return JsonResponse({'count': count})

# 跳转到登陆页面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request,'html/login.html',context)

#
def login_handle(request):
    # 获取提交表单的内容
    post=request.POST
    uname=post.get('username')
    # print uname
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    # 根据用户名查询对象 获得列表 列表里面是字典
    users = FreshInfo.objects.filter(fname=uname)#[]列表对象
    # users = FreshInfo.objects.get(fname=uname)
    # print type(users)
    # print users[0].fpwd
    # 判断是否查到用户名,如果查到则判断密码是否正确,正确则转到用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].fpwd:
            url = request.COOKIES.get('red_url', '/')
            red = HttpResponseRedirect(url)
            # 成功后删除转向地址,防止以后直接登录造成的转向
            red.set_cookie('url', '', max_age=-1)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'html/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'html/login.html', context)

def logout(request):
    request.session.flush()# flush()清除
    return redirect('/')

@user_login.login
def info(request):# 用户中心
    # 判断是否登陆,未登录则跳转到登录页面!
    # 用装饰器

    uid = request.session['user_id']
    user_email = FreshInfo.objects.get(id = uid).femail
    # 最近浏览
    goods_list = []
    goods_ids = request.COOKIES.get('liulan', '')
    # 第一种方式:字符串
    # if goods_ids != '':
    #     goods_ids1 = goods_ids.split(',')  # ['']
    #     # GoodsInfo.objects.filter(id__in=goods_ids1)
    #     for goods_id in goods_ids1:
    #         goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    # 第二种方式:字符串列表
    if goods_ids != '':
        goods_ids1 = eval(goods_ids)
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_name': request.session['user_name'],
               'user_email': user_email,
               'page_name': 1,
               'goods_list': goods_list,
                "info_active":'active',
               }

    return render(request, 'html/user_center_info.html',context)

@user_login.login
def order(request,pIndex):# 订单
    uid = request.session['user_id']#用户id
    list = OrderInfo.objects.filter(user_id = int(uid))
    p = Paginator(list, 2)
    if pIndex == '':
        pIndex = '1'
    pages = p.page(pIndex)
    print pages
    context = {"title": "用户中心",
                'page_name': 1,
               "order_active":'active',
                'pages':pages,
               }
    return render(request, 'html/user_center_order.html', context)

@user_login.login
def pay(request,oid):#支付
    order = OrderInfo.objects.get(pk=oid)
    order.isPay = True
    order.save()
    return redirect('/user/order/')

@user_login.login
def site(request):
    uid = request.session['user_id']
    user = FreshInfo.objects.get(id = uid)
    if request.method == 'POST':
        post = request.POST
        user.frecipients = post.get('ushou')# 收件人
        user.faddress = post.get('uaddress')
        user.fyoubian = post.get('uyoubian')
        user.fphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心',
               'user': user,
               'page_name': 1,
               "site_active":'active',
               }
    return render(request, 'html/user_center_site.html', context)