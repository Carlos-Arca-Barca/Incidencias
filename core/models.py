from django.conf import settings
from django.db import models


class Calidad(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    notas = models.TextField(
        blank=True,
        verbose_name="Notas",
    )

    GRID_COLUMNS = [
        {"field": "codigo", "label": "Código"},
        {"field": "descripcion", "label": "Descripción"},
        {"field": "notas", "label": "Notas"},
    ]

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Calidad"
        verbose_name_plural = "Calidades"
        ordering = ["codigo"]


class Categoria(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    notas = models.TextField(
        blank=True,
        verbose_name="Notas",
    )

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["codigo"]


class Comercial(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="Email",
    )
    telefono = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Teléfono",
    )

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Comercial"
        verbose_name_plural = "Comerciales"
        ordering = ["codigo"]


class Representante(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    comercial = models.ForeignKey(
        "Comercial",
        on_delete=models.PROTECT,
        related_name="representantes",
        verbose_name="Comercial",
    )

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Representante"
        verbose_name_plural = "Representantes"
        ordering = ["codigo"]


class Cliente(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    representante = models.ForeignKey(
        "Representante",
        on_delete=models.PROTECT,
        related_name="clientes",
        verbose_name="Representante",
    )

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["codigo"]


class Accion(models.Model):
    codigo = models.CharField(
        verbose_name="Código",
        max_length=10,
        unique=True,
    )
    descripcion = models.CharField(
        verbose_name="Descripción",
        max_length=40,
    )
    es_sistema = models.BooleanField(
        verbose_name="Es sistema",
        default=False,
    )

    genera_detalle = models.BooleanField(
        verbose_name="Genera detalle",
        default=False,
    )
    detalle_tipo = models.CharField(
        verbose_name="Tipo de detalle",
        max_length=10,
        blank=True,
    )
    detalle_descripcion = models.CharField(
        verbose_name="Descripción del detalle",
        max_length=40,
        blank=True,
    )
    detalle_notas = models.TextField(
        verbose_name="Notas del detalle",
        blank=True,
    )

    enviar_email = models.BooleanField(
        verbose_name="Enviar email",
        default=False,
    )
    email_to = models.EmailField(
        verbose_name="Destinatario",
        max_length=254,
        blank=True,
    )
    email_cc = models.TextField(
        verbose_name="CC",
        blank=True,
    )
    email_bcc = models.TextField(
        verbose_name="BCC",
        blank=True,
    )
    email_subject = models.CharField(
        verbose_name="Asunto",
        max_length=254,
        blank=True,
    )
    email_body = models.TextField(
        verbose_name="Cuerpo del email",
        blank=True,
    )
    email_attachments = models.BooleanField(
        verbose_name="Adjuntos email",
        default=False,
    )
    email_editable = models.BooleanField(
        verbose_name="Email editable",
        default=False,
    )

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Acción"
        verbose_name_plural = "Acciones"
        ordering = ["codigo"]


class Incidencia(models.Model):
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )

    cliente = models.ForeignKey(
        "Cliente",
        on_delete=models.PROTECT,
        related_name="incidencias",
        verbose_name="Cliente",
    )
    calidad = models.ForeignKey(
        "Calidad",
        on_delete=models.PROTECT,
        related_name="incidencias",
        verbose_name="Calidad",
    )
    categoria = models.ForeignKey(
        "Categoria",
        on_delete=models.PROTECT,
        related_name="incidencias",
        verbose_name="Categoría",
    )

    notas = models.TextField(
        blank=True,
        verbose_name="Notas",
    )

    fecha_apertura = models.DateTimeField(
        verbose_name="Fecha apertura",
    )
    fecha_ultimo = models.DateTimeField(
        verbose_name="Última actualización",
    )
    fecha_cierre = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha cierre",
    )
    fecha_control = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha control",
    )

    cerrado = models.BooleanField(
        default=False,
        verbose_name="Cerrado",
    )
    control = models.BooleanField(
        default=False,
        verbose_name="Control",
    )

    usuario_apertura = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_abiertas",
        verbose_name="Usuario apertura",
    )
    usuario_actualizacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_actualizadas",
        verbose_name="Usuario última actualización",
    )
    usuario_cierre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_cerradas",
        blank=True,
        null=True,
        verbose_name="Usuario cierre",
    )
    usuario_control = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="incidencias_controladas",
        blank=True,
        null=True,
        verbose_name="Usuario control",
    )

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"
        ordering = ["-fecha_apertura"]
        indexes = [
            models.Index(fields=["cliente"]),
            models.Index(fields=["fecha_apertura"]),
            models.Index(fields=["cerrado"]),
        ]


class Detalle(models.Model):
    incidencia = models.ForeignKey(
        "Incidencia",
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="Incidencia",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    tipo = models.CharField(
        max_length=10,
        verbose_name="Tipo",
    )
    fecha = models.DateTimeField(
        verbose_name="Fecha",
    )
    fecha_control = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha control",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="detalles_creados",
        verbose_name="Usuario",
    )
    usuario_control = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="detalles_controlados",
        blank=True,
        null=True,
        verbose_name="Usuario control",
    )
    adjunto = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adjunto",
    )
    notas = models.TextField(
        blank=True,
        verbose_name="Notas",
    )
    control = models.BooleanField(
        default=False,
        verbose_name="Control",
    )

    def __str__(self):
        return f"{self.incidencia.codigo} - {self.descripcion}"

    class Meta:
        verbose_name = "Detalle"
        verbose_name_plural = "Detalles"
        ordering = ["fecha"]
        indexes = [
            models.Index(fields=["incidencia"]),
            models.Index(fields=["fecha"]),
        ]


class Configuracion(models.Model):
    nombre_empresa = models.CharField(
        max_length=40,
        verbose_name="Nombre empresa",
    )

    dir_general_email = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="Email Dirección General",
    )
    dir_general_apertura = models.BooleanField(
        default=False,
        verbose_name="DG - Apertura",
    )
    dir_general_cierre = models.BooleanField(
        default=False,
        verbose_name="DG - Cierre",
    )
    dir_general_reapertura = models.BooleanField(
        default=False,
        verbose_name="DG - Reapertura",
    )

    dir_comercial_email = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="Email Dirección Comercial",
    )
    dir_comercial_apertura = models.BooleanField(
        default=False,
        verbose_name="DC - Apertura",
    )
    dir_comercial_cierre = models.BooleanField(
        default=False,
        verbose_name="DC - Cierre",
    )
    dir_comercial_reapertura = models.BooleanField(
        default=False,
        verbose_name="DC - Reapertura",
    )

    dpt_calidad_email = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="Email Calidad",
    )
    dpt_calidad_apertura = models.BooleanField(
        default=False,
        verbose_name="Calidad - Apertura",
    )
    dpt_calidad_cierre = models.BooleanField(
        default=False,
        verbose_name="Calidad - Cierre",
    )
    dpt_calidad_reapertura = models.BooleanField(
        default=False,
        verbose_name="Calidad - Reapertura",
    )

    comercial_apertura = models.BooleanField(
        default=False,
        verbose_name="Comercial - Apertura",
    )
    comercial_cierre = models.BooleanField(
        default=False,
        verbose_name="Comercial - Cierre",
    )
    comercial_reapertura = models.BooleanField(
        default=False,
        verbose_name="Comercial - Reapertura",
    )

    otros_email = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name="Otros emails",
    )
    otros_apertura = models.BooleanField(
        default=False,
        verbose_name="Otros - Apertura",
    )
    otros_cierre = models.BooleanField(
        default=False,
        verbose_name="Otros - Cierre",
    )
    otros_reapertura = models.BooleanField(
        default=False,
        verbose_name="Otros - Reapertura",
    )

    tamano_maximo_adjunto = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Tamaño máximo adjunto",
    )
    tamano_maximo_adjuntos = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Tamaño máximo adjuntos",
    )

    cierre_requiere_control = models.BooleanField(
        default=False,
        verbose_name="Cierre requiere control",
    )

    logotipo = models.BinaryField(
        blank=True,
        null=True,
        verbose_name="Logotipo",
    )
    fecha_licencia = models.TextField(
        blank=True,
        verbose_name="Fecha licencia",
    )

    def __str__(self):
        return "Configuración del sistema"
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise Exception("No se puede eliminar Configuración")

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuración"


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="Usuario Django",
    )
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código",
    )
    descripcion = models.CharField(
        max_length=40,
        verbose_name="Descripción",
    )
    sistema = models.BooleanField(
        default=False,
        verbose_name="Usuario de sistema",
    )
    modo = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Modo",
    )
    notas = models.TextField(
        blank=True,
        verbose_name="Notas",
    )
    password_change = models.BooleanField(
        default=False,
        verbose_name="Debe cambiar contraseña",
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"
        ordering = ["codigo"]
