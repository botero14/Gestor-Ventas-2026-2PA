from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import DetalleCompra


@admin.register(DetalleCompra)
class DetalleCompraAdmin(CommonAdmin):
    list_display = ("fk_com", "fk_pro", "dco_cantidad", "dco_costo_unitario")
    search_fields = ("fk_pro__pro_nombre", "fk_com__com_factura")
    list_filter = ("fk_pro",)
