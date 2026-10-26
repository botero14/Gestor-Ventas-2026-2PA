from django.contrib import admin

from apps.common.admin import CommonAdmin
from apps.ejemplares.models import Ejemplar
from apps.stocks.models import Stock
from .models import Producto


class StockInline(admin.StackedInline):
    model = Stock
    can_delete = False


class EjemplarInline(admin.TabularInline):
    model = Ejemplar
    extra = 1


@admin.register(Producto)
class ProductoAdmin(CommonAdmin):
    list_display = ("pro_codigo", "pro_nombre", "pro_precio", "pro_activo")
    search_fields = ("pro_codigo", "pro_nombre")
    list_filter = ("pro_activo",)
    inlines = [StockInline, EjemplarInline]
