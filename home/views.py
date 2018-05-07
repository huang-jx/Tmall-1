import json

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# 序列化   ---- 生成json数据
# 反序列化 ----- 解析json数据
from home.models import Product, ProductImage


def index(request):
    return render(request, 'index.html', {})


def get_head_data(request):
    return


'''
{}
[]()
字符串
数字
null
bool

'''


# 前后端分离,返回的时候不是模板 而是json数据
# python  对象不支持json


# 需要手动讲对象转化字典


# 变量 = 值
# # {key:value}
# [
#     {
#         'id': 值
#         'img_list': [
#             {},
#             {}
#         ]
#
#     }
#     ,
#     product,
#     ...

def get_search_shop(request):
    result = {}
    try:
        keywords = request.GET.get('key')
        products = Product.objects.filter(name__contains=keywords)
        li = []
        for product in products:
            product.img_list = product.qs_to_dict(ProductImage.objects.filter(pid=product.id))
            li.append((product.to_dict()))
        result.update(state=200, msg='成功', data=li)
    except BaseException as e:
        result.update(state=-1, msg='失败')
    return HttpResponse(json.dumps(result), content_type='Application/json')
