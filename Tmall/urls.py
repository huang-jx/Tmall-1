from django.conf.urls import url, include
from django.contrib import admin

from home import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url('account/', include('account.urls')),
    url('shop/', include('shop.urls')),
    url('home/', include('home.urls')),
]
