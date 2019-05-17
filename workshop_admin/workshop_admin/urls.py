from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    url(r'^ajax_select/', include(ajax_select_urls)),
    path('grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
]
