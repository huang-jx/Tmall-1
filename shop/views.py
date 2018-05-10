from django.http import HttpResponse

from home.models import ShopCar, User, Product


# rest
# get 获取数据
# post 提交数据
# put  修改数据
# delete 删除
def add_shop_car(request):
    if request.method == 'POST':
        try:
            uid = request.POST.get('uid', 1)
            pid = request.POST.get('pid')
            num = request.POST.get('num')
            ShopCar.objects.get_or_create(uid=User.objects.get(id=uid), pid=Product.objects.get(
                id=pid), num=num)
            return HttpResponse('成功', content_type='Application/json')
        except BaseException as e:
            return HttpResponse('保存失败', content_type='Application/json')
    else:
        return HttpResponse('错误的请求方式', content_type='Application/json')
