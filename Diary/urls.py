"""Diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import re_path
from xcx import views as indexviews
from xcx.api.user_CreateTestCase import user_testCase as SaveCase
from xcx.api.updateUser import update_Users as user
from xcx.api.userList import user_list as users
from xcx.api.req_Debug import req_debug as req
from xcx.api.login import Login as login
from xcx.api.CaseChoice import caseChoice as case
from xcx.api import wechat as wechatview
from xcx.api.loginAndRegite import login_and_reg as xcx_login
from xcx.api import uploadimg

urlpatterns = [
    #re_path('',oneviews.login),
    re_path(r'^$',indexviews.login),
    re_path('session_test',users().session_test),
    re_path('index',indexviews.index),
    re_path('login',indexviews.login),
    re_path('Loginup',login().Loginup),
    re_path('goRegister',indexviews.goRegister),
    re_path('register',indexviews.register),
    re_path('reqJson',req().reqJson),
    re_path('username',users().getuser),
    re_path('UserHistory', users().userHistory),
    re_path(r'^accounts/login/$',indexviews.login),
    re_path('SaveCommodity',SaveCase().SaveCommodity),
    re_path('delCom',SaveCase().delCom),
    re_path('userList',users().userList),
    re_path('updateUserStatus',user().updateUserStatus),
    re_path('addUser',users().add_User),
    re_path('user_delete',user().user_delete),
    re_path('userDelList',users().userDelList),
    re_path('recoverCustomer',users().recoverCustomer),
    re_path('addChoice',case().addChoice),
    re_path('queryForProduct',case().queryForProduct),
    re_path('queryForOur',case().queryForOur),
    re_path('caseList',case().comList),
    re_path('batchExecution',case().batchExecution),
    re_path('sendMsg',wechatview.sendMsg),
    re_path('getUserInfo',xcx_login().getUserInfo),
    re_path('uploadImage',uploadimg.uploadImage)


]
