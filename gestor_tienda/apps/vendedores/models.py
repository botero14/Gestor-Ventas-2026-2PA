from django.conf import settings
from django.db import models

from apps.common.models import CommonModel


class Vendedor(CommonModel):
    """Perfil del rol VENDEDOR: el empleado que atiende las ventas."""

    pk_vdr_id = models.BigAutoField(primary_key=True)
    fk_usu = models.OneToOneField(  # 1:1 con tbl_usuario
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendedor",
        verbose_name="usuario",
    )
    vdr_codigo = models.CharField("código", max_length=10, unique=True)
    vdr_fecha_ingreso = models.DateField("fecha de ingreso")

    class Meta:
        db_table = "tbl_vendedor"
        ordering = ["vdr_codigo"]
        verbose_name_plural = "vendedores"

    def __str__(self):
        return f"{self.vdr_codigo} - {self.fk_usu}"
