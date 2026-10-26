from django.contrib import admin

from apps.common.admin import CommonAdmin
from .models import Ejemplar


@admin.register(Ejemplar)
class EjemplarAdmin(CommonAdmin):
    list_display = ("fk_pro", "eje_numero", "eje_estado", "created_at")
    search_fields = ("fk_pro__pro_nombre", "fk_pro__pro_codigo")
    list_filter = ("eje_estado", "fk_pro")
