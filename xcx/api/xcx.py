#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2020/3/10 10:18
@Author  : Careslten
@Site    :
@File    : wechat.py
@Software: PyCharm
'''
from django.http import HttpResponse
from random import randint
from xcx import models
import json, time
import requests
from django.shortcuts import render
from wechat_sdk import WechatBasic
import urllib.request
import re
from django.db import connection
from xcx.models import Commodity_banner


class xcx():

    # 首页banner
    def xcxIndex(self, request):
        user_id = request.session.get('user_id', None)
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        # if user_id is None:
        #     return HttpResponse(json.dumps({'status': 300, 'msg': '请登录'}))
        # 首页banner
        query_banner = models.Commodity_banner.objects.filter(status='1', banner_path__in=['1', '2'])
        # print(query_banner.query)
        banner = []
        fy = self.pages(page, limit)
        for i in query_banner:
            data = {}
            data['id'] = i.id
            data['status'] = i.status
            data['banner_path'] = i.banner_path
            data['banner_pic_path'] = i.banner_pic_path
            data['banner_name'] = i.banner_name
            banner.append(data)
        query_commodity = models.Commodity.objects.filter(status='1').order_by('-commodity_num')

        num = 0
        commodity = []
        for i in query_commodity:
            data_com = {}
            num += 1
            if num < fy[0]:
                continue
            if num > fy[1]:
                break
            data_com['id'] = i.id
            data_com['Commodity_name'] = i.Commodity_name
            data_com['Comodity_introduction'] = i.Comodity_introduction
            data_com['Comodity_type'] = i.Comodity_type
            data_com['Commodity_Company'] = i.Commodity_Company
            data_com['Commodity_money'] = i.Commodity_money
            data_com['commodity_num'] = i.commodity_num
            data_com['Comodity_Specifications'] = i.Comodity_Specifications
            commodity.append(data_com)
        return HttpResponse(
            json.dumps({'status': 1, 'msg': '操作成功', 'data': {'banner': banner, 'commodity': commodity}}))

    def pages(self, page, limit):
        page = int(page)
        limit = int(limit)
        if page == 1:
            return (1, limit)
        begin = (page - 1) * limit + 1
        end = page * limit
        return (begin, end)

    # 分类商品列表
    def xcxComList(self, request):
        user_id = request.session.get('user_id', None)
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        type = request.POST.get('type', None)
        # if user_id is None:
        #    return HttpResponse(json.dumps({'status': 300, 'msg': '请登录'}))
        if type is None:
            return HttpResponse(json.dumps({'status': 400, 'msg': '参数错误'}))
        fy = self.pages(page, limit)
        query = models.Commodity.objects.filter(status=1, Comodity_type=type).order_by('-commodity_num')
        num = 0
        commodity = []
        for i in query:
            data_com = {}
            num += 1
            if num < fy[0]:
                continue
            if num > fy[1]:
                break
            data_com['id'] = i.id
            data_com['Commodity_name'] = i.Commodity_name
            data_com['Comodity_introduction'] = i.Comodity_introduction
            data_com['Comodity_type'] = i.Comodity_type
            data_com['Commodity_Company'] = i.Commodity_Company
            data_com['Commodity_money'] = i.Commodity_money
            data_com['commodity_num'] = i.commodity_num
            data_com['Comodity_Specifications'] = i.Comodity_Specifications
            commodity.append(data_com)
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功', 'data': commodity}))

    # 生成订单
    def createOrder(self, request):
        user_id = request.POST.get('user_id', 1)
        commodity_data = json.loads(request.body)['commodity_data']
        # if user_id is None:
        #     return HttpResponse(json.dumps({'status': 300, 'msg': '请登录'}))
        if commodity_data is None or isinstance(commodity_data,list) == False:
            return HttpResponse(json.dumps({'status': 400, 'msg': '参数错误'}))
        com_num = 0
        query = []
        for i in commodity_data:
            date = {}
            query_com = models.Commodity.objects.filter(id=i['com_id']).values()[0]  # 查询商品信息
            if query_com.__len__() == 0:
                return HttpResponse(json.dumps({'status': 600, 'msg': '{}该商品不存在'.format(i['com_id'])}))
            date['Commodity_id'] = query_com['id']
            date['Commodity_name']=query_com['Commodity_name']
            date['Comodity_num'] = i['Comodity_num']
            date['Commodity_money'] = query_com['Commodity_money']
            date['user_id'] = user_id
            com_num += int(i['Comodity_num']) * int(query_com['Commodity_money'])
            query.append(date)
        order_id = str(time.strftime('%Y%m%d%H%M%S', time.localtime())) + str(randint(1, 10000))
        dic = {
             'order_id': order_id,
            'Commodity_money': com_num,
            'user_id': user_id
        }
        try:
            orderID = models.Commodity_order.objects.create(**dic)
            for i in query:
                i['order_id'] = orderID.order_id
                try:
                    models.Commodity_order_pr.objects.create(**i)
                except Exception as e:
                    print(e)
                    return HttpResponse(json.dumps({'status': 500, 'msg': e}))
        except Exception as e:
            try:
                print(e)
                return HttpResponse(json.dumps({'status': 500, 'msg': e}))
            except Exception as e:
                return HttpResponse(json.dumps({'status': 500, 'msg': '数据库报错啦'}))
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功','order_id':orderID.order_id}))

    def addComCar(self,request):
        user_id = request.POST.get('user_id', 1)
        # if user_id is None:
        #     return HttpResponse(json.dumps({'status': 300, 'msg': '请登录'}))
        commodity_id = request.POST.get('com_id', None)
        Comodity_num = request.POST.get('Comodity_num', None)
        if commodity_id is None or Comodity_num is None:
            return HttpResponse(json.dumps({'status': 400, 'msg': '参数错误'}))
        query_com = models.Commodity.objects.filter(id=commodity_id).values()[0]  # 查询商品信息
        dic = {
            'user_id' :user_id,
            'Commodity_id':query_com['id'],
            'Comodity_num':Comodity_num,
            'Commodity_money':int(query_com['Commodity_money']) * int(Comodity_num)
        }
        models.comCar.objects.create(**dic)
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))

    def delComCar(self,request):
        user_id = request.POST.get('user_id', 1)
        # if user_id is None:
        #     return HttpResponse(json.dumps({'status': 300, 'msg': '请登录'}))
        car_id = request.POST.get('car_id', None)
        if car_id is None:
            return HttpResponse(json.dumps({'status': 400, 'msg': '参数错误'}))
        models.comCar.objects.filter(id=car_id,user_id=user_id).update(status=0) # 查询商品信息
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))

    def ComCar(self,request):
        user_id = request.POST.get('user_id', 1)
        # if user_id is None:
        #     return HttpResponse(json.dumps({'status': 300, 'msg': '请登录'}))
        query = models.comCar.objects.filter(status=1,user_id=user_id).values()

        data = []
        for i in query:
            body = {}
            body['id'] = i['id']
            try:
                query_com = models.Commodity.objects.filter(id=i['Commodity_id']).values()[0]
            except Exception as e:
                return HttpResponse(json.dumps({'status': 400, 'msg': '商品不存在'}))
            body['statuus'] = query_com['status']
            body['com_id'] = i['Commodity_id']
            body['com_name'] = query_com['Commodity_name']
            body['com_num'] = i['Commodity_num']
            body['com_money'] = i['Commodity_money']
            data.append(body)
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功','data':data}))



