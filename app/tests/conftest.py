import pytest
import random

from rest_framework.test import APIClient

from currency_exchange.models import Currency, Exchange


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def currency_EUR():
    return Currency.objects.create(symbol="EUR", name="Euro", symbol_native="€", name_plural="Euros")


@pytest.fixture
def currency_PLN():
    return Currency.objects.create(symbol="PLN", name="Polish Zloty", symbol_native="zł", name_plural="Polish zlotys")


@pytest.fixture
def currency_USD():
    return Currency.objects.create(symbol="USD", name="US Dollar", symbol_native="$", name_plural="US dollars")


@pytest.fixture
def currency_GBP():
    return Currency.objects.create(symbol="GBP", name="British Pound Sterling", symbol_native="£", name_plural="British pounds sterling")


@pytest.fixture
def exchange_objects(currency_EUR, currency_PLN, currency_USD, currency_GBP):
    list_objects_to_create = list()

    # most_frequent sales
    for _ in range(4):
        exchange_obj = Exchange(sell=currency_PLN,
                                buys=random.choice([currency_EUR, currency_USD]),
                                exchange_rate=round(random.uniform(0.99, 1.33), 10))
        list_objects_to_create.append(exchange_obj)

    # most_frequent shopping
    for _ in range(4):
        exchange_obj = Exchange(sell=random.choice([currency_EUR, currency_USD]),
                                buys=currency_GBP,
                                exchange_rate=round(random.uniform(0.99, 1.33), 10))
        list_objects_to_create.append(exchange_obj)

    return Exchange.objects.bulk_create(list_objects_to_create)
