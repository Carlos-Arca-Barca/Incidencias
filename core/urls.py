from django.urls import path
from . import views

from .views import (
    home,
    calidad_ver,
    calidad_editar,
    calidad_nuevo,
    calidad_eliminar,
    categoria_ver,
    categoria_editar,
    categoria_nuevo,
    categoria_eliminar,
    comercial_ver,
    comercial_editar,
    comercial_nuevo,
    comercial_eliminar,
    representante_ver,
    representante_editar,
    representante_nuevo,
    representante_eliminar,
    cliente_ver,
    cliente_editar,
    cliente_nuevo,
    cliente_eliminar,
    incidencia_ver,
    incidencia_editar,
    incidencia_nuevo,
    incidencia_eliminar,
)

from .views_grid import grid_view
from .grid_configs import CALIDAD_GRID, CATEGORIA_GRID, COMERCIAL_GRID, REPRESENTANTE_GRID, CLIENTE_GRID, INCIDENCIA_GRID


urlpatterns = [
    path("", home, name="home"),

    # GRID CALIDAD (framework)
    path(
        "calidad/",
        grid_view,
        {"config": CALIDAD_GRID},
        name="calidad",
    ),

    # CRUD
    path("calidad/nuevo/", calidad_nuevo, name="calidad_nuevo"),
    path("calidad/<int:id>/", calidad_ver, name="calidad_ver"),
    path("calidad/<int:id>/editar/", calidad_editar, name="calidad_editar"),
    path("calidad/<int:id>/eliminar/", calidad_eliminar, name="calidad_eliminar"),


    # GRID CATEGORIAS
    path(
        "categorias/",
        grid_view,
        {"config": CATEGORIA_GRID},
        name="categorias",
    ),
    
    # CRUD
    path("categorias/nuevo/", categoria_nuevo, name="categoria_nuevo"),
    path("categorias/<int:id>/", categoria_ver, name="categoria_ver"),
    path("categorias/<int:id>/editar/", categoria_editar, name="categoria_editar"),
    path("categorias/<int:id>/eliminar/", categoria_eliminar, name="categoria_eliminar"),


    # GRID COMERCIAL
    path(
        "comerciales/",
        grid_view,
        {"config": COMERCIAL_GRID},
        name="comerciales",
    ),

    # CRUD
    path("comerciales/nuevo/", comercial_nuevo, name="comercial_nuevo"),
    path("comerciales/<int:id>/", comercial_ver, name="comercial_ver"),
    path("comerciales/<int:id>/editar/", comercial_editar, name="comercial_editar"),
    path("comerciales/<int:id>/eliminar/", comercial_eliminar, name="comercial_eliminar"),


    # GRID REPRESENTANTE
    path(
        "representantes/",
        grid_view,
        {"config": REPRESENTANTE_GRID},
        name="representantes",
    ),

    # CRUD
    path("representantes/nuevo/", representante_nuevo, name="representante_nuevo"),
    path("representantes/<int:id>/", representante_ver, name="representante_ver"),
    path("representantes/<int:id>/editar/", representante_editar, name="representante_editar"),
    path("representantes/<int:id>/eliminar/", representante_eliminar, name="representante_eliminar"),


    # GRID CLIENTE
    path(
        "clientes/",
        grid_view,
        {"config": CLIENTE_GRID},
        name="clientes",
    ),

    # CRUD
    path("clientes/nuevo/", cliente_nuevo, name="cliente_nuevo"),
    path("clientes/<int:id>/", cliente_ver, name="cliente_ver"),
    path("clientes/<int:id>/editar/", cliente_editar, name="cliente_editar"),
    path("clientes/<int:id>/eliminar/", cliente_eliminar, name="cliente_eliminar"),


    # GRID INCIDENCIAS
    path(
        "incidencias/",
        grid_view,
        {"config": INCIDENCIA_GRID},
        name="incidencias",
    ),

    # CRUD
    path("incidencias/nuevo/", incidencia_nuevo, name="incidencia_nuevo"),
    path("incidencias/<int:id>/", incidencia_ver, name="incidencia_ver"),
    path("incidencias/<int:id>/editar/", incidencia_editar, name="incidencia_editar"),
    path("incidencias/<int:id>/eliminar/", incidencia_eliminar, name="incidencia_eliminar"),


    
    # OTROS
    path(
        "ajax/representante/<int:id>/comercial/",
        views.ajax_representante_comercial,
        name="ajax_representante_comercial"
    ),


    # endpoint
    path(
        "ajax/cliente/<int:id>/info/",
        views.ajax_cliente_info,
        name="ajax_cliente_info"
    ),

]