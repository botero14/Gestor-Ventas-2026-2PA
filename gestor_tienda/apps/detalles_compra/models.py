from django.db import models

from apps.common.models import CommonModel


class DetalleCompra(CommonModel):
    """Productos por compra: tabla intermedia del N:M Compra–Producto."""

    pk_dco_id = models.BigAutoField(primary_key=True)
    fk_com = models.ForeignKey(
        "compras.Compra",
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="compra",
    )
    fk_pro = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT,
        related_name="detalles_compra",
        verbose_name="producto",
    )
    dco_cantidad = models.PositiveIntegerField("cantidad", default=1)
    dco_costo_unitario = models.DecimalField(
        "costo unitario", max_digits=10, decimal_places=2
    )

    class Meta:
        db_table = "tbl_detalle_compra"
        verbose_name = "producto de la compra"
        verbose_name_plural = "productos por compra"
        constraints = [
            models.UniqueConstraint(
                fields=["fk_com", "fk_pro"], name="producto_unico_por_compra"
            ),
        ]

    def __str__(self):
        return f"{self.dco_cantidad} x {self.fk_pro.pro_nombre}"
