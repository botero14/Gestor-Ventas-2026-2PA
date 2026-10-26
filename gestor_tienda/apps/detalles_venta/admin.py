from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import DetalleVenta


@admin.register(DetalleVenta)
class DetalleVentaAdmin(CommonAdmin):
    list_display = ("fk_ven", "fk_pro", "dve_cantidad", "dve_precio_unitario")
    search_fields = ("fk_pro__pro_nombre", "fk_ven__fk_cli__cli_nombres")
    list_filter = ("fk_pro",)
