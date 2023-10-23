from django.contrib import admin

from currency_exchange.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'symbol_native')
