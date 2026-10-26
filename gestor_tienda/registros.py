from datetime import date
from decimal import Decimal

from apps.clientes.models import Cliente
from apps.compras.models import Compra
from apps.detalles_compra.models import DetalleCompra
from apps.detalles_venta.models import DetalleVenta
from apps.ejemplares.models import Ejemplar
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from apps.stocks.models import Stock
from apps.ventas.models import Venta

# ---------- Clientes ----------
ana, _ = Cliente.objects.get_or_create(
    cli_documento="1001001",
    defaults={
        "cli_nombres": "Ana",
        "cli_apellidos": "Gómez",
        "cli_correo": "ana@correo.com",
        "cli_telefono": "3001112233",
    },
)
luis, _ = Cliente.objects.get_or_create(
    cli_documento="1002002",
    defaults={
        "cli_nombres": "Luis",
        "cli_apellidos": "Pérez",
        "cli_correo": "luis@correo.com",
    },
)
marta, _ = Cliente.objects.get_or_create(
    cli_documento="1003003",
    defaults={
        "cli_nombres": "Marta",
        "cli_apellidos": "Ríos",
        "cli_correo": "marta@correo.com",
        "cli_telefono": "3104445566",
    },
)

# ---------- Proveedores ----------
tecno, _ = Proveedor.objects.get_or_create(
    prv_nit="900123456",
    defaults={
        "prv_razon_social": "TecnoDistribuciones S.A.S.",
        "prv_correo": "ventas@tecno.com",
    },
)
mayorista, _ = Proveedor.objects.get_or_create(
    prv_nit="900654321",
    defaults={"prv_razon_social": "Mayorista del Caribe", "prv_telefono": "6057281000"},
)

# ---------- Productos ----------
teclado, _ = Producto.objects.get_or_create(
    pro_codigo="TEC-001",
    defaults={
        "pro_nombre": "Teclado mecánico",
        "pro_descripcion": "Switches rojos",
        "pro_precio": Decimal("185000"),
    },
)
mouse, _ = Producto.objects.get_or_create(
    pro_codigo="MOU-002",
    defaults={"pro_nombre": "Mouse inalámbrico", "pro_precio": Decimal("65000")},
)
monitor, _ = Producto.objects.get_or_create(
    pro_codigo="MON-003",
    defaults={
        "pro_nombre": "Monitor 24 pulgadas",
        "pro_descripcion": "Full HD, IPS",
        "pro_precio": Decimal("720000"),
    },
)

# ---------- Stock (1:1 con Producto) ----------
Stock.objects.get_or_create(
    fk_pro=teclado, defaults={"sto_minimo": 2, "sto_ubicacion": "Estante A1"}
)
Stock.objects.get_or_create(
    fk_pro=mouse, defaults={"sto_minimo": 3, "sto_ubicacion": "Estante A2"}
)
Stock.objects.get_or_create(
    fk_pro=monitor, defaults={"sto_minimo": 1, "sto_ubicacion": "Bodega B1"}
)

# ---------- Compras a proveedores + productos por compra ----------
compra1, _ = Compra.objects.get_or_create(
    com_factura="FV-1001", defaults={"fk_prv": tecno, "com_fecha": date(2026, 10, 20)}
)
DetalleCompra.objects.get_or_create(
    fk_com=compra1,
    fk_pro=teclado,
    defaults={"dco_cantidad": 3, "dco_costo_unitario": Decimal("120000")},
)
DetalleCompra.objects.get_or_create(
    fk_com=compra1,
    fk_pro=mouse,
    defaults={"dco_cantidad": 4, "dco_costo_unitario": Decimal("40000")},
)

compra2, _ = Compra.objects.get_or_create(
    com_factura="MC-0450",
    defaults={"fk_prv": mayorista, "com_fecha": date(2026, 10, 22)},
)
DetalleCompra.objects.get_or_create(
    fk_com=compra2,
    fk_pro=monitor,
    defaults={"dco_cantidad": 2, "dco_costo_unitario": Decimal("550000")},
)

# ---------- Ejemplares (entidad débil): una unidad por cada producto comprado ----------
for detalle in DetalleCompra.objects.all():
    for numero in range(1, detalle.dco_cantidad + 1):
        Ejemplar.objects.get_or_create(fk_pro=detalle.fk_pro, eje_numero=numero)

# ---------- Ventas a clientes + productos por venta ----------
venta1, creada1 = Venta.objects.get_or_create(
    fk_cli=ana,
    ven_fecha=date(2026, 10, 24),
    defaults={"ven_metodo_pago": Venta.MetodoPago.TARJETA},
)
DetalleVenta.objects.get_or_create(
    fk_ven=venta1,
    fk_pro=teclado,
    defaults={"dve_cantidad": 1, "dve_precio_unitario": teclado.pro_precio},
)
DetalleVenta.objects.get_or_create(
    fk_ven=venta1,
    fk_pro=mouse,
    defaults={"dve_cantidad": 2, "dve_precio_unitario": mouse.pro_precio},
)

venta2, creada2 = Venta.objects.get_or_create(
    fk_cli=luis,
    ven_fecha=date(2026, 10, 25),
    defaults={"ven_metodo_pago": Venta.MetodoPago.EFECTIVO},
)
DetalleVenta.objects.get_or_create(
    fk_ven=venta2,
    fk_pro=monitor,
    defaults={"dve_cantidad": 1, "dve_precio_unitario": monitor.pro_precio},
)

# Marcar como vendidos los ejemplares que salieron en las ventas
for detalle in DetalleVenta.objects.all():
    vendidos = detalle.fk_pro.ejemplares.filter(eje_estado="VENDIDO").count()
    faltan = detalle.dve_cantidad - vendidos
    if faltan > 0:
        ids = detalle.fk_pro.ejemplares.filter(eje_estado="DISPONIBLE").values_list(
            "pk_eje_id", flat=True
        )[:faltan]
        Ejemplar.objects.filter(pk_eje_id__in=list(ids)).update(eje_estado="VENDIDO")

print("Datos de prueba creados.")
for modelo in (
    Cliente,
    Proveedor,
    Producto,
    Stock,
    Ejemplar,
    Compra,
    DetalleCompra,
    Venta,
    DetalleVenta,
):
    print(f"  {modelo._meta.db_table:<20} {modelo.objects.count()} registros")
