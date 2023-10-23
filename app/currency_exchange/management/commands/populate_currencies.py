import os
import requests

from django.core.management.base import BaseCommand

from currency_exchange.models import Currency


class Command(BaseCommand):

    help = 'Create currencies'

    def handle(self, *args, **kwargs):
        if Currency.objects.exists():
            self.stdout.write(self.style.ERROR('Currencies alredy exists'))
            return None

        url = os.environ.get('BASE_CURRENCY_URL')
        api_key = os.environ.get('API_CURRENCY_KEY')

        response = requests.get(url + f'currencies/?apikey={api_key}')

        data = response.json()

        list_to_create = list()

        for key, value in data['data'].items():
            curency_obj = Currency(symbol=value['code'],
                                   name=value['name'],
                                   symbol_native=value['symbol_native'],
                                   name_plural=value['name_plural'])
            list_to_create.append(curency_obj)

        Currency.objects.bulk_create(list_to_create)

        self.stdout.write(self.style.SUCCESS('Currencies created successfully'))
