#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View
from libs.captcha.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse, JsonResponse
from libs.yuntongxun.sms import CCP
from random import randint
# Create your views here.
# 图形验证码的逻辑
# 前端：
#     拼接一个url，然后给img，img发起请求
# 后端：
#     请求      接收路由中的uuid
#     业务逻辑    生成图片验证码和图片二进制，通过redis将图片验证码保存起来
#     响应      返回图片二进制
# 步骤：
#     1.接收路由中的uuid
#     2.生成图片验证码和图片二进制
#     3.通过redis把图片验证码保存起来
#     4.返回图片二进制
class ImageCodeView(View):
    def get(self, request, uuid):
        # 1.接收路由中的uuid
        # 2.生成图片验证码和二进制图片
        text, image = captcha.generate_captcha()
        print(text)
        # 3.将图片验证码和二进制保存至redis
        # 3.1.连接redis数据库库
        redis_cli = get_redis_connection('code')
        # 3.2 将生成的验证码与uuid以及有效时间保存在redis数据库中
        redis_cli.setex(uuid, 100, text)
        # 4.将图片二进制返回
        # 注意要设置响应体数据类型conent_type='大类/小类'
        # 例如图片image/jpeg,image/gif, image/png
        return HttpResponse(image, content_type='image/png')


# 短信验证的逻辑
# 前端：
#     设置点击事件，拼接一个url包括用户的手机号，然后给后端发起短信验证码请求/用户最后点击注册时检测验证码是否正确
# 后端：
#     请求      接收路由中的手机号
# 业务逻辑        向第三方发送手机号验证码请求，然后将验证码与手机号保存在redis中
# 响应          返回json数据，验证码发送成功/失败|用户点击注册之后检测是否匹配
# 路由：采用GET
class CmsCodeView(View):
    def get(self, request, mobile):
        # 步骤：1.获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2.验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400,
                                 'errmsg': '参数不全'})
        # 3.验证图片验证码
        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code == None:
            return JsonResponse({'code': 400,
                                 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400,
                                 'errmsg': '验证码输入错误'})
        # 4.生成短信验证码
        vcode = '%06d' % randint(0, 999999)
        # 5.保存短信验证码
        redis_cli.setex(mobile, 100, vcode)
        # 6.发送短信验证码
        ccp = CCP()
        ccp.send_template_sms(mobile, [vcode, 5], 1)
        # 7.返回响应
        return JsonResponse({'code': 0,
                             'errmsg': 'ok'})

"""
中间人
生产者
消费者
使用Celery实现前三者
"""