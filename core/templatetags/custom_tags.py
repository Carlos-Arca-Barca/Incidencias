from django import template
from core.utils.grid import resolve_display_field

register = template.Library()


@register.filter
def get_field(obj, field_name):

    try:
        model_name = obj.__class__.__name__

        real_field = resolve_display_field(model_name, field_name)

        value = obj

        for attr in real_field.split("__"):
            value = getattr(value, attr)

            if value is None:
                return ""

        # =========================
        # LOOKUP MODE (CORRECTO)
        # =========================
        lookup_mode = getattr(obj, "_lookup_mode", False)

        if hasattr(obj, "_force_lookup_mode"):
            lookup_mode = True

        # =========================
        # FK DISPLAY LOGIC
        # =========================
        if hasattr(value, "descripcion"):

            # FIX ESPECÍFICO INCIDENCIA
            if model_name == "Incidencia":
                return value.descripcion

            # LOOKUP MODE
            if lookup_mode:
                return value.descripcion

            return f"{value.codigo} - {value.descripcion}"

        # =========================
        # BOOLEAN FORMAT GLOBAL
        # =========================
        if isinstance(value, bool):
            return "Sí" if value else "No"

        return value

    except Exception:
        return ""


@register.filter
def get_query(request, key):
    try:
        return request.GET.get(key, "")
    except Exception:
        return ""


@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""