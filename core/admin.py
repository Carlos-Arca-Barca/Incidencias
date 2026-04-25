from django.contrib import admin
from .models import *

for model in [
    Accion,
    Incidencia,
    Detalle,
    Calidad,
    Categoria,
    Comercial,
    Representante,
    Cliente,
    Configuracion,
    PerfilUsuario,
]:
    try:
        admin.site.register(model)
        print(f"OK: {model.__name__}")
    except Exception as e:
        print(f"ERROR en {model.__name__}: {e}")