from django.contrib import admin

from currency_exchange.models import Currency, Exchange


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'symbol_native')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('sell', 'buys', 'exchange_rate', 'timestamp')
