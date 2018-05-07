import json

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# 序列化   ---- 生成json数据
# 反序列化 ----- 解析json数据
from home.models import Product, ProductImage, Category, CategorySub


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


def get_category_data(reqeust):
    """
    获取分类菜单的数据
    :return:
    """
    result = {}
    try:
        cate_list = Category.objects.all()
        li = []
        for cate in cate_list:
            # select *  from  categorysub where cid=60
            # 获取一级菜单对应的二级菜单的数据 [cate_sub]
            sub_list = CategorySub.objects.filter(cid=cate.id)
            # 将queryset对象转化成 列表套字典
            cate.subs = cate.qs_to_dict(sub_list)
            li.append(cate.to_dict())
        result.update(state=200, msg='success', data=li)
    except:
        result.update(state=200, msg='查询失败')

    return HttpResponse(json.dumps(result), content_type='Application/json')
