from django import forms


class BootstrapFormMixin:
    """
    Pone a cada campo la clase CSS de Bootstrap que le corresponde,
    así las plantillas no tienen que hacerlo campo por campo.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"
            else:
                widget.attrs["class"] = "form-control"
