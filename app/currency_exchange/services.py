import os
import requests
from requests.exceptions import ConnectionError


def get_exange_rate(request, sell, buys):
    # for testing purposes
    if request.GET.get('testing'):
        url = f'https://httpbin.org/get?currencies={buys}&base_currency={sell}'
        response = requests.get(url)

        test_data = response.json()
        test_data['data'] = {buys: '19.1299883'}

        return test_data, response.status_code

    url = os.environ.get('BASE_CURRENCY_URL')
    api_key = os.environ.get('API_CURRENCY_KEY')
    url = f'{url}latest?apikey={api_key}&currencies={buys}&base_currency={sell}'

    try:
        response = requests.get(url)

        data = response.json()
        return data, response.status_code

    except ConnectionError as e:
        return {'error': str(e)}, 405
