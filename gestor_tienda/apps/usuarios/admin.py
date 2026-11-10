from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # UserAdmin ya trae el formulario de contraseña; solo agregamos el rol
    list_display = ("username", "first_name", "last_name", "email", "usu_rol")
    list_filter = ("usu_rol", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Rol en la tienda", {"fields": ("usu_rol",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rol en la tienda", {"fields": ("usu_rol",)}),
    )
