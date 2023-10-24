from django.urls import path

from .api_views import (exchange_view, ListCurrencies)

app_name = 'currency_exchange'
urlpatterns = [
    path('', ListCurrencies.as_view(), name='list-currencies'),
    path('<str:sell>/<str:buys>/', exchange_view, name='exchange-view'),
]
