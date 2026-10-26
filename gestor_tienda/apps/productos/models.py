from django.db import models

from apps.common.models import CommonModel


class Producto(CommonModel):
    pk_pro_id = models.BigAutoField(primary_key=True)
    pro_codigo = models.CharField("código", max_length=20, unique=True)
    pro_nombre = models.CharField("nombre", max_length=120)
    pro_descripcion = models.TextField("descripción", blank=True)
    pro_precio = models.DecimalField("precio de venta", max_digits=10, decimal_places=2)
    pro_activo = models.BooleanField("activo", default=True)

    class Meta:
        db_table = "tbl_producto"
        ordering = ["pro_nombre"]

    def __str__(self):
        return f"{self.pro_codigo} - {self.pro_nombre}"
