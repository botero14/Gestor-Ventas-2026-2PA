from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(CommonAdmin):
    list_display = ("prv_nit", "prv_razon_social", "prv_telefono")
    search_fields = ("prv_nit", "prv_razon_social")
    list_filter = ("created_at",)
