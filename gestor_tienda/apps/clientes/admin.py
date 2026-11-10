from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(CommonAdmin):
    list_display = ("cli_documento", "fk_usu", "cli_telefono")
    search_fields = ("cli_documento", "fk_usu__first_name", "fk_usu__last_name")
    list_filter = ("created_at",)
    list_select_related = ("fk_usu",)  # trae el usuario en la misma consulta
