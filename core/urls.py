from django.urls import path
from . import views

from .views_grid import grid_view
from .grid_configs import (
    CALIDAD_GRID,
    CATEGORIA_GRID,
    COMERCIAL_GRID,
    REPRESENTANTE_GRID,
    CLIENTE_GRID,
    INCIDENCIA_GRID,
    ACCION_GRID
)

urlpatterns = [

    path("", views.home, name="home"),

    # =========================
    # GRID CALIDAD
    # =========================
    path(
        "calidad/",
        grid_view,
        {"config": CALIDAD_GRID},
        name="calidad",
    ),

    path("calidad/nuevo/", views.calidad_nuevo, name="calidad_nuevo"),
    path("calidad/<int:id>/", views.calidad_ver, name="calidad_ver"),
    path("calidad/<int:id>/editar/", views.calidad_editar, name="calidad_editar"),
    path("calidad/<int:id>/eliminar/", views.calidad_eliminar, name="calidad_eliminar"),

    # =========================
    # GRID CATEGORIAS
    # =========================
    path(
        "categorias/",
        grid_view,
        {"config": CATEGORIA_GRID},
        name="categorias",
    ),

    path("categorias/nuevo/", views.categoria_nuevo, name="categoria_nuevo"),
    path("categorias/<int:id>/", views.categoria_ver, name="categoria_ver"),
    path("categorias/<int:id>/editar/", views.categoria_editar, name="categoria_editar"),
    path("categorias/<int:id>/eliminar/", views.categoria_eliminar, name="categoria_eliminar"),

    # =========================
    # GRID COMERCIAL
    # =========================
    path(
        "comerciales/",
        grid_view,
        {"config": COMERCIAL_GRID},
        name="comerciales",
    ),

    path("comerciales/nuevo/", views.comercial_nuevo, name="comercial_nuevo"),
    path("comerciales/<int:id>/", views.comercial_ver, name="comercial_ver"),
    path("comerciales/<int:id>/editar/", views.comercial_editar, name="comercial_editar"),
    path("comerciales/<int:id>/eliminar/", views.comercial_eliminar, name="comercial_eliminar"),

    # =========================
    # GRID REPRESENTANTE
    # =========================
    path(
        "representantes/",
        grid_view,
        {"config": REPRESENTANTE_GRID},
        name="representantes",
    ),

    path("representantes/nuevo/", views.representante_nuevo, name="representante_nuevo"),
    path("representantes/<int:id>/", views.representante_ver, name="representante_ver"),
    path("representantes/<int:id>/editar/", views.representante_editar, name="representante_editar"),
    path("representantes/<int:id>/eliminar/", views.representante_eliminar, name="representante_eliminar"),

    # =========================
    # GRID CLIENTE
    # =========================
    path(
        "clientes/",
        grid_view,
        {"config": CLIENTE_GRID},
        name="clientes",
    ),

    path("clientes/nuevo/", views.cliente_nuevo, name="cliente_nuevo"),
    path("clientes/<int:id>/", views.cliente_ver, name="cliente_ver"),
    path("clientes/<int:id>/editar/", views.cliente_editar, name="cliente_editar"),
    path("clientes/<int:id>/eliminar/", views.cliente_eliminar, name="cliente_eliminar"),


    # =========================
    # GRID ACCION
    # =========================
    path(
        "acciones/",
        grid_view,
        {"config": ACCION_GRID},
        name="acciones",
    ),

    path("acciones/nuevo/", views.accion_nuevo, name="accion_nuevo"),
    path("acciones/<int:id>/", views.accion_ver, name="accion_ver"),
    path("acciones/<int:id>/editar/", views.accion_editar, name="accion_editar"),
    path("acciones/<int:id>/eliminar/", views.accion_eliminar, name="accion_eliminar"),


    # =========================
    # GRID INCIDENCIAS
    # =========================
    path(
        "incidencias/",
        grid_view,
        {"config": INCIDENCIA_GRID},
        name="incidencias",
    ),

    path("incidencias/nuevo/", views.incidencia_nuevo, name="incidencia_nuevo"),
    path("incidencias/<int:id>/", views.incidencia_ver, name="incidencia_ver"),
    path("incidencias/<int:id>/editar/", views.incidencia_editar, name="incidencia_editar"),
    path("incidencias/<int:id>/eliminar/", views.incidencia_eliminar, name="incidencia_eliminar"),

    # =========================
    # ACCIONES INCIDENCIAS
    # =========================
    path(
        "incidencias/<int:id>/cerrar/",
        views.incidencia_cerrar,
        name="incidencia_cerrar"
    ),

    # =========================
    # AJAX
    # =========================
    path(
        "ajax/representante/<int:id>/comercial/",
        views.ajax_representante_comercial,
        name="ajax_representante_comercial"
    ),

    path(
        "ajax/cliente/<int:id>/info/",
        views.ajax_cliente_info,
        name="ajax_cliente_info"
    ),
]