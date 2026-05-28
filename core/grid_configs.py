from .models import Calidad
from .models import Categoria
from .models import Comercial
from .models import Representante
from .models import Cliente
from .models import Incidencia
from .models import Detalle


CALIDAD_GRID = {
    "model": Calidad,
    "template": "core/calidad.html",

    "columns": [
        {"field": "codigo", "label": "Código", "sortable": True, "width": "120px"},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "250px"},
        {"field": "notas", "label": "Notas", "sortable": True, "width": "auto"},
    ],

    # 🔥 NUEVO → filtros declarativos
    "filters": [
        {"field": "codigo", "label": "Código", "type": "text"},
        {"field": "descripcion", "label": "Descripción", "type": "text"},
        {"field": "notas", "label": "Notas", "type": "text"},
    ],

    "page_size": 10,

    "actions": {
        "ver": "calidad_ver",
        "editar": "calidad_editar",
        "eliminar": "calidad_eliminar",
        "nuevo": "calidad_nuevo",
    }
}

CATEGORIA_GRID = {
    "model": Categoria,
    "template": "core/categoria.html",

    "columns": [
        {"field": "codigo", "label": "Código", "sortable": True, "width": "120px"},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "250px"},
        {"field": "notas", "label": "Notas", "sortable": True, "width": "auto"},
    ],

    # 🔥 NUEVO → filtros declarativos
    "filters": [
        {"field": "codigo", "label": "Código", "type": "text"},
        {"field": "descripcion", "label": "Descripción", "type": "text"},
        {"field": "notas", "label": "Notas", "type": "text"},
    ],

    "page_size": 10,

    "actions": {
        "ver": "categoria_ver",
        "editar": "categoria_editar",
        "eliminar": "categoria_eliminar",
        "nuevo": "categoria_nuevo",
    }
}


COMERCIAL_GRID = {
    "model": Comercial,
    "template": "core/comercial.html",

    "columns": [
        {"field": "codigo", "label": "Código", "sortable": True, "width": "120px"},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "250px"},
        {"field": "email", "label": "Email", "sortable": True, "width": "250px"},
        {"field": "telefono", "label": "Teléfono", "sortable": True, "width": "auto"},
    ],

    "filters": [
        {"field": "codigo", "label": "Código", "type": "text"},
        {"field": "descripcion", "label": "Descripción", "type": "text"},
        {"field": "email", "label": "Email", "type": "text"},
        {"field": "telefono", "label": "Teléfono", "type": "text"},
    ],

    "page_size": 10,

    "actions": {
        "ver": "comercial_ver",
        "editar": "comercial_editar",
        "eliminar": "comercial_eliminar",
        "nuevo": "comercial_nuevo",
    }
}


from .models import Calidad, Categoria, Comercial, Representante


REPRESENTANTE_GRID = {
    "model": Representante,
    "template": "core/representante.html",

    "columns": [
        {"field": "codigo", "label": "Código", "sortable": True, "width": "120px"},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "250px"},
        {"field": "comercial", "label": "Comercial", "sortable": True, "width": "auto"},
    ],

    "filters": [
        {"field": "codigo", "label": "Código", "type": "text"},
        {"field": "descripcion", "label": "Descripción", "type": "text"},
        {"field": "comercial", "label": "Comercial", "type": "text"},
    ],

    "page_size": 10,

    "actions": {
        "ver": "representante_ver",
        "editar": "representante_editar",
        "eliminar": "representante_eliminar",
        "nuevo": "representante_nuevo",
    }
}


CLIENTE_GRID = {

    "model": Cliente,
    "template": "core/cliente.html",

    "columns": [
        {"field": "codigo", "label": "Código", "sortable": True, "width": "120px"},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "250px"},
        {"field": "representante", "label": "Representante", "sortable": True, "width": "250px"},
        {"field": "representante__comercial__descripcion","label": "Comercial", "sortable": True,"width": "auto"},
    ],

    "filters": [
        {"field": "codigo", "label": "Código", "type": "text"},
        {"field": "descripcion", "label": "Descripción", "type": "text"},
        {"field": "representante", "label": "Representante", "type": "text"},
        {"field": "comercial", "label": "Comercial", "type": "text"},
    ],

    "page_size": 10,

    "actions": {
        "ver": "cliente_ver",
        "editar": "cliente_editar",
        "eliminar": "cliente_eliminar",
        "nuevo": "cliente_nuevo",
    }
}

INCIDENCIA_GRID = {

    "model": Incidencia,

    "template": "core/incidencia.html",

    "columns": [

        {"field": "codigo_visual", "label": "Código", "sortable": True, "width": "80px",},
        {"field": "descripcion", "label": "Descripción", "sortable": True, "width": "170px",},
        {"field": "cliente_visual", "label": "Cliente", "sortable": True, "width": "120px",},
        {"field": "representante", "label": "Representante", "sortable": True, "width": "120px",},
        {"field": "comercial", "label": "Comercial", "sortable": True, "width": "120px",},
        {"field": "calidad", "label": "Calidad", "sortable": True, "width": "120px",},
        {"field": "categoria", "label": "Categoría", "sortable": True, "width": "120px",},
        {"field": "fecha_apertura", "label": "F. Apertura", "sortable": True, "width": "100px",},
        {"field": "fecha_ultimo", "label": "F. Actualiz", "sortable": True, "width": "100px",},
        {"field": "fecha_cierre", "label": "F. Cierre", "sortable": True, "width": "100px",},
        {"field": "fecha_control", "label": "F. Control", "sortable": True, "width": "100px",},
        {"field": "cerrado", "label": "Cerrado", "sortable": True, "width": "90px",},
        {"field": "control", "label": "Control", "sortable": True, "width": "90px",},
        {"field": "usuario_apertura", "label": "U. Apertura", "sortable": True, "width": "100px",},
        {"field": "usuario_actualizacion", "label": "U. Actualiz", "sortable": True, "width": "100px",},
        {"field": "usuario_cierre", "label": "U. Cierre", "sortable": True, "width": "100px",},
        {"field": "usuario_control", "label": "U. Control", "sortable": True, "width": "100px", },
        {"field": "notas", "label": "Notas", "sortable": True, "width": "100px", },
    ],

    "filters": {

        "general": [
            {"field": "codigo_visual", "label": "Código", "type": "text",},
            {"field": "descripcion", "label": "Descripción", "type": "text",},
            {"field": "cliente", "label": "Cliente", "type": "text",},
            {"field": "representante", "label": "Representante", "type": "text",},
            {"field": "comercial", "label": "Comercial", "type": "text",},
            {"field": "calidad", "label": "Calidad", "type": "text",},
            {"field": "categoria", "label": "Categoría", "type": "text",},
            {"field": "notas", "label": "Notas", "type": "text",},
        ],

        "usuarios": [
            {"field": "usuario_apertura", "label": "Apertura", "type": "text", },
            {"field": "usuario_actualizacion",  "label": "Actualización", "type": "text",},
            {"field": "usuario_cierre", "label": "Cierre", "type": "text", },
            {"field": "usuario_control", "label": "Control", "type": "text", },
        ],

        "fechas": [
            {"field": "fecha_apertura", "label": "Apertura", "type": "daterange",},
            {"field": "fecha_ultimo", "label": "Actualización", "type": "daterange",},
            {"field": "fecha_cierre", "label": "Cierre", "type": "daterange",},
            {"field": "fecha_control", "label": "Control", "type": "daterange",},
        ],

        "booleanos": [
            {"field": "cerrado", "label": "Cerrado", "type": "boolean",},
            {"field": "control", "label": "Control", "type": "boolean",},
        ],
    },

    "page_size": 10,

    "actions": {
        "ver": "incidencia_ver",
        "editar": "incidencia_editar",
        "eliminar": "incidencia_eliminar",
        "nuevo": "incidencia_nuevo",
    }
}


DETALLE_GRID = {

    "model": Detalle,

    "template": "components/detalle_grid.html",

    "columns": [

        {
            "field": "fecha",
            "label": "Fecha",
            "sortable": True,
            "width": "180px"
        },

        {
            "field": "tipo",
            "label": "Tipo",
            "sortable": True,
            "width": "120px"
        },

        {
            "field": "descripcion",
            "label": "Descripción",
            "sortable": True,
            "width": "260px"
        },

        {
            "field": "usuario",
            "label": "Usuario",
            "sortable": True,
            "width": "180px"
        },

        {
            "field": "control",
            "label": "Control",
            "sortable": True,
            "width": "100px"
        },
    ],

    "filters": [

        {
            "field": "descripcion",
            "label": "Descripción",
            "type": "text"
        },

        {
            "field": "tipo",
            "label": "Tipo",
            "type": "text"
        },
    ],

    "page_size": 10,

    "actions": {
        "ver": "detalle_ver",
        "editar": "detalle_editar",
        "eliminar": "detalle_eliminar",
        "nuevo": "detalle_nuevo",
    }
}