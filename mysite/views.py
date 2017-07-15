# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.http import HttpResponseRedirect,HttpResponse
from mysite import models,forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request,pid=None,del_pass=None):
    if request.user.is_authenticated():
        username=request.user.username
        useremail=request.user.email
        try:
            user=models.User.objects.get(username=username)
            diaries=models.Diary.objects.filter(user=user).order_by('-ddate')
        except:
            pass
    messages.get_messages(request)
    return render(request,'index.html',locals())


def listing(request):
    template=get_template('listing.html')
    posts=models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods=models.Mood.objects.all()

    html=template.render(locals())

    return HttpResponse(html)


@login_required(login_url='/login/')
def posting(request):
    if request.user.is_authenticated():
        username=request.user.username
        useremail=request.user.email
    messages.get_messages(request)

    if request.method=='POST':
        user=User.objects.get(username=username)
        diary=models.Diary(user=user)
        post_form=forms.DiaryForm(request.POST,instance=diary)
        if post_form.is_valid():
            messages.add_message(request,messages.INFO,'日记已存储')
            post_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, '如果要张贴日记，那么每一个字段都需要填')
    else:
        post_form=forms.DiaryForm()
        messages.add_message(request, messages.INFO, '如果要张贴日记，那么每一个字段都需要填')

    return render(request,'posting.html',locals())


def contact(request):
    if request.method=='POST':
        form=forms.ContactForm(request.POST)
        if form.is_valid():
            message="感谢您的来信"
            user_name=form.cleaned_data['user_name']
            user_city=form.cleaned_data['user_city']
            user_school=form.cleaned_data['user_school']
            user_email=form.cleaned_data['user_email']
            user_message=form.cleaned_data['user_message']
        else:
            message="请检查您输入的信息是否正确"
    else:
        form=forms.ContactForm()

    return render(request,'contact.html',locals())


def post2db(request):
    if request.method =='POST':
        post_form=forms.PostForm(request.POST)
        if post_form.is_valid():
            message='您的信息已存储，要等管理员启用后才看得到'
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message = '如果要张贴信息，那么每一个字段都要填...'
    else:
        post_form=forms.PostForm()
        message = '如果要张贴信息，那么每一个字段都要填...'

    return render(request,'post2db.html',locals())


def login(request):
    if request.method =='POST':
        login_form=forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=login_form.cleaned_data['password']
            user=authenticate(username=login_name,password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    print "success"
                    messages.add_message(request,messages.SUCCESS,'成功登录了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '账号尚未启用')
            else:
                messages.add_message(request, messages.WARNING, '登录失败')
        else:
            messages.add_message(request, messages.INFO, '请检查输入的字段内容')
    else:
        login_form=forms.LoginForm()

    return render(request,'login.html',locals())


def logout(request):
    auth.logout(request)
    messages.add_message(request,messages.INFO,'成功注销了')
    return redirect('/')


@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated():
        username=request.user.username
        try:

            user=User.objects.get(username=username)
            userinfo=models.Profile.objects.get(user=user)
        except:
            pass
    else:
        return redirect('/login/')
    template=get_template('userinfo.html')
    html=template.render(locals())
    return HttpResponse(html)