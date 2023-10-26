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
