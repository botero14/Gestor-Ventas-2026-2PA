from django.urls import path
from . import views

apps_name = "clientes"

urlpatterns = [path("", views.lista_clientes, name="lista_clientes")]
