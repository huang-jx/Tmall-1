from django.conf.urls import url

from home import views

urlpatterns = [
    url('search/', views.get_search_shop),
    url('cates/', views.get_category_data),
    url('shops/', views.get_shop_data),
    url('detail/', views.get_shop_detail),
]
