from django.db import models
# !/usr/bin/python
# -*- coding: gbk -*-
# Create your models here.

# 1.�Լ�����ģ��
# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     mobile = models.CharField(max_length=11, unique=True)


# 2.django�Դ�һ���û�ģ��
# ����û�ģ��������ļ����Լ��������֤
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = 'userManage'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
