from django import forms
from .models import (
    Calidad, Categoria, Comercial,
    Representante, Cliente,
    Incidencia, Detalle, Accion
)

# =========================
# FORMATOS FECHA
# =========================

DATETIME_INPUT_FORMATS = [
    "%d-%m-%Y %H:%M",
    "%Y-%m-%dT%H:%M",
]

DATETIME_DISPLAY_FORMAT = "%Y-%m-%dT%H:%M"


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
# ACCION
# =========================
class AccionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 SOLO ESTO AHORA
        for f in [
            "email_to",
            "email_cc",
            "email_bcc",
            "email_subject",
            "email_body",
        ]:
            if f in self.fields:
                self.fields[f].required = False

    class Meta:
        model = Accion
        fields = [
            "codigo",
            "descripcion",
            "es_sistema",
            "genera_detalle",
            "detalle_tipo",
            "detalle_descripcion",
            "detalle_notas",
            "enviar_email",
            "email_to",
            "email_cc",
            "email_bcc",
            "email_subject",
            "email_body",
            "email_attachments",
            "email_editable",
        ]
    
    def clean_email_to(self):
        value = self.cleaned_data.get("email_to")

        if not value:
            return value

        # fuerza validación real EmailField
        if "@" not in value:
            raise ValidationError("Email inválido")

        return value

    def clean(self):

        cleaned = super().clean()

        # =========================
        # DETALLE
        # =========================
        if not cleaned.get("genera_detalle"):
            cleaned["detalle_tipo"] = None
            cleaned["detalle_descripcion"] = ""
            cleaned["detalle_notas"] = ""

            # evitar validación obligatoria
            self.fields["detalle_tipo"].required = False

        # =========================
        # EMAIL
        # =========================
        if not cleaned.get("enviar_email"):
            cleaned["email_to"] = ""
            cleaned["email_cc"] = ""
            cleaned["email_bcc"] = ""
            cleaned["email_subject"] = ""
            cleaned["email_body"] = ""

            # booleanos
            cleaned["email_attachments"] = False
            cleaned["email_editable"] = False

            # evitar validación
            self.fields["email_to"].required = False
            self.fields["email_subject"].required = False

        return cleaned

# =========================
# INCIDENCIA
# =========================
class IncidenciaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        readonly_fields = [
            "fecha_apertura",
            "fecha_ultimo",
            "fecha_cierre",
            "fecha_control",

            "usuario_apertura",
            "usuario_actualizacion",
            "usuario_cierre",
            "usuario_control",

            "cerrado",
        ]

        for field_name in readonly_fields:

            if field_name in self.fields:

                self.fields[field_name].disabled = True
                self.fields[field_name].required = False

                

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

    fecha_apertura = forms.DateTimeField(
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_DISPLAY_FORMAT,
            attrs={"type": "datetime-local"}
        )
    )

    fecha_ultimo = forms.DateTimeField(
        required=False,
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_DISPLAY_FORMAT,
            attrs={"type": "datetime-local"}
        )
    )

    fecha_cierre = forms.DateTimeField(
        required=False,
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_DISPLAY_FORMAT,
            attrs={"type": "datetime-local"}
        )
    )

    fecha_control = forms.DateTimeField(
        required=False,
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_DISPLAY_FORMAT,
            attrs={"type": "datetime-local"}
        )
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


# =========================
# DETALLE
# =========================
class DetalleForm(forms.ModelForm):

    fecha = forms.DateTimeField(
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_DISPLAY_FORMAT,
            attrs={"type": "datetime-local"}
        )
    )

    fecha_control = forms.DateTimeField(
        required=False,
        input_formats=DATETIME_INPUT_FORMATS,
        widget=forms.DateTimeInput(
            format=DATETIME_DISPLAY_FORMAT,
            attrs={"type": "datetime-local"}
        )
    )

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