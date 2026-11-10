from django.db.models import F
from django.shortcuts import render

from apps.clientes.models import Cliente
from apps.productos.models import Producto
from apps.stocks.models import Stock
from apps.ventas.models import Venta


def inicio(request):
    """Panel de entrada: muestra cifras distintas según el rol."""
    contexto = {
        "total_productos": Producto.objects.filter(pro_activo=True).count(),
    }

    if not request.user.es_cliente:
        contexto["total_clientes"] = Cliente.objects.count()
        contexto["total_ventas"] = Venta.objects.count()
        # Productos que ya llegaron o bajaron del mínimo: hay que reponer
        contexto["por_reponer"] = (
            Stock.objects.select_related("fk_pro")
            .filter(sto_cantidad__lte=F("sto_minimo"))
            .order_by("sto_cantidad")
        )

    return render(request, "common/inicio.html", contexto)
