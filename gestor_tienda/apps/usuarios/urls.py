from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("ingresar/", views.IngresarView.as_view(), name="login"),
    path("registro/", views.registro, name="registro"),
    # Desde Django 5 el logout solo acepta POST (ver formulario en el navbar)
    path("salir/", LogoutView.as_view(), name="logout"),
]
