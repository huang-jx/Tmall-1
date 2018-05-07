import datetime
from decimal import Decimal

from django.db import models

# DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"
# DATE_FORMAT = "%Y/%m/%d"
from django.db.models import QuerySet


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def to_dict(self):
        """
        把对象转化字典
        """
        #  内置函数 能获取对象的所有的
        # .keys 获取所有的变量的名称 返回的是一个列表

        dic = {}
        for key in vars(self).keys():
            if not key.startswith('_'):
                # getattr 通过key来获取值 参数一  对象  参数二 key  参数三 默认值
                if isinstance(getattr(self, key), datetime.date):
                    dic[key] = datetime.date.strftime(getattr(self, key), '%Y%m%d')
                elif isinstance(getattr(self, key), datetime.datetime):
                    dic[key] = datetime.datetime.strftime(getattr(self, key), '%Y%m%d %H%M%S')
                elif isinstance(getattr(self, key), Decimal):
                    dic[key] = float(getattr(self, key))
                else:
                    dic[key] = getattr(self, key)
        return dic

    @staticmethod
    def qs_to_dict(qs=None):
        """
        将QuerySet对象转化成li套字典
        :param qs:
        :return:
        """
        if isinstance(qs, QuerySet):
            li = [model.to_dict() for model in qs]
        return li

    def to_json(self):
        pass


class Banner(BaseModel):
    bid = models.AutoField(primary_key=True)
    path = models.CharField(max_length=32)

    class Meta:
        db_table = 't_banner'


class Category(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'category'


class CategorySub1(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='cid', blank=True, null=True)

    class Meta:
        db_table = 'category_sub1'


class CategorySub2(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    cs1id = models.ForeignKey(CategorySub1, models.DO_NOTHING, db_column='cs1id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_sub2'


class CategorySub(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='cid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categorysub'


class Order(models.Model):
    ordercode = models.CharField(db_column='orderCode', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    address = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    usermessage = models.CharField(db_column='userMessage', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    paydate = models.DateTimeField(db_column='payDate', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='deliveryDate', blank=True, null=True)  # Field name made lowercase.
    confirmdate = models.DateTimeField(db_column='confirmDate', blank=True, null=True)  # Field name made lowercase.
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    pid = models.ForeignKey('Product', models.DO_NOTHING, db_column='pid', blank=True, null=True)
    oid = models.IntegerField(blank=True, null=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)


class Product(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(db_column='subTitle', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    orignal_price = models.FloatField(db_column='orignalPrice', blank=True, null=True)  # Field name made lowercase.
    promote_price = models.FloatField(db_column='promotePrice', blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(blank=True, null=True)
    cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='cid', blank=True, null=True)
    create_date = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    img_list = {}

    class Meta:
        db_table = 'product'


class ProductImage(BaseModel):
    pid = models.ForeignKey(Product, models.DO_NOTHING, db_column='pid', related_name='product_image', blank=True,
                            null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'productimage'


class Property(models.Model):
    cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='cid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'property'

        managed = False


class PropertyValue(models.Model):
    pid = models.IntegerField(blank=True, null=True)
    ptid = models.ForeignKey(Property, models.DO_NOTHING, db_column='ptid', blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'propertyvalue'


class Review(models.Model):
    content = models.CharField(max_length=4000, blank=True, null=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    pid = models.ForeignKey(Product, models.DO_NOTHING, db_column='pid', blank=True, null=True)
    create_date = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'review'


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user'
