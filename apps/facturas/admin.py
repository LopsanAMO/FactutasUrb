from django.contrib import admin
from .models import Factura, Concept


@admin.register(Factura)
class AdminFactura(admin.ModelAdmin):
    list_display = ('id', 'emisor', 'receiver', 'date_expedition', 'folio', '_id')
    list_filter = ('emisor', 'receiver', 'date_expedition')

admin.site.register(Concept)
