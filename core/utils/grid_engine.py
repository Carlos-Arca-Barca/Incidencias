from django.shortcuts import render
from django.core.paginator import Paginator
from .grid import apply_grid_state, get_grid_state


def grid_view(request, config):
    """
    Motor único de grids reutilizable
    """

    model = config["model"]
    qs = model.objects.all()

    # filtros + orden
    qs = apply_grid_state(request, qs)

    # paginación
    paginator = Paginator(qs, config.get("page_size", 10))
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, config["template"], {
        "page_obj": page_obj,
        "columnas": config["columns"],
        "pages": build_pages(page_obj),
        "state": get_grid_state(request),
        "grid_urls": config.get("actions", {}),
        "total_registros": qs.count(),
    })


def build_pages(page_obj):
    total = page_obj.paginator.num_pages
    current = page_obj.number

    if total <= 7:
        return list(range(1, total + 1))

    pages = []

    # siempre primero
    pages.append(1)

    # ventana central fija
    start = current - 2
    end = current + 2

    if start < 2:
        start = 2
        end = 6

    if end > total - 1:
        start = total - 5
        end = total - 1

    for i in range(start, end + 1):
        pages.append(i)

    # siempre último
    pages.append(total)

    return pages