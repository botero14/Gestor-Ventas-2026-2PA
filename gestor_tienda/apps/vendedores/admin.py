from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import Vendedor


@admin.register(Vendedor)
class VendedorAdmin(CommonAdmin):
    list_display = ("vdr_codigo", "fk_usu", "vdr_fecha_ingreso")
    search_fields = ("vdr_codigo", "fk_usu__first_name", "fk_usu__last_name")
    list_select_related = ("fk_usu",)
