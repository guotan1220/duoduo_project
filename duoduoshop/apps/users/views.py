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
from .models import User, Address
import re
import json
from django.http import JsonResponse, HttpResponse
from django import http
import logging

logger = logging.getLogger('django')


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
        from django.contrib.auth import login
        login(request, user)
        return JsonResponse({'code': 0,
                             'errmsg': 'ok from daguo'})


"""
注册之后的行为：
    需求一：注册成功即代表用户认证通过，那么此时可以在注册成功之后实现状态保持（注册成功即已经登录）
    需求二：注册成功跳转到登陆界面，然后由用户操作进行登陆
状态保持方法1：
    cookie
    session 
状态保持方法2：
    from django.contrib.auth import login
    login(request, user)
"""
"""
用户登陆的实现
前端：通过post将用户名与密码通过axios发送到后端
后端：
    请求：接收数据、验证数据
    业务逻辑：验证用户名，密码是否与数据库一致，然后实现状态保持（session）
    响应：返回json数据，成功0，失败400
步骤：
    1.接收数据
    2.验证数据
    3.验证用户名密码是否正确
    4.session
    5.判断是否记住登录
    6.返回响应
"""


class LoginView(View):
    def post(self, request):
        ####################
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        #####################
        if not all([username, password]):
            return JsonResponse({'code': 400,
                                 'errmsg': '参数不全'})
        #########################
        # 有些时候，用户可以自行选择通过用户名或者手机号进行登录
        # 这时候，系统默认的USERNAME_FILED为username字段
        # 可以通过获取的登录信息，去修改这个字段，使得authenticate可以通过USERNAME_FILED对用户与密码进行比对,然后返回user或者none
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        # 系统提供了一个验证用户名密码的方法
        # 使用authenticate方法，如果验证通过则拿到用户信息，不正确则返回none
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'code': 400,
                                 'errmsg': '账号或密码输入错误'})
        #######################
        from django.contrib.auth import login
        login(request, user)
        #######################
        # #记住登录=天内免登录
        if remembered is not None:
            # session有效时间具体问题具体分析
            request.session.set_expiry(None)
        else:
            # 设置0 则退出浏览器则过期
            request.session.set_expiry(0)
        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok from daguo'})
        # 这里的cookie主要是为了主页显示用户名
        response.set_cookie('username', user.username)
        return response


"""
用户登出功能的实现
前端：点击退出按钮之后，发送axios请求（delete）
后端：
    请求：
    业务逻辑：退出
    响应：返回json数据
"""


class LogoutView(View):
    def delete(self, request):
        from django.contrib.auth import logout
        logout(request)
        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok from daguo'})
        response.delete_cookie('username')
        return response


"""
用户中心的显示
"""
from utils.views import LoginRequiredJSONMixin


class CenterView(LoginRequiredJSONMixin, View):
    def get(self, request):
        # request.user就是已经登陆的用户信息
        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active
        }
        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'info_data': info_data})


"""
整体需求：保存邮箱地址，然后发送邮件验证码，最后用户激活邮件
前端：当用户完成输入点击保存按钮之后，会发送axios请求
后端： 
    请求：接受请求，获取数据
    业务逻辑：接收前端的数据据，然后进行验证，并入库
    响应：返回json数据
步骤：
    1.接收数据、获取数据
    2.验证数据
    3.数据入库
    4.返回json数据
"""
from celery_demo.email.tasks import send_mail_link


class EmailView(View):
    def put(self, request):
        # 1.
        # 接收数据、获取数据
        data = json.loads(request.body.decode())
        email = data['email']
        user = request.user
        # 2.
        # 验证数据
        # 通过正则验证邮箱是否正确
        if not re.match('[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
            return JsonResponse({'code': 400,
                                 'errmsg': 'email address maybe wrong'})
        # 3.
        # 数据入库
        user.email = email
        user.save()
        # 发送验证码
        # 赋值email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            import logging
            logger = logging.getLogger('django')
            logger.error(e)
            return JsonResponse({'code': 0, 'errmsg': '添加邮箱失败'})
        # def send_mail_link(to_email, verify_url):
        #     """
        #     发送验证邮箱邮件
        #     :param to_email: 收件人邮箱
        #     :param verify_url: 验证链接
        #     :return: None
        #     """
        # 生成用户单独的验证链接
        from .utils import generate_verify_email_url
        verify_url = generate_verify_email_url(user)
        send_mail_link.delay(email, verify_url)
        # 4.
        # 返回json数据
        return JsonResponse({'code': 0,
                             'errmsg': 'ok from daguo'})


# 编写一个用于验证用户点击邮件中验证链接的接口
from .utils import check_verify_email_token


class VerifyEmailView(View):
    def put(self, request):
        # - 1.接收 token
        token = request.GET.get('token')

        if not token:
            return JsonResponse({'code': 400, 'errmsg': 'token缺少'})

        # - 2.解密
        data_dict = check_verify_email_token(token)

        # - 4.去数据库对比 user_id,email
        try:
            user = User.objects.get(pk=data_dict.get('user_id'), email=data_dict.get('email'))
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '参数有误!'})

        # - 5.修改激活状态
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            return JsonResponse({'code': 0, 'errmsg': '激活失败!'})


"""
用户数据库的增删改查
请求：
业务逻辑：
响应：

增：注册
    1.接收数据
    2.验证数据
    3.数据入库
    4.返回响应
删：
    1.查询指定记录
    2.删除数据（物理删除、逻辑删除）
    3.返回响应
改：个人邮箱
    1.查询指定记录
    2.接收数据
    3.验证数据
    4.数据入库
    5.返回响应
            
查：area，个人中心数据的展示
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应
"""
"""
实现用户地址信息的新增
前端：
    将收货人、地区、地址、手机、固定电话、邮箱通过axios发送到后端
后端：
    （新增）
    接收数据
    验证数据
    数据入库
    返回响应
"""
"""
需求：
    新增地址

前端：
        当用户填写完成地址信息后，前端应该发送一个axios请求，会携带 相关信息 （POST--body）

后端：

    请求：         接收请求，获取参数,验证参数
    业务逻辑：      数据入库
    响应：         返回响应

    路由：     POST        /addresses/create/
    步骤： 
        1.接收请求
        2.获取参数，验证参数
        3.数据入库
        4.返回响应

"""
from apps.users.models import Address


class AddressCreateView(LoginRequiredJSONMixin, View):

    def post(self, request):
        # 1.接收请求
        data = json.loads(request.body.decode())
        # 2.获取参数，验证参数
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user
        # 验证参数 （省略）
        # 2.1 验证必传参数
        # 2.2 省市区的id 是否正确
        # 2.3 详细地址的长度
        # 2.4 手机号
        # 2.5 固定电话
        # 2.6 邮箱

        # 3.数据入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        address_dict = {
            'id': address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 4.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


class AddressView(LoginRequiredJSONMixin, View):

    def get(self, request):
        # 1.查询指定数据
        user = request.user
        # addresses=user.addresses

        addresses = Address.objects.filter(user=user, is_deleted=False)
        # 2.将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})


"""
需求：前端向后端传要求改的地址id以及要改的地址信息
前端；接口：addresses/(?<address_id>\d+)/
        json信息，包括要修改的所有地址信息
后端：
    请求：         接收请求，获取参数,验证参数
    业务逻辑：      数据入库
    响应：         返回响应

    路由：     POST       addresses/(?<address_id>\d+)/
    步骤： 
        1.接收请求
        2.获取参数，验证参数
        3.数据入库
        4.返回响应
"""


class AddressModifyView(LoginRequiredJSONMixin, View):
    """修改和删除地址"""

    def put(self, request, address_id):
        """修改地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.JsonResponse({'code': 400,
                                      'errmsg': '缺少必传参数'})

        if not re.match('1[3-9]\d{9}', mobile):
            return http.JsonResponse({'code': 400,
                                      'errmsg': '参数mobile有误'})

        if tel:
            if not re.match('0\d{2,3}\d{7,8}|^1[3456789]\d{9}', tel):
                return http.JsonResponse({'code': 400,
                                          'errmsg': '参数tel有误'})
        if email:
            if not re.match('[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
                return http.JsonResponse({'code': 400,
                                          'errmsg': '参数email有误'})

        # 判断地址是否存在,并更新地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '更新地址失败'})

        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应更新地址结果
        return JsonResponse({'code': 0, 'errmsg': '更新地址成功', 'address': address_dict})

    """
    删除地址：
    需求：前端像后端发送要删除的地址id，后端将该数据 逻辑删除
    前端：像后端传待删id
    后端：
        逻辑删除
    """
    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 查询要删除的地址
            address = Address.objects.get(id=address_id)

            # 将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '删除地址失败'})

        # 响应删除地址结果
        return http.JsonResponse({'code': 0, 'errmsg': '删除地址成功'})


"""
设置默认收获地址
前端：发送put请求包含地址id到指定接口
后端：接收address_id，将指定用户的default_address设置为该address_id对应的Address,返回响应
"""
class DefaultAddressView(LoginRequiredJSONMixin, View):
    def put(self, request, address_id):
        request.user.default_address = Address.objects.get(id=address_id)
        request.user.save()
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })

"""
修改地址标题： 效果：也就是只修改一部分数据，比如用户的地址标题
前端：调用put方法到指定接口将待修改的address_id传到后端
后端：接收address_id
        查询指定address
        修改address的title
"""
class AddressTitleModifyView(LoginRequiredJSONMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        try:
            # 查询地址
            address = Address.objects.get(id=address_id)

            # 设置新的地址标题
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '设置地址标题失败'})

        # 4.响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置地址标题成功'})

"""
修改密码逻辑：
    前端：将当前密码，以及两次新密码通过put方法传至后端
    接口: password/
    后端：接收数据，验证数据，数据入库，修改完毕后需要用户重新登录
"""
class PasswordmodifyView(LoginRequiredJSONMixin, View):
    def put(self, request):
        # 获取数据
        json_dict = json.loads(request.body.decode())
        old_password = json_dict.get('old_password')
        new_password = json_dict.get('new_password')
        new_password2 = json_dict.get('new_password2')
        # 检查数据
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({'code': 400,
                                 'errmsg': 'please input all parameters!'})
        if old_password == new_password:
            return JsonResponse({
                'code': 400,
                'errmsg': '密码重复'
            })
        if not re.match('[a-zA-Z0-9_-]{6,20}', new_password):
            return JsonResponse({'code': 400,
                                 'errmsg': 'check the first password !'})
        if new_password != new_password2:
            return JsonResponse({'code': 400,
                                 'errmsg': 'password id not Consistency !'})
        user = request.user
        user.set_password(new_password)
        user.save()

        from django.contrib.auth import logout
        logout(request)
        response = JsonResponse({
            'code': 0,
            'errmsg': '密码修改成功,现在请重新登陆'
        })
        response.delete_cookie('username') # 清理状态保持信息
        return response
