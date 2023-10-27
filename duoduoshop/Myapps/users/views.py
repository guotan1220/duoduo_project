
from django.shortcuts import render

# Create your views here.

# 判断用户名是否重名的功能
# 前端： 当用户输入用户名之后，失去焦点，发送一个axios（ajax）请求
# 后端（思路）：
#     请求： 接收用户名
#     业务逻辑：   根据用户查询数据库，如果查询的结果数量等于0，说明没有注册
#                     如果查询结果数量等于1，说明已经注册
#     响应：         JSON{code:0,count:0/1,errmsg:ok}
#     路由：         GET usernames/<username>/count/
#     步骤：
#         1.接收用户名
#         2.根据用户名查询数据库
#         3.返回响应
from django.views import View
from .models import User
from django.http import JsonResponse
import re


class UserNameCountView(View):
    def get(self, request, username):
        # 1.接收用户名
        # 如果用户名不满足输入要求，则直接返回错误
        # if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #     return JsonResponse({'code': 200,
        #                          'errmsg': 'username error!'})
        # 2.根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0,
                             'count': count,
                             'errmsg': 'ok from daguo'})


# 后端不相信前端提交的任何数据，有可能是接受的信息不是通过网页发过来的
# 前端： 当用户输入用户名、密码、确认密码、手机号以及同意协议之后
#         发送axios请求
# 后端：
#     请求：     接收请求（json数据），获取数据
#     业务逻辑：   验证数据，数据入库
#     响应：     返回字典数据JSON{'code':0, 'errmsg':'ok from daguo'} 0表示成功，400表示失败
#     路由：     post register/
#     步骤：
#         1.接收请求（post请求----JSON）
#         2.获取数据
#         3.验证数据
#             3.1 前端提交的所有数据
#             3.2 用户名满足规则and不能够重复
#             3.3 密码满足规则 and确认密码与密码要一致
#             3.4 手机号满足规则and手机号不能重复
#             3.5 需要同意协议
#         4.数据入库
#         5.返回响应
import json

class RegisterView(View):
    def post(self, request):
        # 1.接收请求（post请求----JSON）
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # 2.获取数据
        username = body_dict.get('username')
        password1 = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        # all([xxx,xxx,xxx])
        # all里面的元素只要是none或者False，all就会返回False，否则就会返回True
        #         3.验证数据
        #             3.1 前端提交的所有数据
        #             3.2 用户名满足规则and不能够重复
        #             3.3 密码满足规则 and确认密码与密码要一致
        #             3.4 手机号满足规则and手机号不能重复
        #             3.5 需要同意协议
        if not all([username, password1, password2, mobile, allow]):
            return JsonResponse({'code': 400,
                                 'errmsg': 'please input all parameters!'})
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400,
                                 'errmsg': 'check the username!'})
        if not re.match('[a-zA-Z0-9_-]{6,20}', password1):
            return JsonResponse({'code': 400,
                                 'errmsg': 'check the first password !'})
        if password1 != password2:
            return JsonResponse({'code': 400,
                                 'errmsg': 'password id not Consistency !'})
        if not re.match('1[345789]\d{9}', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': 'check the mobile !'})
        if not allow:
            return JsonResponse({'code': 400,
                                 'errmsg': 'please allow the agreement !'})
        # 4.数据入库
        # 方法一：
        # User(username = username, password = password1, mobile = mobile)
        # User.save()
        # 方法二：
        # User.objects.create(username=username, password=password1, mobile=mobile)
        # 方法三（能够对密码进行加密）
        user = User.objects.create_user(username=username, password=password1, mobile=mobile)
        user.save()
        return JsonResponse({'code': 0,
                             'errmsg': 'ok from daguo'})

"""
注册思路分析：
前端
"""