import uuid
# django rest fromework
# flask
from django.db.models import F, Q
from django.http import HttpResponse
from .utils import response_json
from home.models import ShopCar, User, Product, Order, OrderItem
from home.models import BaseModel


# flask
# rest
# get 获取数据
# post 提交数据
# put  修改数据
# delete 删除
# 自增
def add_shop_car(request):
    if request.method == 'POST':
        try:
            uid = request.POST.get('uid', 0)
            pid = request.POST.get('pid', 0)
            num = request.POST.get('num', 0)
            if uid and pid and num:
                shop_cars = ShopCar.objects.filter(uid=uid, pid=pid)
                if not shop_cars:
                    ShopCar.objects.create(uid=User.objects.get(id=uid), pid=Product.objects.get(id=pid), num=num)
                else:
                    shop_car = shop_cars.first()
                    shop_car.num = F('num') + int(num)
                    shop_car.save()
            return HttpResponse('成功', content_type='Application/json')
        except BaseException as e:
            return HttpResponse('保存失败', content_type='Application/json')
    else:
        return HttpResponse('错误的请求方式', content_type='Application/json')


# 定义个 result
# 如果正常获取数据  数据data  状态吗  错误的信息
# 如果异常         状态吗    错误的信息
# 最后吧结果集返回(json数据)

def shop_car_list(request):
    uid = request.GET.get('uid')
    if uid:
        try:
            cars = ShopCar.objects.filter(Q(uid=uid) & Q(status=1))
            for car in cars:
                car.product = car.pid.to_dict()
            return response_json(data=BaseModel.qs_to_dict(cars))
        except Exception as e:
            return response_json(status=400, msg='查询失败')
    else:
        return response_json(status=400, msg='参数错误')


# 结算的功能
# 生成订单号 ----> 发起支付
# 必须uid 总价格 商品相关的信息  pid
def total_shop(request):
    # 前端  json 数据  后台解析
    uid = request.POST.get('uid')
    total = request.POST.get('total')
    pid = request.POST.get('pid')

    # 订单号  用户id
    # 生成订单号
    order_code = uuid.uuid1()
    # 生产订单
    order = Order.objects.create(uid=uid, ordercode=order_code)
    # 清空购物车
    shop_car = ShopCar.objects.filter(uid=uid)
    for car in shop_car:
        car.status = 0
        car.save()
        # 把购买的商品信息 保存到 oderitem表
        OrderItem.objects.create(oid=order.id, uid=uid, pid=car.pid, number=car.num)
    # 支付方式

    #   发起支付
