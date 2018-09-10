# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import sha1
from .models import *


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
            red = HttpResponseRedirect('/user/info/')
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)

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


def info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {
        'title': '用户中心',
        'user': user
    }
    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    context = {
        'title': '订单中心'
    }
    return render(request, 'df_user/user_center_order.html', context)


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
        'title': '收货中心',
        'user': user
    }
    return render(request, 'df_user/user_center_site.html', context)
