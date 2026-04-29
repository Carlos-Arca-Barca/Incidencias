from django.shortcuts import render
from .models import Calidad
from django.core.paginator import Paginator
from .utils.grid import build_grid


def home(request):
    return render(request, "core/home.html")


def calidad(request):

    qs = Calidad.objects.all()

    columnas = [
        {"field": "codigo", "label": "Código", "sortable": True, "width": "120px"},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "250px"},
        {"field": "notas", "label": "Notas", "sortable": False, "width": "auto"},
    ]
    
    context = build_grid(
        request=request,
        qs=qs,
        columnas=columnas,
        page_size=10
    )

    return render(request, "core/calidad.html", context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Calidad
from .forms import CalidadForm


def calidad_nuevo(request):

    if request.method == "POST":
        form = CalidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("calidad")
    else:
        form = CalidadForm()

    return render(request, "core/calidad_form.html", {
        "form": form,
        "modo": "nuevo"
    })


def calidad_ver(request, id):

    obj = get_object_or_404(Calidad, id=id)
    form = CalidadForm(instance=obj)

    # desactivar campos
    for field in form.fields.values():
        field.disabled = True

    return render(request, "core/calidad_form.html", {
        "form": form,
        "modo": "ver",
        "id": id
    })


def calidad_editar(request, id):

    obj = get_object_or_404(Calidad, id=id)

    if request.method == "POST":
        form = CalidadForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("calidad")
    else:
        form = CalidadForm(instance=obj)

    return render(request, "core/calidad_form.html", {
        "form": form,
        "modo": "editar",
        "id": id
    })


def calidad_eliminar(request, id):

    obj = get_object_or_404(Calidad, id=id)

    if request.method == "POST":
        obj.delete()
        return redirect("calidad")

    return render(request, "core/calidad_confirm_delete.html", {
        "obj": obj
    })