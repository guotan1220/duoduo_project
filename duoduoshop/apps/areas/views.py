from django.shortcuts import render

# Create your views here.
"""
需求：
    获取省份信息
前端：
    当前界面加载的时候， 发送axios请求，获取省份信息
后端：
    请求： 不需要请求参数
    业务逻辑：   接收请求之后将省份信息返回
    响应： json
    路由： areas/
    步骤：
        1.查询省份
        2.返回响应
        
"""
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Area
import logging
logger = logging.getLogger('django')
from django.core.cache import cache
class AreaView(View):
    """省市区数据"""
    def get(self, request):
        """提供省市区数据"""
        # 提供省份数据
        # 首先判断cache是否有要查询的数据
        province_list = cache.get('province_list')
        if province_list is None:
            try:
                # 查询省份数据
                province_model_list = Area.objects.filter(parent__isnull=True)

                # 序列化省级数据
                province_list = []
                for province_model in province_model_list:
                    province_list.append({'id': province_model.id, 'name': province_model.name})
                cache.set('province_list', province_list, 7 * 3600)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': 400, 'errmsg': '省份数据错误'})
            # 响应省份数据
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'province_list': province_list})
"""
需求：
    获取市以及县的信息
前端：
    当前界面输入了省级或者市级信息之后，前端会向后端发送一个axios请求
后端：
    请求：     将省级或者市级的id传递到后端
    业务逻辑：   后端根据传递到的id信息查询子级信息，并将查询到的结果转化为字典列表
    响应：     json
    路由：     areas/id/
    步骤：
        1.获取省市id，查询信息
        2.将对象转化为字典数据
        3.返回响应
"""
class SubAreaView(View):
    """省市区数据"""

    def get(self, request, pk):
        """提供省市区数据"""
        # 判断是否在缓存中
        sub_data = cache.get('sub_list%s' % pk)
        if sub_data is None:
            # 提供市或区数据
            try:
                parent_model = Area.objects.get(id=pk)  # 查询市或区的父级
                sub_model_list = parent_model.subs.all()

                # 序列化市或区数据
                sub_list = []
                for sub_model in sub_model_list:
                    sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                sub_data = {
                    'id': parent_model.id,  # 父级pk
                    'name': parent_model.name,  # 父级name
                    'subs': sub_list  # 父级的子集
                }
                cache.set('sub_list%s' % pk, sub_data, 7 * 3600)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': 400, 'errmsg': '城市或区数据错误'})

        # 响应市或区数据
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'sub_data': sub_data})