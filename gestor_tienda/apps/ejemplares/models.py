from django.db import models

from apps.common.models import CommonModel


class Ejemplar(CommonModel):
    """Entidad débil: cada unidad física de un producto."""

    class Estado(models.TextChoices):
        DISPONIBLE = "DISPONIBLE", "Disponible"
        VENDIDO = "VENDIDO", "Vendido"
        DANADO = "DANADO", "Dañado"

    pk_eje_id = models.BigAutoField(primary_key=True)
    fk_pro = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="ejemplares",
        verbose_name="producto",
    )
    eje_numero = models.PositiveIntegerField("número")
    eje_estado = models.CharField(
        "estado", max_length=10, choices=Estado.choices, default=Estado.DISPONIBLE
    )

    class Meta:
        db_table = "tbl_ejemplar"
        ordering = ["fk_pro", "eje_numero"]
        verbose_name_plural = "ejemplares"
        constraints = [
            # Identificación de la entidad débil: dueño + clave parcial
            models.UniqueConstraint(
                fields=["fk_pro", "eje_numero"], name="ejemplar_unico_por_producto"
            ),
        ]

    def __str__(self):
        return f"{self.fk_pro.pro_nombre} #{self.eje_numero}"
