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

'''


# 前后端分离,返回的时候不是模板 而是json数据
# python  对象 不支持json
def get_search_shop(request):
    result = {}
    try:
        keywords = request.GET.get('key')
        products = Product.objects.filter(name__contains=keywords)
        li = []
        for product in products:
            img = ProductImage.objects.filter(pid=product.id).values('id').first().get('id')
            # 对象 不支持json序列化   把python对象转化字典
            pro = model_to_dict(product)
            li.append(pro)
        result.update(state=200, msg='成功', data=li)
    except BaseException as e:
        result.update(state=-1, msg='失败')
    #     cls
    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), content_type='Application/json')
