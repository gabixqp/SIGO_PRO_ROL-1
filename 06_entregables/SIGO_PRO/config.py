"""Configuracion central del proyecto.

Aqui se definen rutas, nombres de archivos, columnas esperadas y valores de
negocio por defecto. Mantenerlos juntos evita repetir cadenas de texto en todo
el codigo y hace mas facil cambiar la estructura de datos despues.
"""

from pathlib import Path

# Carpeta raiz del proyecto. Todas las rutas relativas salen de aqui.
BASE_DIR = Path(__file__).resolve().parent
# Carpeta donde viven los CSV y JSON de datos.
DATA_DIR = BASE_DIR / "data"
# Carpeta general para archivos generados por la aplicacion.
OUTPUT_DIR = BASE_DIR / "output"
# Subcarpeta para reportes de texto.
REPORTES_DIR = OUTPUT_DIR / "reportes"
# Subcarpeta para imagenes PNG de graficos.
GRAFICOS_DIR = OUTPUT_DIR / "graficos"
# Subcarpeta para CSV exportados.
EXPORTACIONES_DIR = OUTPUT_DIR / "exportaciones"

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

# Columnas obligatorias para que cada CSV pueda operar sin romper pantallas.
COLUMNAS_CSV = {
    "clientes.csv": [
        "id_cliente", "nombre", "tipo", "canal", "contacto", "telefono",
        "estado", "fecha_registro",
    ],
    "productos.csv": [
        "id_producto", "nombre", "categoria", "precio_venta",
        "stock_actual", "stock_minimo", "unidad",
    ],
    "insumos.csv": [
        "id_insumo", "nombre", "unidad", "stock_actual", "stock_minimo",
        "costo_unitario", "merma_pct",
    ],
    "recetas.csv": ["id_receta", "id_producto", "id_insumo", "cantidad"],
    "pedidos.csv": ["id_pedido", "id_cliente", "fecha", "canal", "estado", "total"],
    "detalle_pedidos.csv": [
        "id_detalle", "id_pedido", "id_producto", "cantidad",
        "precio_unitario", "subtotal",
    ],
    "produccion.csv": ["id_orden", "id_producto", "cantidad", "fecha", "estado"],
    "despachos.csv": [
        "id_despacho", "id_pedido", "fecha_programada",
        "fecha_entrega", "estado",
    ],
    "feedback.csv": [
        "id_feedback", "id_pedido", "id_cliente", "puntuacion",
        "comentario", "fecha",
    ],
}

# Columnas que no son indispensables para arrancar, pero activan calculos mas
# completos cuando existen en los CSV reales.
COLUMNAS_OPCIONALES_CSV = {
    "productos.csv": [
        "familia",
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
    ],
    "pedidos.csv": [
        "tipo_comprobante",
        "valor_venta",
        "igv_pct",
        "igv",
        "total_con_igv",
    ],
}
