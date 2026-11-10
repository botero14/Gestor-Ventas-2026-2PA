"""
Datos de prueba.

Uso:  python manage.py shell -c "exec(open('registros.py', encoding='utf-8').read())"

Contraseña de todos los usuarios: tienda2026
"""

from datetime import date
from decimal import Decimal

from apps.clientes.models import Cliente
from apps.compras.models import Compra
from apps.detalles_compra.models import DetalleCompra
from apps.detalles_venta.models import DetalleVenta
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from apps.stocks.models import Stock
from apps.usuarios.models import Usuario
from apps.vendedores.models import Vendedor
from apps.ventas.models import Venta

CLAVE = "tienda2026"


def crear_usuario(username, nombres, apellidos, rol, **extra):
    """Crea el usuario una sola vez; create_user se encarga de cifrar la contraseña."""
    usuario = Usuario.objects.filter(username=username).first()
    if usuario is None:
        usuario = Usuario.objects.create_user(
            username=username,
            password=CLAVE,
            first_name=nombres,
            last_name=apellidos,
            email=f"{username}@correo.com",
            usu_rol=rol,
            **extra,
        )
    return usuario


# ---------- Usuarios: uno por rol ----------
crear_usuario(
    "admin", "Administrador", "Tienda", Usuario.Rol.ADMIN, is_staff=True, is_superuser=True
)

carlos = crear_usuario("carlos", "Carlos", "Mendoza", Usuario.Rol.VENDEDOR)
vendedor, _ = Vendedor.objects.get_or_create(
    fk_usu=carlos, defaults={"vdr_codigo": "V-001", "vdr_fecha_ingreso": date(2026, 2, 1)}
)

# ---------- Clientes (usuario + perfil 1:1) ----------
datos_clientes = [
    ("ana", "Ana", "Gómez", "1001001", "3001112233"),
    ("luis", "Luis", "Pérez", "1002002", ""),
    ("marta", "Marta", "Ríos", "1003003", "3104445566"),
]
clientes = {}
for username, nombres, apellidos, documento, telefono in datos_clientes:
    usuario = crear_usuario(username, nombres, apellidos, Usuario.Rol.CLIENTE)
    clientes[username], _ = Cliente.objects.get_or_create(
        fk_usu=usuario,
        defaults={"cli_documento": documento, "cli_telefono": telefono},
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

# ---------- Stock (1:1 con Producto); arranca en cero ----------
Stock.objects.get_or_create(
    fk_pro=teclado, defaults={"sto_minimo": 2, "sto_ubicacion": "Estante A1"}
)
Stock.objects.get_or_create(
    fk_pro=mouse, defaults={"sto_minimo": 3, "sto_ubicacion": "Estante A2"}
)
Stock.objects.get_or_create(
    fk_pro=monitor, defaults={"sto_minimo": 1, "sto_ubicacion": "Bodega B1"}
)

# ---------- Compras: cada detalle nuevo suma al stock ----------
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

# ---------- Ventas: cada detalle nuevo resta del stock ----------
venta1, _ = Venta.objects.get_or_create(
    fk_cli=clientes["ana"],
    ven_fecha=date(2026, 10, 24),
    defaults={"fk_vdr": vendedor, "ven_metodo_pago": Venta.MetodoPago.TARJETA},
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

venta2, _ = Venta.objects.get_or_create(
    fk_cli=clientes["luis"],
    ven_fecha=date(2026, 10, 25),
    defaults={"fk_vdr": vendedor, "ven_metodo_pago": Venta.MetodoPago.EFECTIVO},
)
DetalleVenta.objects.get_or_create(
    fk_ven=venta2,
    fk_pro=monitor,
    defaults={"dve_cantidad": 1, "dve_precio_unitario": monitor.pro_precio},
)

print("Datos de prueba creados.")
for modelo in (
    Usuario,
    Cliente,
    Vendedor,
    Proveedor,
    Producto,
    Stock,
    Compra,
    DetalleCompra,
    Venta,
    DetalleVenta,
):
    print(f"  {modelo._meta.db_table:<20} {modelo.objects.count()} registros")
