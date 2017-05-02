from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from api.exceptions import error404
from api.exceptions import error500

handler404 = error404
handler500 = error500

urlpatterns = [
    url(r'^api/', include('api.urls'), name='api'),

    url(r'^admin/', include(admin.site.urls)),
]
