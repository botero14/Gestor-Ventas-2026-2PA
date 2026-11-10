from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Tabla única de usuarios del sistema.

    Hereda de AbstractUser: username, password, first_name, last_name,
    email, is_active, is_staff, is_superuser, last_login y date_joined.
    Solo agregamos el rol; los datos propios de cada rol viven en su
    tabla de perfil (tbl_cliente, tbl_vendedor) con una relación 1:1.
    """

    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        VENDEDOR = "VENDEDOR", "Vendedor"
        CLIENTE = "CLIENTE", "Cliente"

    pk_usu_id = models.BigAutoField(primary_key=True)
    usu_rol = models.CharField(
        "rol", max_length=10, choices=Rol.choices, default=Rol.CLIENTE
    )
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        db_table = "tbl_usuario"
        ordering = ["last_name", "first_name"]

    def save(self, *args, **kwargs):
        # El superusuario de createsuperuser siempre queda como administrador
        if self.is_superuser:
            self.usu_rol = self.Rol.ADMIN
        super().save(*args, **kwargs)

    # Atajos para preguntar el rol en vistas y plantillas: user.es_admin
    @property
    def es_admin(self):
        return self.usu_rol == self.Rol.ADMIN

    @property
    def es_vendedor(self):
        return self.usu_rol == self.Rol.VENDEDOR

    @property
    def es_cliente(self):
        return self.usu_rol == self.Rol.CLIENTE

    def __str__(self):
        return self.get_full_name() or self.username
