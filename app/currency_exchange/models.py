from django.db import models


class Currency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=250)
    symbol_native = models.CharField(max_length=20, null=True, blank=True)
    name_plural = models.CharField(max_length=100)


class Exchange(models.Model):
    sell = models.ForeignKey(Currency, related_name='seles', on_delete=models.SET_NULL, null=True)
    sell_quantity = models.DecimalField(max_digits=9, decimal_places=2)
    buys = models.ForeignKey(Currency, related_name='shopping', on_delete=models.SET_NULL, null=True)
    buys_quantity = models.DecimalField(max_digits=9, decimal_places=2)
    exchage_rate = models.DecimalField(max_digits=9, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
