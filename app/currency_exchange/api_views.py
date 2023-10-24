from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from .models import Exchange, Currency
from .services import get_exange_rate
from .selectors import (get_currency_obj,
                        queryset_currencies,
                        queryset_exchange_activity)


@api_view(['GET'])
def exchange_view(request, sell, buys):
    """Exchange currency rate view

    :in
        sell : str
        buys : str
    :out
        json Responce with currency rate for sell('base currency') to buys currency
        save rate in database
    """

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


class ListCurrencies(APIView):
    """
    List Currencies objects and list Exchanges objects

    serializers
    ---------
    ListCurrenciesSerializers
        model = Currency
    ListCurrenciesExchangeSerializers
        model = Exchange

    Methods
    --------
    [GET]
        return json with Currency objects and Exchanges objects

    Parameters
    --------
        most_frequent : str (seles/shopping)
        filter_currency : str
        all_activity : bool
        page : int
        filter_activity : str
    """

    class ListCurrenciesSerializers(serializers.ModelSerializer):
        """Serializing Currency model data"""
        class Meta:
            model = Currency
            fields = ('symbol', 'name', 'symbol_native', 'name_plural')

    class ListCurrenciesExchangeSerializers(serializers.ModelSerializer):
        """Serializing Exchange model data ,related fields to Currency model (sell, buys)"""
        sell = serializers.StringRelatedField(many=False)
        buys = serializers.StringRelatedField(many=False)

        class Meta:
            model = Exchange
            fields = ('sell', 'buys', 'exchange_rate', 'timestamp')

    def get(self, request):
        """
        filters:
            :Currrencies:
                filter_currency : str
                most_frequent : str and filter_currency : str
            :Exchanges:
                all_activity : bool
                page : int
                filter_activity : str

        sorting:
            :Currrencies:
                most_frequent:bool
        """
        response = dict()

        # list currencies
        currencies = queryset_currencies(('symbol', 'name', 'symbol_native', 'name_plural'), response, **request.GET)

        serializer_currency = self.ListCurrenciesSerializers(currencies, many=True)
        response["**CURENCIES**"] = serializer_currency.data

        # list exchanging activities
        exchanges = queryset_exchange_activity(('sell', 'buys', 'exchange_rate', 'timestamp'), response=response, **request.GET)

        serializer_exchange = self.ListCurrenciesExchangeSerializers(exchanges, many=True)
        response["**EXCHANGE ACTIVITY**"] = serializer_exchange.data

        return Response(response, status=status.HTTP_200_OK)
