from django.db import models

from apps.common.models import CommonModel


class Stock(CommonModel):
    pk_sto_id = models.BigAutoField(primary_key=True)
    fk_pro = (
        models.OneToOneField(  # 1:1 → cada producto tiene un único registro de stock
            "productos.Producto",
            on_delete=models.CASCADE,
            related_name="stock",
            verbose_name="producto",
        )
    )
    sto_minimo = models.PositiveIntegerField("stock mínimo", default=0)
    sto_ubicacion = models.CharField("ubicación en bodega", max_length=50)

    class Meta:
        db_table = "tbl_stock"
        verbose_name_plural = "stock"

    @property
    def sto_disponible(self):
        """Dato derivado: se calcula contando ejemplares, no se guarda."""
        return self.fk_pro.ejemplares.filter(eje_estado="DISPONIBLE").count()

    def __str__(self):
        return f"Stock de {self.fk_pro.pro_nombre}"
