from django.db import models

from apps.common.models import CommonModel


class Proveedor(CommonModel):
    pk_prv_id = models.BigAutoField(primary_key=True)
    prv_nit = models.CharField("NIT", max_length=15, unique=True)
    prv_razon_social = models.CharField("razón social", max_length=120)
    prv_correo = models.EmailField("correo", blank=True)
    prv_telefono = models.CharField("teléfono", max_length=20, blank=True)

    class Meta:
        db_table = "tbl_proveedor"
        ordering = ["prv_razon_social"]
        verbose_name_plural = "proveedores"

    def __str__(self):
        return self.prv_razon_social
