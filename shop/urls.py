from django.conf.urls import url
from shop import views

urlpatterns = [
    url(r'^add/$', views.add_shop_car)
]
