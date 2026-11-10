from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F

from apps.common.models import CommonModel
from apps.stocks.models import Stock


class DetalleVenta(CommonModel):
    """Productos por venta: tabla intermedia del N:M Venta–Producto."""

    pk_dve_id = models.BigAutoField(primary_key=True)
    fk_ven = models.ForeignKey(
        "ventas.Venta",
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="venta",
    )
    fk_pro = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT,
        related_name="detalles_venta",
        verbose_name="producto",
    )
    dve_cantidad = models.PositiveIntegerField("cantidad", default=1)
    dve_precio_unitario = models.DecimalField(
        "precio unitario", max_digits=10, decimal_places=2
    )

    class Meta:
        db_table = "tbl_detalle_venta"
        verbose_name = "producto de la venta"
        verbose_name_plural = "productos por venta"
        constraints = [
            models.UniqueConstraint(
                fields=["fk_ven", "fk_pro"], name="producto_unico_por_venta"
            ),
        ]

    def clean(self):
        # Los formularios (incluido el admin) llaman a clean() antes de guardar
        if self._state.adding and self.fk_pro_id:
            stock = Stock.objects.filter(fk_pro_id=self.fk_pro_id).first()
            if stock is None or stock.sto_cantidad < self.dve_cantidad:
                raise ValidationError("No hay unidades suficientes en stock.")

    def save(self, *args, **kwargs):
        es_nuevo = self._state.adding
        super().save(*args, **kwargs)
        # Al registrar la venta sale mercancía de la bodega
        if es_nuevo:
            Stock.objects.filter(fk_pro=self.fk_pro).update(
                sto_cantidad=F("sto_cantidad") - self.dve_cantidad
            )

    def __str__(self):
        return f"{self.dve_cantidad} x {self.fk_pro.pro_nombre}"
