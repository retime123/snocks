#coding=utf-8
from django.db import models

# Create your models here.
class FreshInfo(models.Model):
    fname = models.CharField(max_length=20)
    fpwd = models.CharField(max_length=40)#字符:sha1是32,hexdigest()是40
    femail = models.CharField(max_length=30)
    frecipients = models.CharField(max_length=20,default='')# 收件人
    faddress = models.CharField(max_length=100,default='')
    fyoubian = models.CharField(max_length=10,default='')
    fphone = models.CharField(max_length=20,default='')