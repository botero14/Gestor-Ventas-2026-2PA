from django.contrib import admin
from django.urls import include, path

from apps.common.views import inicio

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("usuarios/", include("apps.usuarios.urls")),
    path("productos/", include("apps.productos.urls")),
    path("clientes/", include("apps.clientes.urls")),
]
