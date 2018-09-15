# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import sha1
from .models import *
from . import user_decorator
from df_goods.models import *
from df_cart.models import *


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd1 = post.get('cpwd')
    uemail = post.get('email')

    if upwd != upwd1 or upwd == '':
        return redirect('/user/register/')

    s = sha1()
    upwd = upwd.encode('utf-8')
    s.update(upwd)

    upwd2 = s.hexdigest()

    count = UserInfo.objects.filter(uname=uname).count()
    if count == 1:
        return redirect('/user/register/')

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = uemail

    user.save()

    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        s1 = sha1()
        upwd = upwd.encode('utf-8')
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)

            carts = CartInfo.objects.filter(user_id=users[0].id)
            carts_num = len(carts)
            request.session['carts_num'] = carts_num
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            upwd = upwd.decode('utf-8')
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)

    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_decorator.login
def info(request):
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    print(goods_ids1)
    for goods_id in goods_ids1:
        goods = GoodsInfo.objects.get(pk=int(goods_id))
        goods_list.append(goods)

    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {
        'goods_list': goods_list,
        'page_name': 1,
        'title': '用户中心',
        'user': user
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    context = {
        'page_name': 1,
        'title': '订单中心'
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': '收货中心',
        'user': user
    }
    return render(request, 'df_user/user_center_site.html', context)
