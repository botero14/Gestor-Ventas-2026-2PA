from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(CommonAdmin):
    list_display = ("cli_documento", "cli_nombres", "cli_apellidos", "cli_correo")
    search_fields = ("cli_documento", "cli_nombres", "cli_apellidos")
    list_filter = ("created_at",)
