"""
Middleware de control de acceso por rol.

Un middleware es una capa que envuelve TODAS las peticiones. Django lo
ejecuta en el orden de settings.MIDDLEWARE al entrar la petición y en
orden inverso al salir la respuesta:

    petición -> Security -> Session -> ... -> Auth -> RolMiddleware -> vista
    respuesta <- Security <- Session <- ... <- Auth <- RolMiddleware <- vista

Por eso RolMiddleware va DESPUÉS de AuthenticationMiddleware: necesita que
request.user ya exista.
"""

from django.shortcuts import redirect, render
from django.urls import reverse

# Rutas que se pueden visitar sin iniciar sesión.
# Se identifican por "namespace:nombre", igual que en {% url %}.
RUTAS_PUBLICAS = {
    "usuarios:login",
    "usuarios:registro",
}

# Rutas restringidas y los roles que pueden entrar a cada una.
# La que no aparezca aquí queda abierta para cualquier usuario con sesión.
RUTAS_POR_ROL = {
    "productos:crear": {"ADMIN", "VENDEDOR"},
    "productos:editar": {"ADMIN"},
    "productos:eliminar": {"ADMIN"},
    "clientes:lista": {"ADMIN", "VENDEDOR"},
}


class RolMiddleware:
    def __init__(self, get_response):
        # Se ejecuta una sola vez, cuando arranca el servidor.
        # get_response es el siguiente eslabón de la cadena (otro middleware o la vista).
        self.get_response = get_response

    def __call__(self, request):
        # Se ejecuta en cada petición. Aquí podría ir código "antes de la vista"...
        response = self.get_response(request)
        # ...y aquí código "después de la vista", sobre la respuesta.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Django lo llama justo antes de ejecutar la vista, cuando ya sabe
        qué URL se pidió. Si devuelve None la petición sigue su camino;
        si devuelve una respuesta, la vista nunca se ejecuta.
        """
        match = request.resolver_match
        ruta = match.view_name  # por ejemplo "productos:editar"

        # El admin de Django tiene su propio login, no lo tocamos
        if match.namespace == "admin" or ruta in RUTAS_PUBLICAS:
            return None

        # 1. Sin sesión iniciada: al login, recordando a dónde quería ir
        if not request.user.is_authenticated:
            return redirect(f"{reverse('usuarios:login')}?next={request.path}")

        # 2. Ruta restringida y el rol del usuario no está autorizado: 403
        roles_permitidos = RUTAS_POR_ROL.get(ruta)
        if roles_permitidos and request.user.usu_rol not in roles_permitidos:
            return render(request, "errores/403.html", status=403)

        return None
