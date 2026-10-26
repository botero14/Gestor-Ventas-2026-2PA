from django.db import models


class CommonModel(models.Model):
    """Campos de auditoría que heredan todos los modelos del proyecto."""

    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        abstract = True
