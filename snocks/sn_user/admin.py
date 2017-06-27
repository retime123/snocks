
#coding=utf-8
from django.contrib import admin
from models import *
# Register your models here.

class FreshInfoAdmin(admin.ModelAdmin):
    list_display = ['id','fname','femail']
    list_per_page = 10  # 每页显示10个数据
    search_fields = ['fname'] # 搜索:以fname方式搜索


admin.site.register(FreshInfo,FreshInfoAdmin)