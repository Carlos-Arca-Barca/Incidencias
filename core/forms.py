from django import forms
from .models import (
    Calidad, Categoria, Comercial,
    Representante, Cliente,
    Incidencia, Detalle
)

# =========================
# CALIDAD
# =========================
class CalidadForm(forms.ModelForm):
    class Meta:
        model = Calidad
        fields = ["codigo", "descripcion", "notas"]


# =========================
# CATEGORIA
# =========================
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["codigo", "descripcion", "notas"]


# =========================
# COMERCIAL
# =========================
class ComercialForm(forms.ModelForm):
    class Meta:
        model = Comercial
        fields = ["codigo", "descripcion", "email", "telefono"]


# =========================
# REPRESENTANTE
# =========================
class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ["codigo", "descripcion", "comercial"]


# =========================
# CLIENTE
# =========================
class ClienteForm(forms.ModelForm):

    # 👇 SOLO VISUAL (no se guarda en DB)
    comercial_display = forms.CharField(
        required=False,
        label="Comercial",
        widget=forms.TextInput(attrs={
            "readonly": "readonly",
            "class": "form-control",
            "style": "background:#f2f2f2;"
        })
    )

    class Meta:
        model = Cliente
        fields = [
            "codigo",
            "descripcion",
            "representante",
        ]


# =========================
# INCIDENCIA
# =========================
class IncidenciaForm(forms.ModelForm):

    # =========================
    # CAMPOS VIRTUALES UI
    # =========================

    representante_display = forms.CharField(
        required=False,
        label="Representante",
        widget=forms.TextInput(attrs={
            "readonly": "readonly",
            "class": "form-control",
            "style": "background:#f2f2f2;"
        })
    )

    comercial_display = forms.CharField(
        required=False,
        label="Comercial",
        widget=forms.TextInput(attrs={
            "readonly": "readonly",
            "class": "form-control",
            "style": "background:#f2f2f2;"
        })
    )

    class Meta:
        model = Incidencia

        fields = [
            "descripcion",

            "cliente",
            "calidad",
            "categoria",

            # 👇 CAMPOS VISUALES (no modelo)
            "representante_display",
            "comercial_display",

            "notas",

            "fecha_apertura",
            "fecha_ultimo",
            "fecha_cierre",
            "fecha_control",

            "cerrado",
            "control",

            "usuario_apertura",
            "usuario_actualizacion",
            "usuario_cierre",
            "usuario_control",
        ]

        widgets = {
            "fecha_apertura": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_ultimo": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_cierre": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_control": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


# =========================
# DETALLE
# =========================
class DetalleForm(forms.ModelForm):

    class Meta:
        model = Detalle

        fields = [
            "descripcion",
            "tipo",

            "fecha",
            "fecha_control",

            "usuario",
            "usuario_control",

            "adjunto",
            "notas",

            "control",
        ]

        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_control": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }