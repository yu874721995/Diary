#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/5/28 11:47
@Author  : Careslten
@Site    : 
@File    : user_CreateTestCase.py
@Software: PyCharm
'''

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import pymysql as mysql
import json, time
from xcx import models
import requests
from Public.JsonData import DateEncoder
from django.contrib.auth.decorators import login_required


class user_testCase():

    def checkquery(self, *args):
        for i in args:
            if i == None or i is False or i == '':
                return True

    def SaveCommodity(self, request):
        print('-------------request_body:', request.POST)
        Commodity_name = request.POST.get('Commodity_name', None)  # 商品名称
        cpChoice = request.POST.get('cpChoice', None)  # 所属模块
        Comodity_introduction = request.POST.get('Comodity_introduction', None)  # 商品简介
        Comodity_Specifications = request.POST.get('Comodity_Specifications', None)  # 商品规格
        Commodity_Company = request.POST.get('Commodity_Company', None)  # 商品计量单位
        Commodity_money = request.POST.get('Commodity_money', None)  # 商品价格
        Commodity_img = request.POST.get('Commodity_img', None)  # 商品图片
        Commodity_details = request.POST.get('Commodity_details', None)  # 商品详情
        user_id = request.session.get('user_id', None)
        print('Commodity_name:', Commodity_name, 'user_id:', user_id, 'cpChoice:', cpChoice, 'Comodity_introduction:',
              Comodity_introduction, 'Comodity_Specifications:', Comodity_Specifications, 'Commodity_Company:',
              Commodity_Company, 'Commodity_money:', Commodity_money, 'Commodity_img:', Commodity_img,
              'Commodity_details:', Commodity_details)
        # 参数校验
        if self.checkquery([Commodity_name, cpChoice, Comodity_introduction, Comodity_Specifications, Commodity_Company,
                            Commodity_money]):
            return HttpResponse(json.dumps({'status': 5, 'msg': '参数错误'}))
        if user_id == None:
            return HttpResponse(json.dumps({'status': 100, 'msg': '登录过期'}))

        cpChoice_mk = cpChoice.split('/')[1]  # 隶属模块
        com_id = ''

        try:
            dic = {
                'status': '1',
                'Commodity_name': Commodity_name,
                'Comodity_type': cpChoice_mk,
                'Comodity_introduction': Comodity_introduction,
                'Comodity_Specifications': Comodity_Specifications,
                'Commodity_Company': Commodity_Company,
                'Commodity_money': Commodity_money,
                'Commodity_details': Commodity_details,
                'user_id': user_id
            }
            models.Commodity.objects.create(**dic)
            com = models.Commodity.objects.filter(Commodity_name=Commodity_name).order_by('-create_time')
            print(com)
            com_id = com.values()[0]['id']
        except Exception as e:
            print(e)

        try:
            print('com_id:', com_id)
            img = Commodity_img.split(';')[:-1]  # 前端传来的字符串最后是个空字符
            print(img)
            for i in img:
                data = {
                    'status': '1',
                    'Commodity_id': com_id,
                    'pic_path': i,
                }
                models.Commodity_pic.objects.create(**data)
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 10001, 'msg': '存入商品图片失败', 'error': e}))
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))

    def delCom(self, request):
        com_id = request.POST.get('com_id', None)
        status = request.POST.get('status', None)
        print(com_id, status)
        if com_id is None or status is None:
            return HttpResponse(json.dumps({'status': 500, 'msg': '参数错误'}))
        try:
            models.Commodity.objects.filter(id=com_id).update(status=status)
            return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 10086, 'msg': e}))

    def editbanner(self, request):
        id = request.POST.get('id', None)
        status = request.POST.get('status', None)
        print(id, status)
        if id is None or status is None:
            return HttpResponse(json.dumps({'status': 500, 'msg': '参数错误'}))
        try:
            models.Commodity_banner.objects.filter(id=id).update(status=status)
            return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 10086, 'msg': e}))

    def Savebanner(self, request):
        print('request_body------------------:', request.POST)
        banner_name = request.POST.get('banner_name', None)
        banner_path = request.POST.get('banner_path', None)
        banner_img = request.POST.get('banner_img', None)
        banner_detail = request.POST.get('banner_details', None)
        if self.checkquery([banner_detail, banner_img, banner_name, banner_path]):
            return HttpResponse(json.dumps({'status': 5, 'msg': '参数错误'}))
        user_id = request.session.get('user_id', None)
        query = models.Commodity_banner.objects.filter(banner_name=banner_name).values()
        queryNum = models.Commodity_banner.objects.filter(banner_path=banner_path, status=1).values()
        if banner_path == 1 or banner_path == '1':
            if queryNum.__len__() >= 5:
                return HttpResponse(json.dumps({'status': 5, 'msg': '首页仅允许添加5个活动'}))
        elif banner_path == 2 or banner_path == '2':
            if queryNum.__len__() >= 3:
                return HttpResponse(json.dumps({'status': 5, 'msg': '首页仅允许添加3个主题'}))
        else:
            if queryNum.__len__() >= 1:
                return HttpResponse(json.dumps({'status': 5, 'msg': '分类仅允许添加1个主题'}))



        if query.__len__() > 0:
            return HttpResponse(json.dumps({'status': 5, 'msg': '活动名称重复'}))
        try:
            dic = {'status': '1', 'banner_path': banner_path, 'banner_pic_path': banner_img, 'banner_name': banner_name,'banner_detail':banner_detail,
                   'user_id': user_id}
            models.Commodity_banner.objects.create(**dic)
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 5, 'msg': e}))
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))
