from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import FieldDoesNotExist


# =========================
# RESERVADOS
# =========================

RESERVED_KEYS = {
    "page",
    "orden",
    "dir",
    "selected",
    "next",
    "select",
    "target",
    "return",
}

# =========================
# CAMPOS CALCULADOS
# =========================

CALCULATED_FILTERS = {

    "Cliente": {

        "representante": [
            "representante__codigo",
            "representante__descripcion",
        ],

        "comercial": [
            "representante__comercial__codigo",
            "representante__comercial__descripcion",
        ],
    },

    "Representante": {

        "comercial": [
            "comercial__codigo",
            "comercial__descripcion",
        ],
    },

    "Incidencia": {

        "representante": [
            "cliente__representante__codigo",
            "cliente__representante__descripcion",
        ],

        "comercial": [
            "cliente__representante__comercial__codigo",
            "cliente__representante__comercial__descripcion",
        ],
    },
}


# =========================
# CAMPOS DISPLAY
# =========================

CALCULATED_DISPLAYS = {

    "Cliente": {

        "representante":
            "representante__descripcion",

        "comercial":
            "representante__comercial__descripcion",
    },

    "Representante": {

        "comercial":
            "comercial__descripcion",
    },

    "Incidencia": {

        "representante":
            "cliente__representante__descripcion",

        "comercial":
            "cliente__representante__comercial__descripcion",

        # =========================
        # 🔥 AÑADIDO (FIX INCIDENCIA)
        # =========================
        "calidad": "calidad__descripcion",
        "categoria": "categoria__descripcion",
    },
}


# =========================
# LOOKUP PARAMS
# =========================

def preserve_lookup_params(request):
    return {
        "select": request.GET.get("select"),
        "target": request.GET.get("target"),
        "return": request.GET.get("return"),
    }


# =========================
# GRID STATE
# =========================

def get_grid_state(request):

    state = {}

    for key, value in request.GET.items():
        if key in RESERVED_KEYS:
            continue
        if value:
            state[key] = value

    state["orden"] = request.GET.get("orden", "codigo")
    state["dir"] = request.GET.get("dir", "asc")
    state["page"] = request.GET.get("page", "1")
    state["selected"] = request.GET.get("selected", "")

    return state


# =========================
# HELPERS
# =========================

def _is_incidencia_queryset(qs):
    try:
        return qs.model.__name__ == "Incidencia"
    except Exception:
        return False


def _filter_user(qs, field_name, value):
    return qs.filter(
        Q(**{f"{field_name}__username__icontains": value}) |
        Q(**{f"{field_name}__first_name__icontains": value}) |
        Q(**{f"{field_name}__last_name__icontains": value})
    )

def resolve_display_field(model_name, field_name):

    displays = CALCULATED_DISPLAYS.get(
        model_name,
        {}
    )

    return displays.get(field_name, field_name)


# =========================
# CAMPOS VIRTUALES
# =========================

VIRTUAL_FIELD_FILTERS = {

    "Cliente": {

        "representante": [
            "representante__codigo",
            "representante__descripcion",
        ],

        "comercial": [
            "representante__comercial__codigo",
            "representante__comercial__descripcion",
        ],
    },

    "Representante": {

        "comercial": [
            "comercial__codigo",
            "comercial__descripcion",
        ],
    },

    "Incidencia": {

        "representante": [
            "cliente__representante__codigo",
            "cliente__representante__descripcion",
        ],

        "comercial": [
            "cliente__representante__comercial__codigo",
            "cliente__representante__comercial__descripcion",
        ],
    },
}


# =========================
# FILTROS
# =========================

def apply_filters(request, qs):

    for key, value in request.GET.items():

        if not value or key in RESERVED_KEYS:
            continue

        # =========================
        # NORMALIZACIÓN FECHAS
        # =========================
        # convertimos todo a formato estándar interno
        if key.endswith("_from"):
            key = key.replace("_from", "_desde")

        if key.endswith("_to"):
            key = key.replace("_to", "_hasta")

        # =========================
        # FECHAS
        # =========================
        if key.endswith("_desde"):
            field = key.replace("_desde", "")
            qs = qs.filter(**{f"{field}__gte": value})
            continue

        if key.endswith("_hasta"):
            field = key.replace("_hasta", "")
            qs = qs.filter(**{f"{field}__lte": value})
            continue

        # =========================
        # BOOLEANOS
        # =========================
        try:
            field = qs.model._meta.get_field(key)

            if field.get_internal_type() == "BooleanField":
                if value == "si":
                    qs = qs.filter(**{key: True})
                elif value == "no":
                    qs = qs.filter(**{key: False})
                continue

        except Exception:
            pass

        # =========================
        # INCIDENCIA CODIGO VISUAL
        # =========================
        if _is_incidencia_queryset(qs) and key == "codigo_visual":

            numero = value.upper().replace("INC_", "").lstrip("0")

            if numero.isdigit():
                qs = qs.filter(id=int(numero))

            continue

        # =========================
        # CAMPOS CALCULADOS
        # =========================
        model_name = qs.model.__name__

        calculated = CALCULATED_FILTERS.get(model_name, {})

        if key in calculated:

            q = Q()

            for lookup in calculated[key]:
                q |= Q(**{f"{lookup}__icontains": value})

            qs = qs.filter(q)
            continue

        # =========================
        # USUARIOS
        # =========================
        if key.startswith("usuario_"):
            qs = _filter_user(qs, key, value)
            continue

        # =========================
        # FK GENERALES SEGURAS
        # =========================
        try:
            field = qs.model._meta.get_field(key)
        except FieldDoesNotExist:
            continue

        if field.is_relation:

            related = field.related_model
            q = Q()

            if hasattr(related, "codigo"):
                q |= Q(**{f"{key}__codigo__icontains": value})

            if hasattr(related, "descripcion"):
                q |= Q(**{f"{key}__descripcion__icontains": value})

            if q:
                qs = qs.filter(q)

            continue

        # =========================
        # TEXTO NORMAL
        # =========================
        qs = qs.filter(**{f"{key}__icontains": value})

    return qs


# =========================
# ORDEN
# =========================

def apply_order(request, qs):

    orden = request.GET.get("orden")
    dir_ = request.GET.get("dir", "asc")

    if orden:
        try:
            qs = qs.order_by(
                f"-{orden}" if dir_ == "desc" else orden
            )
        except Exception:
            pass

    return qs


# =========================
# PAGINACIÓN
# =========================

def paginate(request, qs, page_size):

    paginator = Paginator(qs, page_size)

    return paginator.get_page(
        request.GET.get("page", 1)
    )


# =========================
# URLS GRID
# =========================

def build_grid_urls(grid_config):

    actions = grid_config.get("actions", {})

    return {
        "ver": reverse(actions["ver"], args=[0]).replace("/0/", "/__ID__/"),
        "editar": reverse(actions["editar"], args=[0]).replace("/0/", "/__ID__/"),
        "eliminar": reverse(actions["eliminar"], args=[0]).replace("/0/", "/__ID__/"),
        "nuevo": reverse(actions["nuevo"]),
    }


def get_position_in_grid(qs, obj_id):
    """
    Devuelve la posición real del objeto dentro del queryset ya filtrado y ordenado
    EXACTAMENTE igual que el grid.
    """

    ids = list(qs.values_list("id", flat=True))

    try:
        pos = ids.index(obj_id) + 1
        return pos
    except ValueError:
        return None
    


# =========================
# GRID BUILDER
# =========================

def build_grid(request, qs, columnas, page_size=10, grid_config=None):

    qs = apply_filters(request, qs)
    qs = apply_order(request, qs)

    final_queryset = qs

    if request.GET.get("select") == "1":
        final_queryset = final_queryset
        final_queryset._lookup_mode = True

    total_registros = qs.count()

    page_obj = paginate(request, qs, page_size)

    lookup = preserve_lookup_params(request)

    current = page_obj.number
    total = page_obj.paginator.num_pages

    from urllib.parse import urlencode

    base_params = request.GET.copy()
    base_params.pop("page", None)

    base_query = urlencode(base_params)

    # =========================
    # PAGINACIÓN
    # =========================

    if total <= 10:
        pages = list(range(1, total + 1))
    else:
        if current <= 5:
            pages = [1, 2, 3, 4, 5, 6, 7, "...", total - 1, total]
        elif current >= total - 4:
            pages = [1, 2, "...",
                     total - 6, total - 5, total - 4,
                     total - 3, total - 2, total - 1, total]
        else:
            pages = [1, "...",
                     current - 2, current - 1, current,
                     current + 1, current + 2,
                     "...", total - 1, total]

    context = {
        "page_obj": page_obj,
        "pages": pages,
        "orden": request.GET.get("orden", "codigo"),
        "dir": request.GET.get("dir", "asc"),
        "total_registros": total_registros,
        "columnas": columnas,
        "state": get_grid_state(request),
        "lookup": lookup,
        "base_query": base_query,
        "final_queryset": final_queryset,
        "lookup_select": request.GET.get("select") == "1",
    }

    if grid_config:
        context["grid_config"] = grid_config
        context["grid_urls"] = build_grid_urls(grid_config)

    return context