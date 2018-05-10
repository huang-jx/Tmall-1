import json

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect

# 序列化   ---- 生成json数据
# 反序列化 ----- 解析json数据
from home.models import Product, ProductImage, Category, CategorySub, Banner, BaseModel, Review, OrderItem


def index(request):
    return redirect('http://127.0.0.1:8000/static/index.html')

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


# django  rest

# 合理的合并请求
def get_category_data(reqeust):
    """
    获取分类菜单的数据
    :return:
    """
    result = {}
    try:
        cate_list = Category.objects.all()
        banners = Banner.qs_to_dict(Banner.objects.all())
        result.update(banners=banners)
        li = []
        for cate in cate_list:
            # select *  from  categorysub where cid=60
            # 获取一级菜单对应的二级菜单的数据 [cate_sub]
            sub_list = CategorySub.objects.filter(cid=cate.id)
            # 将queryset对象转化成 列表套字典
            cate.subs = Category.qs_to_dict(sub_list)
            li.append(cate.to_dict())
        result.update(state=200, msg='success', data=li)
    except:
        result.update(state=200, msg='查询失败')

    return HttpResponse(json.dumps(result), content_type='Application/json')


# 分类信息表---一对多-->产品表---一对多--->产品图片表

# class cate:
#     products = [product,...]
#
# class product:
#     imgs= [img,....]
#
# class img:
#     pass


def get_shop_data(reqeust):
    result = {}
    # 保存分类信息的数据
    li = []
    try:
        # 查询分类信息表
        # SELECT *  FROM  category
        cates = Category.objects.all()

        for cate in cates:
            # Product.objects.filter(cid=cate.id)
            # 查询每个分类的商品信息
            products = cate.product_set.all()
            # 遍历商品信息  通过商品对象来获取图片的信息
            for product in products:
                # 商品跟图片表之前的关系是一对多的关系
                # SELECT  * FROM  PRODUCTIMAGE WHERE PID=PRODUCT.ID
                product.imgs = BaseModel.qs_to_dict(product.product_image.all())

            # 商品信息添加到每个分类对象里
            cate.products = BaseModel.qs_to_dict(products)
            li.append(cate.to_dict())
        result.update(state=200, msg='success', data=li)
    except:
        result.update(state=200, msg='查询失败')

    return HttpResponse(json.dumps(result), content_type='Application/json')


def get_shop_detail(request):
    result = {}
    pid = request.GET.get('pid')
    try:
        product = Product.objects.get(id=pid)
        # 获取详情图片数据
        img_queryset = product.product_image.filter(type='type_single')
        product.imgs = BaseModel.qs_to_dict(img_queryset)
        # Review.objects.filter(pid=pid).count()
        # 评论数据
        product.comment_count = product.review_set.count()
        # 获取产品的销售量
        # product.orderitem_set.aggregate(count=Sum('number'))  字典
        number_dict = product.orderitem_set.aggregate(sum=Sum('number'))
        product.sale_count = number_dict.get('sum')
        result.update(state=200, msg='success', data=product.to_dict())
    except Exception as e:
        print(e)
        # -2 表示商品信息不存在
        result.update(state=-2, msg='查询失败')
    return HttpResponse(json.dumps(result), content_type='Application/json')
