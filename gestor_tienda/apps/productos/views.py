from django.contrib import messages
from django.db import transaction
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.stocks.models import Stock
from .forms import ProductoForm
from .models import Producto

# Ninguna de estas vistas valida el login ni el rol: de eso se encarga
# RolMiddleware (apps/common/middleware.py) antes de que lleguen aquí.


def lista_productos(request):
    """READ: listado con búsqueda opcional por código o nombre."""
    # select_related trae el stock en la misma consulta (JOIN) y evita
    # una consulta extra por cada fila de la tabla
    productos = Producto.objects.select_related("stock")

    # El cliente solo ve los productos activos
    if request.user.es_cliente:
        productos = productos.filter(pro_activo=True)

    buscar = request.GET.get("q", "").strip()
    if buscar:
        productos = productos.filter(
            Q(pro_codigo__icontains=buscar) | Q(pro_nombre__icontains=buscar)
        )

    return render(
        request,
        "productos/lista.html",
        {"productos": productos, "buscar": buscar},
    )


def crear_producto(request):
    """CREATE: GET muestra el formulario vacío, POST lo valida y guarda."""
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                producto = form.save()
                # Todo producto nace con su registro de stock en cero (relación 1:1)
                Stock.objects.create(fk_pro=producto)
            messages.success(request, f"Producto {producto.pro_codigo} creado.")
            return redirect("productos:lista")
    else:
        form = ProductoForm()

    return render(
        request,
        "productos/formulario.html",
        {"form": form, "titulo": "Nuevo producto"},
    )


def editar_producto(request, pk):
    """UPDATE: el mismo formulario, pero cargado con la instancia existente."""
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Producto {producto.pro_codigo} actualizado.")
            return redirect("productos:lista")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        "productos/formulario.html",
        {"form": form, "titulo": f"Editar {producto.pro_nombre}"},
    )


def eliminar_producto(request, pk):
    """DELETE: GET pide confirmación, POST elimina."""
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        try:
            producto.delete()
            messages.success(request, f"Producto {producto.pro_codigo} eliminado.")
        except ProtectedError:
            # on_delete=PROTECT en los detalles de compra/venta impide borrar
            # un producto que ya tiene movimientos
            messages.error(
                request,
                "No se puede eliminar: el producto ya tiene compras o ventas. "
                "Puedes desactivarlo desde Editar.",
            )
        return redirect("productos:lista")

    return render(request, "productos/eliminar.html", {"producto": producto})
