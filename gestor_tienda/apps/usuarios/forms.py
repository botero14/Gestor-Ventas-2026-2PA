from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction

from apps.clientes.models import Cliente
from apps.common.forms import BootstrapFormMixin
from .models import Usuario


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """El formulario de login de Django, solo con estilos de Bootstrap."""


class RegistroClienteForm(BootstrapFormMixin, UserCreationForm):
    """
    Un solo formulario que llena dos tablas:
    tbl_usuario (datos de acceso) y tbl_cliente (perfil).
    """

    # Campos extra que no son de Usuario sino de Cliente
    cli_documento = forms.CharField(label="Documento", max_length=15)
    cli_telefono = forms.CharField(label="Teléfono", max_length=20, required=False)

    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in ("first_name", "last_name", "email"):
            self.fields[nombre].required = True

    def clean_cli_documento(self):
        documento = self.cleaned_data["cli_documento"]
        if Cliente.objects.filter(cli_documento=documento).exists():
            raise forms.ValidationError("Ya existe un cliente con ese documento.")
        return documento

    @transaction.atomic  # si falla el perfil, tampoco se guarda el usuario
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.usu_rol = Usuario.Rol.CLIENTE
        usuario.save()
        Cliente.objects.create(
            fk_usu=usuario,
            cli_documento=self.cleaned_data["cli_documento"],
            cli_telefono=self.cleaned_data["cli_telefono"],
        )
        return usuario
