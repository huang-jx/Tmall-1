from django.conf.urls import url, include
from django.contrib import admin

from home import views

urlpatterns = [
    url('search/', views.get_search_shop)
]
