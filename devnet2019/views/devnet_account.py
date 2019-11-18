#!/usr/bin/env python3
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from devnet2019.forms import UserForm, loginForm


# 登入
@csrf_exempt
def network_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        next_to = request.GET.get('next', '/')
        remember = request.POST.get('remember', 0)
        if form.is_valid():
            # 取出登录表单信息，使用 cleaned_data 可以取出表单的原有格式
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if next_to == '':
                next_to = '/'
            if user:
                if user.is_active:
                    login(request, user)
                    # 在session在增加一些会话变量
                    request.session['username'] = username
                    request.session['uid'] = user.id
                    request.session['nick'] = None
                    request.session['tid'] = None

                    response = HttpResponseRedirect(next_to)

                    if remember != 0:
                        response.set_cookie('username', username)
                    else:
                        response.set_cookie('username', '', max_age=-1)
                    return response
                else:
                    message = True
                    return render(request, 'account/login.html', locals())
            else:
                message = False
                return render(request, 'account/login.html', locals())
    else:
        next_to = request.GET.get('next', '/')
    return render(request, 'account/login.html', locals())


# 登出
@csrf_exempt
def network_logout(request):
    # 清理cookie里保存username
    next_to = request.GET.get('next', '/')
    if next_to == '':
        next_to = '/'
    # response = HttpResponseRedirect(next_to)
    # response.delete_cookie('username')
    logout(request)
    return redirect(next_to)


# 注册
@csrf_exempt
def network_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        next_to = request.POST.get('next', 0)
        if form.is_valid():
            # 获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            # 判断密码是不是纯数字
            if password.isdigit():
                pwd_error = 'nums'
                return render(request, 'account/signup.html', locals())
            # 判断2字输入密码是否相同
            if password != password2:
                pwd_error = 'unequal'
                return render(request, 'account/signup.html', locals())

            # 判断用户和email是否存在
            is_user = User.objects.filter(username=username)
            is_email = User.objects.filter(email=email)

            pwd_length = len(password)
            if pwd_length < 8 or pwd_length > 20:
                pwd_error = 'length'
                return render(request, 'account/signup.html', locals())

            user_length = len(username)

            # 对表单信息判断
            if user_length < 5 or user_length > 20:
                user_error = 'length'
                return render(request, 'account/signup.html', locals())
            if is_user:
                user_error = 'exit'
                return render(request, 'account/signup.html', locals())
            if is_email:
                email_error = 'exit'
                return render(request, 'account/signup.html', locals())
            # 添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            user = authenticate(username=username, password=password)

            # 添加到session
            request.session['username'] = username
            request.session['uid'] = user.id
            request.session['email'] = email
            request.session['nick'] = ''

            # 调用auth登录
            login(request, user)
            # 重定向到首页
            if next_to == '':
                next_to = '/'
            return redirect(next_to)
    else:
        next_to = request.GET.get('next', '/')
        isLogin = False
        next_to = next_to
    # 将request 、页面 、以及context（要传入html文件中的内容包含在字典里）返回
    return render(request, 'account/signup.html', locals())
