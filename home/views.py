from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

# 序列化   ---- 生成json数据
# 反序列化 ----- 解析json数据
from home.models import Product, Productimage


def index(request):
    return render(request, 'index.html', {})


def get_head_data(request):
    return


# 前后端分离,返回的时候不是模板 而是json数据
def get_search_shop(request):
    keywords = request.GET.get('key')
    # queryset
    products = Product.objects.filter(name__contains=keywords)
    for product in products:
        product.img = Productimage.objects.filter(pid=product.id).first()
    data = serializers.serialize('json', products)
    return HttpResponse(data, content_type='Application/json')
