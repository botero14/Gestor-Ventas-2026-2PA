from django.db import models

from apps.common.models import CommonModel


class Compra(CommonModel):
    """Ingreso de mercancía: la tienda le compra productos a un proveedor."""

    pk_com_id = models.BigAutoField(primary_key=True)
    fk_prv = models.ForeignKey(
        "proveedores.Proveedor",
        on_delete=models.PROTECT,
        related_name="compras",
        verbose_name="proveedor",
    )
    com_factura = models.CharField("factura del proveedor", max_length=30)
    com_fecha = models.DateField("fecha")
    com_productos = models.ManyToManyField(  # N:M resuelto con la tabla intermedia
        "productos.Producto",
        through="detalles_compra.DetalleCompra",
        related_name="compras",
    )

    class Meta:
        db_table = "tbl_compra"
        ordering = ["-com_fecha"]

    @property
    def com_total(self):
        return sum(d.dco_cantidad * d.dco_costo_unitario for d in self.detalles.all())

    def __str__(self):
        return f"Compra #{self.pk_com_id} - {self.fk_prv}"