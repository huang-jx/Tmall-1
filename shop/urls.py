from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^shop/', include('shop.urls')),
    url(r'^home/', include('home.urls')),
]
