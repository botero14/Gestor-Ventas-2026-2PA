from django.shortcuts import render

from .models import Cliente


def lista_clientes(request):
    # Solo ADMIN y VENDEDOR llegan aquí (ver RUTAS_POR_ROL en el middleware)
    clientes = Cliente.objects.select_related("fk_usu")
    return render(request, "clientes/lista.html", {"clientes": clientes})
