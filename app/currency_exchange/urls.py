from django.urls import path

from .api_views import (exchange_view)

app_name = 'currency_exchange'
urlpatterns = [
    path('<str:sell>/<str:buys>/', exchange_view, name='exchange-view')
]
