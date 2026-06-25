"""Configuracion central del proyecto SIGO-PRO FoodOps.

Este archivo concentra rutas, datos de empresa, parametros de negocio,
estructura de archivos, columnas esperadas y configuracion visual del sistema.

Importante para el Rol 1 Integrador:
- No colocar rutas sueltas en otros archivos.
- No repetir colores, estados, nombres de modulos o textos globales.
- Mantener compatibilidad con modules/, analytics/ y pages/.
"""

from pathlib import Path


# ============================================================
# 1. RUTAS PRINCIPALES DEL PROYECTO
# ============================================================

# Carpeta raiz del proyecto. Todas las rutas relativas salen de aqui.
BASE_DIR = Path(__file__).resolve().parent

# Carpeta donde viven los CSV y JSON de datos.
DATA_DIR = BASE_DIR / "data"

# Carpeta general para archivos generados por la aplicacion.
OUTPUT_DIR = BASE_DIR / "output"

# Subcarpetas de salida.
REPORTES_DIR = OUTPUT_DIR / "reportes"
GRAFICOS_DIR = OUTPUT_DIR / "graficos"
EXPORTACIONES_DIR = OUTPUT_DIR / "exportaciones"

# Carpetas auxiliares para mejoras de integracion.
LOGS_DIR = BASE_DIR / "logs"
BACKUPS_DIR = BASE_DIR / "backups"
EVIDENCIAS_DIR = BASE_DIR / "evidencias"

# Carpeta de recursos visuales.
ASSETS_DIR = BASE_DIR / "assets"
LOGO_DIR = ASSETS_DIR / "logo"
FONDOS_DIR = ASSETS_DIR / "fondos"
PRODUCTOS_IMG_DIR = ASSETS_DIR / "productos"
ICONOS_DIR = ASSETS_DIR / "iconos"


# ============================================================
# 2. DATOS DE LA EMPRESA PILOTO
# ============================================================

EMPRESA = {
    "nombre_comercial": "Gourmet Senor de Locumba",
    "razon_social": "GOURMET SENOR DE LOCUMBA SOCIEDAD ANONIMA CERRADA",
    "ruc": "20612215546",
    "ubicacion": "Tiabaya, Arequipa",
    "rubro": "Actividades de restaurantes y servicio movil de comidas",
    "tipo_empresa": "S.A.C.",
    "estado": "Activo",
    "condicion": "Habido",
    "sistema": "SIGO-PRO FoodOps",
    "descripcion_sistema": (
        "Sistema de gestion operativa para pedidos, produccion, inventario, "
        "costos, despachos y reportes inteligentes."
    ),
}


# ============================================================
# 3. CONFIGURACION VISUAL GENERAL
# ============================================================

APP_CONFIG = {
    "page_title": "SIGO-PRO FoodOps",
    "page_icon": "🍽️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

TEXTOS_APP = {
    "titulo": "SIGO-PRO FoodOps",
    "subtitulo": "Gestion operativa inteligente para servicios de alimentacion",
    "hero_titulo": "Gestiona pedidos, produccion, inventario y costos desde un solo lugar.",
    "hero_descripcion": (
        "Sistema desarrollado para Gourmet Senor de Locumba S.A.C., orientado "
        "a mejorar el control operativo, la toma de decisiones y la experiencia "
        "de gestion interna."
    ),
    "footer": "SIGO-PRO FoodOps | Proyecto de Computacion Aplicada | Ingenieria Industrial",
}


# Paleta visual definida en el Design Brief.
COLORES = {
    "rojo_vino": "#8B0F1A",
    "rojo_vino_oscuro": "#5E0810",
    "negro_carbon": "#111111",
    "gris_carbon": "#1C1C1C",
    "gris_medio": "#4B4B4B",
    "crema": "#F6EFE3",
    "crema_suave": "#FFF9F0",
    "blanco": "#FFFFFF",
    "dorado": "#C9A44C",
    "dorado_suave": "#E2C878",
    "verde": "#2E7D32",
    "amarillo": "#F9A825",
    "rojo_alerta": "#C62828",
    "azul_info": "#1565C0",
}

# Alias de colores para facilitar uso en UI.
COLOR_PRIMARIO = COLORES["rojo_vino"]
COLOR_SECUNDARIO = COLORES["dorado"]
COLOR_FONDO = COLORES["negro_carbon"]
COLOR_TEXTO = COLORES["crema_suave"]


# ============================================================
# 4. ASSETS VISUALES
# ============================================================

ASSETS = {
    "logo_principal": LOGO_DIR / "logo_sigo_pro.png",
    "logo_blanco": LOGO_DIR / "logo_sigo_pro_blanco.png",
    "logo_gourmet": LOGO_DIR / "logo_gourmet.png",
    "hero": FONDOS_DIR / "hero_foodops.jpg",
    "fallback": FONDOS_DIR / "fallback_foodops.jpg",
    "producto_menu_ejecutivo": PRODUCTOS_IMG_DIR / "menu_ejecutivo.jpg",
    "producto_almuerzo_corporativo": PRODUCTOS_IMG_DIR / "almuerzo_corporativo.jpg",
    "producto_menu_familiar": PRODUCTOS_IMG_DIR / "menu_familiar.jpg",
    "producto_menu_institucional": PRODUCTOS_IMG_DIR / "menu_institucional.jpg",
    "producto_bebidas": PRODUCTOS_IMG_DIR / "bebidas.jpg",
    "producto_postres": PRODUCTOS_IMG_DIR / "postres.jpg",
}

ICONOS_MODULOS = {
    "inicio": ICONOS_DIR / "icon_inicio.svg",
    "clientes": ICONOS_DIR / "icon_clientes.svg",
    "productos": ICONOS_DIR / "icon_productos.svg",
    "pedidos": ICONOS_DIR / "icon_pedidos.svg",
    "produccion": ICONOS_DIR / "icon_produccion.svg",
    "despachos": ICONOS_DIR / "icon_despachos.svg",
    "costos": ICONOS_DIR / "icon_costos.svg",
    "reportes": ICONOS_DIR / "icon_reportes.svg",
    "configuracion": ICONOS_DIR / "icon_configuracion.svg",
}


# ============================================================
# 5. MODULOS DEL SISTEMA
# ============================================================

MODULOS_APP = [
    {
        "id": "inicio",
        "nombre": "Inicio",
        "descripcion": "Vista general del sistema y acceso rapido a modulos.",
        "pagina": "1_Inicio.py",
        "icono": ICONOS_MODULOS["inicio"],
    },
    {
        "id": "clientes",
        "nombre": "Clientes",
        "descripcion": "Gestion de clientes, canales y datos de contacto.",
        "pagina": "2_Clientes.py",
        "icono": ICONOS_MODULOS["clientes"],
    },
    {
        "id": "productos",
        "nombre": "Productos e insumos",
        "descripcion": "Catalogo de menus, productos, insumos y stock base.",
        "pagina": "3_Productos_Insumos.py",
        "icono": ICONOS_MODULOS["productos"],
    },
    {
        "id": "pedidos",
        "nombre": "Pedidos",
        "descripcion": "Registro y seguimiento de pedidos por cliente y canal.",
        "pagina": "4_Pedidos.py",
        "icono": ICONOS_MODULOS["pedidos"],
    },
    {
        "id": "produccion",
        "nombre": "Produccion",
        "descripcion": "Planificacion y control de ordenes de produccion.",
        "pagina": "5_Produccion.py",
        "icono": ICONOS_MODULOS["produccion"],
    },
    {
        "id": "despachos",
        "nombre": "Despachos",
        "descripcion": "Control de entregas, estados y seguimiento logistico.",
        "pagina": "6_Despachos.py",
        "icono": ICONOS_MODULOS["despachos"],
    },
    {
        "id": "costos",
        "nombre": "Costos",
        "descripcion": "Calculo de costos, margenes y rentabilidad.",
        "pagina": "7_Costos.py",
        "icono": ICONOS_MODULOS["costos"],
    },
    {
        "id": "reportes",
        "nombre": "Reportes inteligentes",
        "descripcion": "Indicadores, graficos y recomendaciones operativas.",
        "pagina": "8_Reportes_Inteligentes.py",
        "icono": ICONOS_MODULOS["reportes"],
    },
    {
        "id": "configuracion",
        "nombre": "Configuracion",
        "descripcion": "Datos de empresa y parametros generales del sistema.",
        "pagina": "9_Configuracion.py",
        "icono": ICONOS_MODULOS["configuracion"],
    },
]


# ============================================================
# 6. PARAMETROS DE NEGOCIO
# ============================================================

# Parametros de negocio usados cuando el archivo CSV todavia no trae valores.
IGV_PCT_DEFAULT = 18.0
METODO_VALUACION_INVENTARIO = "PROMEDIO_PONDERADO"
MARGEN_MINIMO_DEFAULT = 20.0

# Umbral minimo de margen por familia. Si una familia no aparece aqui, se usa
# MARGEN_MINIMO_DEFAULT.
MARGEN_MINIMO_POR_FAMILIA = {
    "panaderia": 22.0,
    "pasteleria": 25.0,
    "bebidas": 18.0,
    "comidas": 20.0,
    "otros": 20.0,
}


# ============================================================
# 7. CATALOGOS COMPARTIDOS
# ============================================================

CANALES_VENTA = [
    "B2C",
    "B2B",
    "Corporativo",
    "Institucional",
    "Mayorista",
    "Recojo en local",
    "Delivery",
]

TIPOS_CLIENTE = [
    "Persona natural",
    "Empresa",
    "Institucion",
    "Cliente corporativo",
]

TIPOS_COMPROBANTE = [
    "Boleta",
    "Factura",
    "Nota de venta",
]

ESTADOS_CLIENTE = [
    "activo",
    "inactivo",
]

ESTADOS_PRODUCTO = [
    "activo",
    "inactivo",
]

ESTADOS_PEDIDO = [
    "registrado",
    "confirmado",
    "en_produccion",
    "listo",
    "en_despacho",
    "entregado",
    "retrasado",
    "cancelado",
]

TRANSICIONES_PEDIDO = {
    "registrado": ["confirmado", "cancelado"],
    "confirmado": ["en_produccion", "cancelado"],
    "en_produccion": ["listo", "retrasado", "cancelado"],
    "listo": ["en_despacho", "retrasado"],
    "en_despacho": ["entregado", "retrasado"],
    "retrasado": ["entregado", "cancelado"],
    "entregado": [],
    "cancelado": [],
}

ESTADOS_DESPACHO = [
    "programado",
    "en_ruta",
    "entregado",
    "retrasado",
    "cancelado",
]

NIVELES_ALERTA = {
    "success": "Correcto",
    "info": "Informacion",
    "warning": "Advertencia",
    "danger": "Critico",
}


# ============================================================
# 8. ARCHIVOS CSV Y JSON
# ============================================================

# Mapa logico: nombre interno del modulo -> archivo fisico en data/.
ARCHIVOS_CSV = {
    "clientes": "clientes.csv",
    "productos": "productos.csv",
    "insumos": "insumos.csv",
    "recetas": "recetas.csv",
    "pedidos": "pedidos.csv",
    "detalle_pedidos": "detalle_pedidos.csv",
    "produccion": "produccion.csv",
    "despachos": "despachos.csv",
    "feedback": "feedback.csv",
}

ARCHIVOS_JSON = {
    "empresa": "empresa.json",
}

# Rutas completas de archivos de datos.
RUTAS_CSV = {
    clave: DATA_DIR / nombre_archivo
    for clave, nombre_archivo in ARCHIVOS_CSV.items()
}

RUTAS_JSON = {
    clave: DATA_DIR / nombre_archivo
    for clave, nombre_archivo in ARCHIVOS_JSON.items()
}


# ============================================================
# 9. COLUMNAS DE DATOS
# ============================================================

# Columnas obligatorias para que cada CSV pueda operar sin romper pantallas.
COLUMNAS_CSV = {
    "clientes.csv": [
        "id_cliente",
        "nombre",
        "tipo",
        "canal",
        "contacto",
        "telefono",
        "estado",
        "fecha_registro",
    ],
    "productos.csv": [
        "id_producto",
        "nombre",
        "categoria",
        "precio_venta",
        "stock_actual",
        "stock_minimo",
        "unidad",
    ],
    "insumos.csv": [
        "id_insumo",
        "nombre",
        "unidad",
        "stock_actual",
        "stock_minimo",
        "costo_unitario",
        "merma_pct",
    ],
    "recetas.csv": [
        "id_receta",
        "id_producto",
        "id_insumo",
        "cantidad",
    ],
    "pedidos.csv": [
        "id_pedido",
        "id_cliente",
        "fecha",
        "canal",
        "estado",
        "total",
    ],
    "detalle_pedidos.csv": [
        "id_detalle",
        "id_pedido",
        "id_producto",
        "cantidad",
        "precio_unitario",
        "subtotal",
    ],
    "produccion.csv": [
        "id_orden",
        "id_producto",
        "cantidad",
        "fecha",
        "estado",
    ],
    "despachos.csv": [
        "id_despacho",
        "id_pedido",
        "fecha_programada",
        "fecha_entrega",
        "estado",
    ],
    "feedback.csv": [
        "id_feedback",
        "id_pedido",
        "id_cliente",
        "puntuacion",
        "comentario",
        "fecha",
    ],
}

# Columnas que no son indispensables para arrancar, pero activan calculos mas
# completos cuando existen en los CSV reales.
COLUMNAS_OPCIONALES_CSV = {
    "clientes.csv": [
        "documento",
        "correo",
        "direccion",
    ],
    "productos.csv": [
        "familia",
        "estado",
        "mano_obra_directa_unitaria",
        "cif_gas_unitario",
        "cif_energia_unitario",
        "cif_depreciacion_unitario",
        "cif_otros_unitario",
        "costo_fijo_asignado",
    ],
    "insumos.csv": [
        "metodo_valuacion",
        "costo_promedio",
        "costo_peps",
        "valor_inventario",
        "fecha_vencimiento",
    ],
    "pedidos.csv": [
        "tipo_comprobante",
        "valor_venta",
        "igv_pct",
        "igv",
        "total_con_igv",
    ],
    "produccion.csv": [
        "cantidad_programada",
        "cantidad_producida",
        "cantidad_vendida",
        "sobrante",
    ],
    "despachos.csv": [
        "tipo_entrega",
        "responsable",
        "hora_salida",
        "hora_entrega",
        "motivo_no_entrega",
    ],
}


# ============================================================
# 10. FUNCIONES AUXILIARES DE CONFIGURACION
# ============================================================

def crear_carpetas_base() -> None:
    """Crea carpetas base si no existen.

    Se puede llamar desde app.py o core/storage.py para asegurar que el sistema
    tenga sus carpetas minimas antes de leer o escribir archivos.
    """
    carpetas = [
        DATA_DIR,
        OUTPUT_DIR,
        REPORTES_DIR,
        GRAFICOS_DIR,
        EXPORTACIONES_DIR,
        LOGS_DIR,
        BACKUPS_DIR,
        ASSETS_DIR,
        LOGO_DIR,
        FONDOS_DIR,
        PRODUCTOS_IMG_DIR,
        ICONOS_DIR,
    ]

    for carpeta in carpetas:
        carpeta.mkdir(parents=True, exist_ok=True)


def obtener_ruta_csv(clave: str) -> Path:
    """Devuelve la ruta completa de un CSV a partir de su clave logica."""
    if clave not in RUTAS_CSV:
        raise KeyError(f"No existe una ruta CSV configurada para la clave: {clave}")

    return RUTAS_CSV[clave]


def obtener_asset(clave: str) -> Path:
    """Devuelve la ruta completa de un asset visual a partir de su clave."""
    if clave not in ASSETS:
        raise KeyError(f"No existe un asset configurado para la clave: {clave}")

    return ASSETS[clave]


def obtener_icono_modulo(clave: str) -> Path:
    """Devuelve la ruta del icono de un modulo."""
    if clave not in ICONOS_MODULOS:
        raise KeyError(f"No existe un icono configurado para el modulo: {clave}")

    return ICONOS_MODULOS[clave]