from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistroClienteForm


class IngresarView(LoginView):
    # LoginView ya resuelve autenticar, crear la sesión y redirigir;
    # solo le indicamos qué plantilla y qué formulario usar
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


def registro(request):
    """Registro público: crea el usuario con rol CLIENTE y su perfil."""
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # entra de una vez, sin volver al login
            messages.success(request, "Cuenta creada. Bienvenido a la tienda.")
            return redirect("inicio")
    else:
        form = RegistroClienteForm()

    return render(request, "usuarios/registro.html", {"form": form})
