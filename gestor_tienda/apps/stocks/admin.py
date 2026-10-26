from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import Stock


@admin.register(Stock)
class StockAdmin(CommonAdmin):
    list_display = ("fk_pro", "sto_ubicacion", "sto_minimo", "sto_disponible")
    search_fields = ("fk_pro__pro_nombre", "sto_ubicacion")
    list_filter = ("sto_ubicacion",)
