from django.shortcuts import render

# Create your views here.

# �ж��û����Ƿ������Ĺ���
# ǰ�ˣ� ���û������û���֮��ʧȥ���㣬����һ��axios��ajax������
# ��ˣ�˼·����
#     ���� �����û���
#     ҵ���߼���   �����û���ѯ���ݿ⣬�����ѯ�Ľ����������0��˵��û��ע��
#                     �����ѯ�����������1��˵���Ѿ�ע��
#     ��Ӧ��         JSON{code:0,count:0/1,errmsg:ok}
#     ·�ɣ�         GET usernames/<username>/count/
#     ���裺
#         1.�����û���
#         2.�����û�����ѯ���ݿ�
#         3.������Ӧ

from django.views import View
from .models import User
from django.http import JsonResponse
class UserNameCountView(View):
    def get(self, request,username):
        # 1.�����û���
        # 2.�����û�����ѯ���ݿ�
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': '0',
                             'count': count,
                             'errmsg': 'ok'})
