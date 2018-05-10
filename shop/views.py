from django.db.models import F, Q
from django.http import HttpResponse
from .utils import response_json
from home.models import ShopCar, User, Product
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
