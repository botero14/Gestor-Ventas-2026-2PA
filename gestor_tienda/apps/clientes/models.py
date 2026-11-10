from django.conf import settings
from django.db import models

from apps.common.models import CommonModel


class Cliente(CommonModel):
    """
    Perfil del rol CLIENTE.

    Nombres, apellidos y correo ya están en tbl_usuario, por eso aquí
    solo quedan los datos que son exclusivos del cliente.
    """

    pk_cli_id = models.BigAutoField(primary_key=True)
    fk_usu = models.OneToOneField(  # 1:1 → un usuario tiene a lo sumo un perfil de cliente
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cliente",
        verbose_name="usuario",
    )
    cli_documento = models.CharField("documento", max_length=15, unique=True)
    cli_telefono = models.CharField("teléfono", max_length=20, blank=True)
    cli_direccion = models.CharField("dirección", max_length=120, blank=True)

    class Meta:
        db_table = "tbl_cliente"
        ordering = ["fk_usu__last_name", "fk_usu__first_name"]

    def __str__(self):
        return str(self.fk_usu)
