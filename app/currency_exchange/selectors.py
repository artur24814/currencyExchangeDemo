from .models import Currency, Exchange
from django.core.paginator import Paginator
from django.db.models import Q, Count


def create_paginator_obj(queryset, page_number, objects_per_page=20):
    """Create paginator object"""
    paginator = Paginator(queryset, objects_per_page)
    page_obj = paginator.get_page(page_number)

    return page_obj


def get_currency_obj(cheking_currency, only_list):
    """Simple curency object filtering by symbol"""
    currency_obj = Currency.objects.only(*only_list).filter(symbol=cheking_currency).first()
    return currency_obj


def queryset_currencies(only_list, response, **kwargs):
    """Currencies objects queryset

    :in
        response : dict
        most_frequent : list[:bool]
        filter_currency : list[:str]
    :out
        queryset : QueryDict
    """

    most_frequent = kwargs.get('most_frequent', None)
    filter_currency = kwargs.get('filter_currency', None)
    queryset = list()

    # filter icontains by query
    if filter_currency:
        queryset = Currency.objects.filter(Q(symbol__icontains=filter_currency[0]) |
                                           Q(name__icontains=filter_currency[0]) |
                                           Q(name_plural__icontains=filter_currency[0]) |
                                           Q(symbol_native__icontains=filter_currency[0])).only(*only_list)

        # +plus filter this queryset by most frequently bought or sold currency
        if most_frequent and most_frequent[0] == 'seles' or most_frequent[0] == 'shopping':
            queryset = queryset.alias(nitem=Count(most_frequent[0])).order_by('-nitem')

    # filter by most frequently bought or sold currency
    elif most_frequent:
        if most_frequent[0] == 'seles' or most_frequent[0] == 'shopping':
            queryset = Currency.objects.only(*only_list).alias(nitem=Count(most_frequent[0])).order_by('-nitem')

    # all currencies
    else:
        queryset = Currency.objects.only(*only_list).all()

    # update response if error typing in most_frequent arguments
    if most_frequent:
        if most_frequent[0] != 'seles' and most_frequent[0] != 'shopping':
            response['---error typing'] = {'available_options': ['seles', 'shopping']}

    return queryset


def queryset_exchange_activity(only_list, response=None, **kwargs):
    """Exchange queryset objects, last 5 actions or all actions (update response dict, pagination info entry)

    :in
        response : dict, default None
        all_activity : list[:bool]
        page : list[:int]
        filter_activity : list[:str]
    :out
        queryset : QueryDict
    """

    many = kwargs.get('all_activity', None)
    page_number = kwargs.get('page', None)
    filter_q = kwargs.get('filter_activity', None)
    queryset = list()

    # convert page number to int
    if not page_number:
        page_number = 1
    else:
        page_number = page_number[0]

    # all_activity
    if many and page_number:
        # filter by question
        if filter_q:
            objects = Exchange.objects.filter(Q(sell__symbol__icontains=filter_q[0]) |
                                              Q(buys__symbol__icontains=filter_q[0]))\
                                              .only(*only_list)\
                                              .prefetch_related('sell', 'buys')\
                                              .order_by('-timestamp')
        # queryset all
        else:
            objects = Exchange.objects.only(*only_list).prefetch_related('sell', 'buys').all().order_by('-timestamp')

        # create paginator
        queryset = create_paginator_obj(objects, page_number)

        # updating response
        response['--current-page'] = int(page_number)
        response['--pages'] = queryset.paginator.num_pages

    # last 5 actions
    else:
        queryset = Exchange.objects.only(*only_list).prefetch_related('sell', 'buys').all().order_by('-timestamp')[:5]

    return queryset
