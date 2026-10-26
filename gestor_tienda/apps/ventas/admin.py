from django.contrib import admin

from apps.common.admin import CommonAdmin
from apps.detalles_venta.models import DetalleVenta
from .models import Venta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(CommonAdmin):
    list_display = ("pk_ven_id", "fk_cli", "ven_fecha", "ven_metodo_pago", "ven_total")
    search_fields = (
        "fk_cli__cli_documento",
        "fk_cli__cli_nombres",
        "fk_cli__cli_apellidos",
    )
    list_filter = ("ven_fecha", "ven_metodo_pago")
    inlines = [DetalleVentaInline]
