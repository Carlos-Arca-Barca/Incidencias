from django.contrib import messages
from django.utils import timezone

from django.http import JsonResponse

from urllib.parse import parse_qsl, urlencode
from django.shortcuts import render, redirect
from django.urls import reverse
#from django.db.models.deletion import ProtectedError
from .utils.delete import safe_delete
from .utils.get_object import safe_get_object

from .models import Calidad
from .forms import CalidadForm

from .models import Categoria
from .forms import CategoriaForm

from .models import Comercial
from .forms import ComercialForm

from .models import Representante
from .forms import RepresentanteForm

from .models import Cliente
from .forms import ClienteForm

from .models import Incidencia
from .forms import IncidenciaForm



def home(request):
    return render(request, "core/home.html")


def _query_params_from_string(query_string):
    """
    Convierte una querystring tipo 'page=2&orden=codigo&dir=asc&codigo=A'
    en un dict limpio.
    """
    if not query_string:
        return {}

    qs = query_string.lstrip("?").strip()
    if not qs:
        return {}

    params = dict(parse_qsl(qs, keep_blank_values=True))

    params.pop("next", None)
    params.pop("selected", None)

    return params


def _apply_grid_params(qs, params):

    reserved = {
        "page",
        "orden",
        "dir",
        "selected",
        "next",
        "return",
    }

    model_name = qs.model.__name__

    for key, value in params.items():

        if key in reserved or value in ("", None):
            continue

        # =========================
        # INCIDENCIA → codigo visual
        # =========================

        if key == "codigo_visual":

            value = str(value).replace("INC_", "").strip()

            if value.isdigit():
                qs = qs.filter(id=int(value))

            continue

        # =========================
        # BOOLEANOS
        # =========================

        if value in ("si", "no"):

            bool_value = value == "si"

            try:
                qs = qs.filter(**{key: bool_value})
            except Exception:
                pass

            continue

        if value == "ambos":
            continue

        # =========================
        # FECHAS DESDE
        # =========================

        if key.endswith("_desde"):

            field = key.replace("_desde", "")

            try:
                qs = qs.filter(**{f"{field}__date__gte": value})
            except Exception:
                pass

            continue

        # =========================
        # FECHAS HASTA
        # =========================

        if key.endswith("_hasta"):

            field = key.replace("_hasta", "")

            try:
                qs = qs.filter(**{f"{field}__date__lte": value})
            except Exception:
                pass

            continue

        # =========================
        # RELACIONES INCIDENCIA
        # =========================

        if model_name == "Incidencia":

            relation_filters = {

                "cliente":
                    "cliente__descripcion__icontains",

                "representante":
                    "cliente__representante__descripcion__icontains",

                "comercial":
                    "cliente__representante__comercial__descripcion__icontains",

                "calidad":
                    "calidad__descripcion__icontains",

                "categoria":
                    "categoria__descripcion__icontains",

                "usuario_apertura":
                    "usuario_apertura__username__icontains",

                "usuario_actualizacion":
                    "usuario_actualizacion__username__icontains",

                "usuario_cierre":
                    "usuario_cierre__username__icontains",

                "usuario_control":
                    "usuario_control__username__icontains",
            }

            if key in relation_filters:

                try:
                    qs = qs.filter(**{
                        relation_filters[key]: value
                    })

                except Exception:
                    pass

                continue

        # =========================
        # RESTO CAMPOS
        # =========================

        try:

            qs = qs.filter(**{
                f"{key}__icontains": value
            })

        except Exception:

            continue

    # =========================
    # ORDEN
    # =========================

    orden = params.get("orden", "id")

    dir_ = params.get("dir", "asc")

    # ordenar codigo visual por id
    if orden == "codigo_visual":
        orden = "id"

    try:

        qs = qs.order_by(
            f"-{orden}" if dir_ == "desc" else orden
        )

    except Exception:

        pass

    return qs


# =========================
# CALIDAD
# =========================


def calidad_ver(request, id):

    obj = safe_get_object(
        Calidad,
        id,
        request,
        "calidad"
    )

    if not isinstance(obj, Calidad):
        return obj
    
    form = CalidadForm(instance=obj)

    for f in form.fields.values():
        f.disabled = True

    return render(request, "core/calidad_form.html", {
        "form": form,
        "modo": "ver",
        "id": id,
        "next": request.GET.get("next", ""),
    })


def calidad_editar(request, id):

    obj = safe_get_object(
        Calidad,
        id,
        request,
        "calidad"
    )

    if not isinstance(obj, Calidad):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = CalidadForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            base_url = reverse("calidad")
            return redirect(f"{base_url}?{next_url}" if next_url else base_url)
    else:
        form = CalidadForm(instance=obj)

    return render(request, "core/calidad_form.html", {
        "form": form,
        "modo": "editar",
        "id": id,
        "next": next_url,
    })


def calidad_nuevo(request):

    next_url = request.POST.get("next") or request.GET.get("next", "")
    next_params = _query_params_from_string(request.POST.get("next") or request.GET.get("next") or "")

    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    # preservar contexto lookup aunque venga fuera de next
    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    if request.method == "POST":

        form = CalidadForm(request.POST)

        if form.is_valid():

            obj = form.save()

            # =========================
            # GRID REAL (FUENTE ÚNICA)
            # =========================
            from .utils.grid import build_grid

            grid_data = build_grid(
                request=request,
                qs=Calidad.objects.all(),
                columnas=[],
                page_size=10,
                grid_config=None
            )

            qs = grid_data["final_queryset"]

            # posición real dentro del grid
            ids = list(qs.values_list("id", flat=True))

            try:
                pos = ids.index(obj.id) + 1
                page_size = 10
                page = ((pos - 1) // page_size) + 1
            except ValueError:
                page = 1

            final_params = dict(next_params)
            final_params["page"] = str(page)
            final_params["selected"] = str(obj.id)

            url = reverse("calidad")
            query = urlencode(final_params)

            return redirect(f"{url}?{query}")

    else:

        form = CalidadForm()

    return render(request, "core/calidad_form.html", {
        "form": form,
        "modo": "nuevo",
        "next": next_url,
    })


def calidad_eliminar(request, id):

    obj = safe_get_object(
        Calidad,
        id,
        request,
        "calidad"
    )

    if not isinstance(obj, Calidad):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":

        _, _ = safe_delete(request, obj, None)

        base_url = reverse("calidad")
        return redirect(f"{base_url}?{next_url}" if next_url else base_url)

    return render(request, "core/calidad_confirm_delete.html", {
        "obj": obj,
        "next": next_url,
    })


# =========================
# CATEGORIA
# =========================

def categoria_ver(request, id):

    obj = safe_get_object(
        Categoria,
        id,
        request,
        "categorias"
    )

    if not isinstance(obj, Categoria):
        return obj
    
    form = CategoriaForm(instance=obj)

    for f in form.fields.values():
        f.disabled = True

    return render(request, "core/categoria_form.html", {
        "form": form,
        "modo": "ver",
        "id": id,
        "next": request.GET.get("next", ""),
    })


def categoria_editar(request, id):

    obj = safe_get_object(
        Categoria,
        id,
        request,
        "categorias"
    )

    if not isinstance(obj, Categoria):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            base_url = reverse("categorias")
            return redirect(f"{base_url}?{next_url}" if next_url else base_url)

    else:
        form = CategoriaForm(instance=obj)

    return render(request, "core/categoria_form.html", {
        "form": form,
        "modo": "editar",
        "id": id,
        "next": next_url,
    })


def categoria_nuevo(request):

    next_url = request.POST.get("next") or request.GET.get("next", "")
    next_params = _query_params_from_string(request.POST.get("next") or request.GET.get("next") or "")

    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    # preservar contexto lookup (CLAVE para que no se pierda el SELECT)
    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    if request.method == "POST":

        form = CategoriaForm(request.POST)

        if form.is_valid():

            obj = form.save()

            # =========================
            # GRID REAL (FUENTE ÚNICA)
            # =========================
            from .utils.grid import build_grid

            grid_data = build_grid(
                request=request,
                qs=Categoria.objects.all(),
                columnas=[],
                page_size=10,
                grid_config=None
            )

            qs = grid_data["final_queryset"]

            ids = list(qs.values_list("id", flat=True))

            try:
                pos = ids.index(obj.id) + 1
                page_size = 10
                page = ((pos - 1) // page_size) + 1
            except ValueError:
                page = 1

            final_params = dict(next_params)
            final_params["page"] = str(page)
            final_params["selected"] = str(obj.id)

            url = reverse("categorias")
            query = urlencode(final_params)

            return redirect(f"{url}?{query}")

    else:

        form = CategoriaForm()

    return render(request, "core/categoria_form.html", {
        "form": form,
        "modo": "nuevo",
        "next": next_url,
    })


def categoria_eliminar(request, id):

    obj = safe_get_object(
        Categoria,
        id,
        request,
        "categorias"
    )

    if not isinstance(obj, Categoria):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":

        _, _ = safe_delete(request, obj, None)

        base_url = reverse("categorias")
        return redirect(f"{base_url}?{next_url}" if next_url else base_url)

    return render(request, "core/categoria_confirm_delete.html", {
        "obj": obj,
        "next": next_url,
    })

# =========================
# COMERCIAL
# =========================


def comercial_ver(request, id):

    obj = safe_get_object(
        Comercial,
        id,
        request,
        "comerciales"
    )

    if not isinstance(obj, Comercial):
        return obj
    
    form = ComercialForm(instance=obj)

    for f in form.fields.values():
        f.disabled = True

    return render(request, "core/comercial_form.html", {
        "form": form,
        "modo": "ver",
        "id": id,
        "next": request.GET.get("next", ""),
    })


def comercial_editar(request, id):

    obj = safe_get_object(
        Comercial,
        id,
        request,
        "comerciales"
    )

    if not isinstance(obj, Comercial):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = ComercialForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            base_url = reverse("comerciales")
            return redirect(f"{base_url}?{next_url}" if next_url else base_url)
    else:
        form = ComercialForm(instance=obj)

    return render(request, "core/comercial_form.html", {
        "form": form,
        "modo": "editar",
        "id": id,
        "next": next_url,
    })


def comercial_nuevo(request):

    next_url = request.POST.get("next") or request.GET.get("next", "")
    next_params = _query_params_from_string(request.POST.get("next") or request.GET.get("next") or "")

    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    # preservar contexto lookup aunque venga fuera de next
    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    if request.method == "POST":

        form = ComercialForm(request.POST)

        if form.is_valid():

            obj = form.save()

            # =========================
            # GRID REAL (FUENTE ÚNICA)
            # =========================
            from .utils.grid import build_grid

            grid_data = build_grid(
                request=request,
                qs=Comercial.objects.all(),
                columnas=[],
                page_size=10,
                grid_config=None
            )

            qs = grid_data["final_queryset"]

            ids = list(qs.values_list("id", flat=True))

            try:
                pos = ids.index(obj.id) + 1
                page_size = 10
                page = ((pos - 1) // page_size) + 1
            except ValueError:
                page = 1

            final_params = dict(next_params)
            final_params["page"] = str(page)
            final_params["selected"] = str(obj.id)

            url = reverse("comerciales")
            query = urlencode(final_params)

            return redirect(f"{url}?{query}")

    else:

        form = ComercialForm()

    return render(request, "core/comercial_form.html", {
        "form": form,
        "modo": "nuevo",
        "next": next_url,
    })


def comercial_eliminar(request, id):

    obj = safe_get_object(
        Comercial,
        id,
        request,
        "comerciales"
    )

    if not isinstance(obj, Comercial):
        return obj

    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        _, _ = safe_delete(request, obj, None)

        base_url = reverse("comerciales")
        return redirect(f"{base_url}?{next_url}" if next_url else base_url)

    return render(request, "core/comercial_confirm_delete.html", {
        "obj": obj,
        "next": next_url,
    })

# =========================
# REPRESENTANTE
# =========================


def representante_ver(request, id):

    obj = safe_get_object(
        Representante,
        id,
        request,
        "representantes"
    )

    if not isinstance(obj, Representante):
        return obj
    
    form = RepresentanteForm(instance=obj)

    for f in form.fields.values():
        f.disabled = True

    return render(request, "core/representante_form.html", {
        "form": form,
        "modo": "ver",
        "id": id,
        "next": request.GET.get("next", ""),
    })


def representante_editar(request, id):

    obj = safe_get_object(
        Representante,
        id,
        request,
        "representantes"
    )

    if not isinstance(obj, Representante):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = RepresentanteForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()

            base_url = reverse("representantes")
            return redirect(f"{base_url}?{next_url}" if next_url else base_url)
    else:
        form = RepresentanteForm(instance=obj)

    return render(request, "core/representante_form.html", {
        "form": form,
        "modo": "editar",
        "id": id,
        "next": next_url,
    })



def representante_nuevo(request):

    next_url = request.POST.get("next") or request.GET.get("next", "")
    next_params = _query_params_from_string(request.POST.get("next") or request.GET.get("next") or "")

    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    # preservar contexto lookup aunque venga fuera de next
    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    if request.method == "POST":

        form = RepresentanteForm(request.POST)

        if form.is_valid():

            obj = form.save()

            # =========================
            # GRID REAL (FUENTE ÚNICA)
            # =========================
            from .utils.grid import build_grid

            grid_data = build_grid(
                request=request,
                qs=Representante.objects.all(),
                columnas=[],
                page_size=10,
                grid_config=None
            )

            qs = grid_data["final_queryset"]

            ids = list(qs.values_list("id", flat=True))

            try:
                pos = ids.index(obj.id) + 1
                page_size = 10
                page = ((pos - 1) // page_size) + 1
            except ValueError:
                page = 1

            final_params = dict(next_params)
            final_params["page"] = str(page)
            final_params["selected"] = str(obj.id)

            url = reverse("representantes")
            query = urlencode(final_params)

            return redirect(f"{url}?{query}")

    else:

        form = RepresentanteForm()

    return render(request, "core/representante_form.html", {
        "form": form,
        "modo": "nuevo",
        "next": next_url,
    })

def representante_eliminar(request, id):

    obj = safe_get_object(
        Representante,
        id,
        request,
        "representantes"
    )

    if not isinstance(obj, Representante):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":

        _, _ = safe_delete(request, obj, None)

        base_url = reverse("representantes")
        return redirect(f"{base_url}?{next_url}" if next_url else base_url)

    return render(request, "core/representante_confirm_delete.html", {
        "obj": obj,
        "next": next_url,
    })


# =========================
# CLIENTE
# =========================

def cliente_ver(request, id):

    obj = safe_get_object(
        Cliente,
        id,
        request,
        "clientes"
    )

    if not isinstance(obj, Cliente):
        return obj
    
    form = ClienteForm(instance=obj)

    for f in form.fields.values():
        f.disabled = True

    return render(request, "core/cliente_form.html", {
        "form": form,
        "modo": "ver",
        "id": id,
        "next": request.GET.get("next", ""),
    })


def cliente_editar(request, id):

    obj = safe_get_object(
        Cliente,
        id,
        request,
        "clientes"
    )

    if not isinstance(obj, Cliente):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()

            base_url = reverse("clientes")
            return redirect(f"{base_url}?{next_url}" if next_url else base_url)

    else:
        form = ClienteForm(instance=obj)

    return render(request, "core/cliente_form.html", {
        "form": form,
        "modo": "editar",
        "id": id,
        "next": next_url,
    })


def cliente_nuevo(request):

    next_url = request.POST.get("next") or request.GET.get("next", "")
    next_params = _query_params_from_string(request.POST.get("next") or request.GET.get("next") or "")

    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    # preservar contexto lookup aunque venga fuera de next
    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    if request.method == "POST":

        form = ClienteForm(request.POST)

        if form.is_valid():

            obj = form.save()

            # =========================
            # GRID REAL (FUENTE ÚNICA)
            # =========================
            from .utils.grid import build_grid

            grid_data = build_grid(
                request=request,
                qs=Cliente.objects.all(),
                columnas=[],
                page_size=10,
                grid_config=None
            )

            qs = grid_data["final_queryset"]

            ids = list(qs.values_list("id", flat=True))

            try:
                pos = ids.index(obj.id) + 1
                page_size = 10
                page = ((pos - 1) // page_size) + 1
            except ValueError:
                page = 1

            final_params = dict(next_params)
            final_params["page"] = str(page)
            final_params["selected"] = str(obj.id)

            url = reverse("clientes")
            query = urlencode(final_params)

            return redirect(f"{url}?{query}")

    else:

        form = ClienteForm()

    return render(request, "core/cliente_form.html", {
        "form": form,
        "modo": "nuevo",
        "next": next_url,
    })


def cliente_eliminar(request, id):

    obj = safe_get_object(
        Cliente,
        id,
        request,
        "clientes"
    )

    if not isinstance(obj, Cliente):
        return obj
    
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":

        _, _ = safe_delete(request, obj, None)

        base_url = reverse("clientes")

        return redirect(
            f"{base_url}?{next_url}"
            if next_url else base_url
        )

    return render(request, "core/cliente_confirm_delete.html", {
        "obj": obj,
        "next": next_url,
    })



# =========================
# INCIDENCIA
# =========================

def incidencia_ver(request, id):

    obj = safe_get_object(
        Incidencia,
        id,
        request,
        "incidencias"
    )

    if not isinstance(obj, Incidencia):
        return obj

    form = IncidenciaForm(instance=obj)

    for f in form.fields.values():
        f.disabled = True

    return render(request, "core/incidencia_form.html", {

        "form": form,
        "modo": "ver",
        "id": id,
        "next": request.GET.get("next", ""),
        "incidencia": obj,
    })


def incidencia_editar(request, id):

    obj = safe_get_object(
        Incidencia,
        id,
        request,
        "incidencias"
    )

    if not isinstance(obj, Incidencia):
        return obj

    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":

        form = IncidenciaForm(
            request.POST,
            instance=obj
        )

        if form.is_valid():

            incidencia = form.save(commit=False)

            incidencia.fecha_ultimo = timezone.now()
            incidencia.usuario_actualizacion = request.user

            if incidencia.cerrado and not incidencia.fecha_cierre:
                incidencia.fecha_cierre = timezone.now()

            if incidencia.cerrado and not incidencia.usuario_cierre:
                incidencia.usuario_cierre = request.user

            incidencia.save()

            base_url = reverse("incidencias")

            return redirect(
                f"{base_url}?{next_url}"
                if next_url else base_url
            )

    else:

        form = IncidenciaForm(instance=obj)

    return render(request, "core/incidencia_form.html", {

        "form": form,
        "modo": "editar",
        "id": id,
        "next": next_url,
        "incidencia": obj,
    })


def incidencia_nuevo(request):

    next_url = request.POST.get("next") or request.GET.get("next", "")
    next_params = _query_params_from_string(request.POST.get("next") or request.GET.get("next") or "")

    for key in ("select", "target", "return"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            next_params[key] = value

    if request.method == "POST":

        form = IncidenciaForm(request.POST)

        if form.is_valid():

            incidencia = form.save(commit=False)

            now = timezone.now()

            incidencia.fecha_apertura = now
            incidencia.fecha_ultimo = now

            incidencia.usuario_apertura = request.user
            incidencia.usuario_actualizacion = request.user

            incidencia.save()

            # 🔴 FIX 1: queryset con orden estable (CRÍTICO)
            base_qs = Incidencia.objects.all().order_by("id")

            qs = _apply_grid_params(base_qs, next_params)

            ids = list(qs.values_list("id", flat=True))

            try:
                pos = ids.index(incidencia.id) + 1
                page_size = 10
                page = ((pos - 1) // page_size) + 1
            except ValueError:
                # 🔴 FIX 2: fallback correcto
                page = 1

            final_params = dict(next_params)

            final_params["page"] = str(page)
            final_params["selected"] = str(incidencia.id)

            url = reverse("incidencias")
            query = urlencode(final_params)

            return redirect(f"{url}?{query}")

    else:

        initial = {

            "fecha_apertura": timezone.now(),
            "fecha_ultimo": timezone.now(),

            "usuario_apertura": request.user,
            "usuario_actualizacion": request.user,
        }

        form = IncidenciaForm(initial=initial)

    return render(request, "core/incidencia_form.html", {

        "form": form,
        "modo": "nuevo",
        "next": next_url,
    })

def incidencia_eliminar(request, id):

    obj = safe_get_object(
        Incidencia,
        id,
        request,
        "incidencias"
    )

    if not isinstance(obj, Incidencia):
        return obj

    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":

        _, _ = safe_delete(request, obj, None)

        base_url = reverse("incidencias")

        return redirect(
            f"{base_url}?{next_url}"
            if next_url else base_url
        )

    return render(request, "core/incidencia_confirm_delete.html", {

        "obj": obj,
        "next": next_url,
    })









def ajax_representante_comercial(request, id):

    try:
        rep = Representante.objects.select_related("comercial").get(id=id)

        if rep.comercial:
            return JsonResponse({
                "id": rep.comercial.id,
                "codigo": rep.comercial.codigo,
                "descripcion": rep.comercial.descripcion,
            })

        return JsonResponse({
            "id": None,
            "codigo": "",
            "descripcion": ""
        })

    except Representante.DoesNotExist:
        return JsonResponse({
            "error": "Representante no encontrado"
        }, status=404)





def ajax_cliente_info(request, id):

    try:
        cliente = (
            Cliente.objects
            .select_related("representante__comercial")
            .get(id=id)
        )

        representante = cliente.representante
        comercial = representante.comercial if representante else None

        return JsonResponse({
            "representante_id": representante.id if representante else "",
            "representante": representante.descripcion if representante else "",
            "comercial": comercial.descripcion if comercial else "",
        })

    except Cliente.DoesNotExist:
        return JsonResponse({
            "error": "Cliente no encontrado"
        }, status=404)

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)