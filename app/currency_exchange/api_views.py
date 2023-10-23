from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Exchange
from .services import get_exange_rate
from .selectors import get_currency_obj


@api_view(['GET'])
def exchange_view(request, sell, buys):
    # uppercases arguments
    sell, buys = sell.upper(), buys.upper()

    # get currency objects
    currency_to_sell, currency_to_buys = get_currency_obj(sell, ['pk']), get_currency_obj(buys, ['pk'])

    # if this objects exists in db
    if currency_to_sell and currency_to_buys:
        data, status_code = get_exange_rate(request, sell, buys)

        # create an exchange object if the data has been successfully download
        if status_code == 200:
            Exchange.objects.create(sell=currency_to_sell, buys=currency_to_buys, exchange_rate=data['data'][buys])

        return Response(data, status=status.HTTP_200_OK)

    # inform user that this currency is not available
    else:
        if currency_to_sell:
            error_currency = buys
        else:
            error_currency = sell

        return Response(f'this ({error_currency}) currency is not available', status=status.HTTP_404_NOT_FOUND)
