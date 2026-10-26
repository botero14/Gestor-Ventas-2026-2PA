from django.shortcuts import render, HttpResponse


# Create your views here.
def lista_clientes(request):
    return HttpResponse("<h1> Vista de clientes </h1>")
