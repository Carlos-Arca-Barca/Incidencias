from django import forms
from .models import Calidad


class CalidadForm(forms.ModelForm):
    class Meta:
        model = Calidad
        fields = ["codigo", "descripcion", "notas"]

        