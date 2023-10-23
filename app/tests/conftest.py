import pytest

from rest_framework.test import APIClient

from currency_exchange.models import Currency


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def currency_EUR():
    return Currency.objects.create(symbol="EUR", name="Euro", symbol_native="€", name_plural="Euros")


@pytest.fixture
def currency_PLN():
    return Currency.objects.create(symbol="PLN", name="Polish Zloty", symbol_native="zł", name_plural="Polish zlotys")
