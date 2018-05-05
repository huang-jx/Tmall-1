from django.conf.urls import url, include
from django.contrib import admin

from home import views

urlpatterns = [
    url(r'^$/', views.index, name='index'),
    url('admin/', admin.site.urls),
    url('account/', include('account.urls')),
    url('shop/', admin.site.urls),
    url('home/', admin.site.urls),
]
