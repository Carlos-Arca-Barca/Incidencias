from django.shortcuts import render
from .utils.grid import build_grid


def grid_view(request, config=None):

    if config is None:
        raise ValueError("grid_view necesita una configuración")

    model = config.get("model")
    columnas = config.get("columns", [])
    page_size = config.get("page_size", 10)
    template = config.get("template")

    qs = model.objects.all()

    context = build_grid(
        request=request,
        qs=qs,
        columnas=columnas,
        page_size=page_size,
        grid_config=config,
    )

    # =========================
    # FILTROS DINÁMICOS
    # =========================

    filters = config.get("filters", {})

    grid_filters = None

    # =====================================================
    # CASO 1: FILTROS ANTIGUOS (LISTA → AUXILIARES)
    # =====================================================
    if isinstance(filters, list):

        grid_filters = []

        for filtro in filters:

            item = dict(filtro)

            item["value"] = request.GET.get(
                item["field"],
                ""
            )

            grid_filters.append(item)

    # =====================================================
    # CASO 2: FILTROS NUEVOS (DICT → INCIDENCIAS)
    # =====================================================
    else:

        grid_filters = {
            "general": [],
            "usuarios": [],
            "fechas": [],
            "booleanos": [],
        }

        for bloque, lista in filters.items():

            for filtro in lista:

                item = dict(filtro)

                field = item["field"]

                ftype = item.get("type")

                # -------------------------
                # FECHAS (RANGO)
                # -------------------------
                if ftype == "daterange":

                    item["from"] = request.GET.get(
                        f"{field}_from",
                        ""
                    )

                    item["to"] = request.GET.get(
                        f"{field}_to",
                        ""
                    )

                # -------------------------
                # BOOLEANOS
                # -------------------------
                elif ftype == "boolean":

                    item["value"] = request.GET.get(
                        field,
                        ""
                    )

                # -------------------------
                # TEXTO / RELACIONES
                # -------------------------
                else:

                    item["value"] = request.GET.get(
                        field,
                        ""
                    )

                # -------------------------
                # SEGURIDAD BLOQUES
                # -------------------------
                if bloque not in grid_filters:
                    grid_filters[bloque] = []

                grid_filters[bloque].append(item)

    context["grid_filters"] = grid_filters

    return render(request, template, context)