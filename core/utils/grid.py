from django.core.paginator import Paginator


def build_grid(request, qs, columnas, page_size=10):

    # =========================
    # FILTROS DINÁMICOS
    # =========================
    for key, value in request.GET.items():

        if not value:
            continue

        if key in ["page", "orden", "dir"]:
            continue

        try:
            qs = qs.filter(**{f"{key}__icontains": value})
        except Exception:
            continue

    total_registros = qs.count()

    # =========================
    # ORDEN (GENÉRICO)
    # =========================
    orden = request.GET.get("orden")
    dir_ = request.GET.get("dir", "asc")

    if orden:
        orden_db = "-" + orden if dir_ == "desc" else orden
        qs = qs.order_by(orden_db)

    # =========================
    # PAGINACIÓN
    # =========================
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    current = page_obj.number
    total = page_obj.paginator.num_pages

    # =========================
    # PÁGINAS
    # =========================
    if total <= 7:
        pages = list(range(1, total + 1))
    else:
        pages = [1]

        if current <= 4:
            pages += [2, 3, 4, 5, "...", total]

        elif current >= total - 3:
            pages += ["...", total - 4, total - 3, total - 2, total - 1, total]

        else:
            pages += [
                "...",
                current - 2,
                current - 1,
                current,
                current + 1,
                current + 2,
                "...",
                total
            ]

    return {
        "page_obj": page_obj,
        "pages": pages,
        "orden": orden or "",
        "dir": dir_,
        "total_registros": total_registros,
        "columnas": columnas,
    }