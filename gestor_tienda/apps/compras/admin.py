from django.contrib import admin

from apps.common.admin import CommonAdmin
from apps.detalles_compra.models import DetalleCompra
from .models import Compra


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1


@admin.register(Compra)
class CompraAdmin(CommonAdmin):
    list_display = ("pk_com_id", "fk_prv", "com_factura", "com_fecha", "com_total")
    search_fields = ("com_factura", "fk_prv__prv_razon_social")
    list_filter = ("com_fecha", "fk_prv")
    inlines = [DetalleCompraInline]
