from django.contrib import admin


class CommonAdmin(admin.ModelAdmin):
    """Configuración base que reutilizan todos los admin del proyecto."""

    readonly_fields = ("created_at", "updated_at")
