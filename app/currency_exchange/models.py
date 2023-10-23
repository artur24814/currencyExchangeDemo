from django.db import models


class Currency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    symbol_native = models.CharField(max_length=20, null=True, blank=True)
    name_plural = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name} ({self.symbol})'


class Exchange(models.Model):
    sell = models.ForeignKey(Currency, related_name='seles', on_delete=models.SET_NULL, null=True)
    buys = models.ForeignKey(Currency, related_name='shopping', on_delete=models.SET_NULL, null=True)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=14)  # according to https://stackoverflow.com/a/47404379/21124442
    timestamp = models.DateTimeField(auto_now_add=True)
