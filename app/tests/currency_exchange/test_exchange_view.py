import pytest
from decimal import Decimal

from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext

from currency_exchange.models import Exchange


@pytest.mark.django_db()
def test_exchange_view(api_client, currency_EUR, currency_PLN):
    """Fetch with arguments 'pln', 'eur', with existing currency in db return exchange rate for pln to eur"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:exchange-view', kwargs={'sell': 'pln', 'buys': 'eur'}) + '?testing=True')

        assert len(connection.queries) <= 3

        assert response.status_code == 200
        assert response.data['args'] == {'base_currency': 'PLN', 'currencies': 'EUR'}
        assert response.data['data'] == {'EUR': '19.1299883'}

    # check created exchange object
    exchange_obj = Exchange.objects.first()

    assert exchange_obj.sell == currency_PLN
    assert exchange_obj.buys == currency_EUR
    assert exchange_obj.exchange_rate == Decimal('19.1299883')


@pytest.mark.django_db()
def test_exchange_view_error_first_currency(api_client, currency_EUR, currency_PLN):
    """Fetch with arguments 'pl', 'eur' ('pl' wrong argument), with existing currency in db return 404"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:exchange-view', kwargs={'sell': 'pl', 'buys': 'eur'}))

        assert len(connection.queries) <= 3

        assert response.status_code == 404
        assert response.data == 'this (PL) currency is not available'


@pytest.mark.django_db()
def test_exchange_view_error_second_currency(api_client, currency_EUR, currency_PLN):
    """Fetch with arguments 'pln', 'er' ('er' wrong argument), with existing currency in db return 404"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:exchange-view', kwargs={'sell': 'pln', 'buys': 'er'}))

        assert len(connection.queries) <= 3

        assert response.status_code == 404
        assert response.data == 'this (ER) currency is not available'


@pytest.mark.django_db()
def test_exchange_view_error_bouth_currencies(api_client, currency_EUR, currency_PLN):
    """Fetch with arguments 'pn', 'er' ('pl' and 'er' wrong arguments), with existing currency in db return 404"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:exchange-view', kwargs={'sell': 'pn', 'buys': 'er'}))

        assert len(connection.queries) <= 3

        assert response.status_code == 404
        assert response.data == 'this (PN) currency is not available'
