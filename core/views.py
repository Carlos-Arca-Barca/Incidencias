
from django.shortcuts import render
from .models import Calidad
from django.core.paginator import Paginator


def home(request):
    return render(request, "core/home.html")


def calidad_list(request):
    return render(request, "core/calidad_list.html")


def calidad_grid(request):

    codigo = request.GET.get("codigo", "")
    descripcion = request.GET.get("descripcion", "")
    notas = request.GET.get("notas", "")

    orden = request.GET.get("orden", "codigo")
    dir_ = request.GET.get("dir", "asc")
    page = request.GET.get("page", 1)

    qs = Calidad.objects.all()

    if codigo:
        qs = qs.filter(codigo__icontains=codigo)

    if descripcion:
        qs = qs.filter(descripcion__icontains=descripcion)

    if notas:
        qs = qs.filter(notas__icontains=notas)

    if dir_ == "desc":
        orden = "-" + orden

    qs = qs.order_by(orden)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    return render(request, "core/calidad_grid.html", {
        "calidades": page_obj,
        "orden": request.GET.get("orden", "codigo"),
        "dir": dir_,
    })