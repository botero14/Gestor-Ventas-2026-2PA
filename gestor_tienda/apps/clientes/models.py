from django.db import models

from apps.common.models import CommonModel


class Cliente(CommonModel):
    pk_cli_id = models.BigAutoField(primary_key=True)
    cli_documento = models.CharField("documento", max_length=15, unique=True)
    cli_nombres = models.CharField("nombres", max_length=60)
    cli_apellidos = models.CharField("apellidos", max_length=60)
    cli_correo = models.EmailField("correo", unique=True)
    cli_telefono = models.CharField("teléfono", max_length=20, blank=True)

    class Meta:
        db_table = "tbl_cliente"
        ordering = ["cli_apellidos", "cli_nombres"]

    def __str__(self):
        return f"{self.cli_nombres} {self.cli_apellidos}"
