from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TxAdmin(admin.ModelAdmin):
    list_display = ('pk', 'txid', 'description',)
    list_display_links = ('txid',)
