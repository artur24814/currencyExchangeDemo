from .models import Currency


def get_currency_obj(cheking_currency, only_list):
    currency_obj = Currency.objects.only(*only_list).filter(symbol=cheking_currency).first()
    return currency_obj
