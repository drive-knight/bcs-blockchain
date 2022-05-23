from django.db import models


class Transaction(models.Model):
    txid = models.CharField('ID транзакции', max_length=255, null=False, blank=False)
    description = models.CharField('Описание', max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.txid}'
