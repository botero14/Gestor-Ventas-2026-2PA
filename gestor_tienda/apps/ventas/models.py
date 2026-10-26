from django.db import models

from apps.common.models import CommonModel


class Venta(CommonModel):
    """Salida de mercancía: la tienda le vende productos a un cliente."""

    class MetodoPago(models.TextChoices):
        EFECTIVO = "EFECTIVO", "Efectivo"
        TARJETA = "TARJETA", "Tarjeta"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferencia"

    pk_ven_id = models.BigAutoField(primary_key=True)
    fk_cli = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="ventas",
        verbose_name="cliente",
    )
    ven_fecha = models.DateField("fecha")
    ven_metodo_pago = models.CharField(
        "método de pago",
        max_length=15,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO,
    )
    ven_productos = models.ManyToManyField(  # N:M resuelto con la tabla intermedia
        "productos.Producto",
        through="detalles_venta.DetalleVenta",
        related_name="ventas",
    )

    class Meta:
        db_table = "tbl_venta"
        ordering = ["-ven_fecha"]

    @property
    def ven_total(self):
        return sum(d.dve_cantidad * d.dve_precio_unitario for d in self.detalles.all())

    def __str__(self):
        return f"Venta #{self.pk_ven_id} - {self.fk_cli}"
