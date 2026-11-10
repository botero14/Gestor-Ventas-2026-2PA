from django import forms

from apps.common.forms import BootstrapFormMixin
from .models import Producto


class ProductoForm(BootstrapFormMixin, forms.ModelForm):
    # ModelForm arma los campos a partir del modelo: tipos, longitudes,
    # obligatoriedad y la validación de pro_codigo único.
    class Meta:
        model = Producto
        fields = ["pro_codigo", "pro_nombre", "pro_descripcion", "pro_precio", "pro_activo"]
        widgets = {
            "pro_descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_pro_codigo(self):
        # clean_<campo> valida o transforma un campo puntual
        return self.cleaned_data["pro_codigo"].strip().upper()

    def clean_pro_precio(self):
        precio = self.cleaned_data["pro_precio"]
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio
