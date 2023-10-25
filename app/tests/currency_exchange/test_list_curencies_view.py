import pytest

from django.urls import reverse
from django.db import connection
from django.test.utils import CaptureQueriesContext


@pytest.mark.django_db()
def test_list_currencies_lack_exchanges_view(api_client, currency_EUR, currency_PLN):
    """When we have 0 exchanges objects in database"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies'))

        assert len(connection.queries) <= 4

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 2
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 0


@pytest.mark.django_db()
def test_list_currencies_simple_view(api_client, exchange_objects):
    """Simple fetch with no get arguments"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies'))

        assert len(connection.queries) <= 4

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 4
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 5


@pytest.mark.django_db()
def test_list_currencies_filter_currency_view(api_client, exchange_objects):
    """Fetch with '?filter_currency=eu' argument return one curency"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies') + '?filter_currency=eu')

        assert len(connection.queries) <= 4

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 1
        assert response.json()['**CURENCIES**'][0]['name'] == 'Euro'
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 5


@pytest.mark.django_db()
def test_list_currencies_sort_sele_currency_view(api_client, exchange_objects):
    """Fetch with '?most_frequent=seles' argument return sortrd curencies, first of them is Polish Zloty"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies') + '?most_frequent=seles')

        assert len(connection.queries) <= 4

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 4
        assert response.json()['**CURENCIES**'][0]['name'] == 'Polish Zloty'
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 5


@pytest.mark.django_db()
def test_list_currencies_sort_buying_currency_view(api_client, exchange_objects):
    """Fetch with '?most_frequent=shopping' argument return sorted currencies, first of them is Polish Zloty"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies') + '?most_frequent=shopping')

        assert len(connection.queries) <= 4

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 4
        assert response.json()['**CURENCIES**'][0]['name'] == 'British Pound Sterling'
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 5


@pytest.mark.django_db()
def test_list_currencies_filter_and_sort_sele_currency_view(api_client, exchange_objects):
    """Fetch with '?filter_currency=p&most_frequent=seles' argument return sorted and filtered currencies (PLN, GBP), first of them is Polish Zloty"""
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies') + '?filter_currency=p&most_frequent=seles')

        assert len(connection.queries) <= 4

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 2
        assert response.json()['**CURENCIES**'][0]['name'] == 'Polish Zloty'
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 5


@pytest.mark.django_db()
def test_list_currencies_all_activity_view(api_client, exchange_objects):
    """
    Fetch with '?all_activity=True' argument
    return all paginating exchanges activity (max page=20, exchanges_obj=8 pages = 1/1)
    """
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies') + '?all_activity=True')

        assert len(connection.queries) <= 5

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 4
        assert response.json()['--current-page'] == 1
        assert response.json()['--pages'] == 1
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 8


@pytest.mark.django_db()
def test_list_currencies_filtered_all_activity_view(api_client, exchange_objects):
    """
    Fetch with '?all_activity=True&filter_activity=pl' argument
    return all paginating exchanges activity filtering bu 'pl' (exchanges_obj=4 pages = 1/1)
    """
    with CaptureQueriesContext(connection):
        response = api_client.get(reverse('currency_exchange:list-currencies') + '?all_activity=True&filter_activity=pl')

        assert len(connection.queries) <= 5

        assert response.status_code == 200
        assert len(response.json()['**CURENCIES**']) == 4
        assert response.json()['--current-page'] == 1
        assert response.json()['--pages'] == 1
        assert len(response.json()['**EXCHANGE ACTIVITY**']) == 4
