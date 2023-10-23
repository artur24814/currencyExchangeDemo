from django.contrib import admin
from django.urls import path, include

from core.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('currency_exchange.urls')),
]

if DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")),)
