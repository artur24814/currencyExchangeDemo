from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currency/', include('currency_exchange.urls')),
]

urlpatterns += staticfiles_urlpatterns()

if DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")),)
