"""Calculos de costo, margen y punto de equilibrio por producto."""

import pandas as pd

try:
    from config import MARGEN_MINIMO_DEFAULT, MARGEN_MINIMO_POR_FAMILIA, METODO_VALUACION_INVENTARIO
except ImportError:
    # Valores seguros para que Streamlit no falle durante recargas parciales.
    MARGEN_MINIMO_DEFAULT = 20.0
    MARGEN_MINIMO_POR_FAMILIA = {}
    METODO_VALUACION_INVENTARIO = "PROMEDIO_PONDERADO"
from modules.productos import listar_productos
from modules.recetas import obtener_receta_producto
from modules.insumos import listar_insumos


def _numero(row, columna: str, default: float = 0.0) -> float:
    """Lee una columna como float; devuelve default si falta o no es numerica."""
    try:
        # row.get busca la columna. Si no existe, devuelve default.
        # float convierte el valor a numero decimal.
        return float(row.get(columna, default))
    except (TypeError, ValueError):
        # Si el valor no se puede convertir a numero, usamos el default.
        return default


def _costo_unitario_valuado(insumo) -> float:
    """Elige el costo unitario segun el metodo de valuacion configurado."""
    # Si el metodo es PEPS y existe costo_peps, usamos ese costo.
    if METODO_VALUACION_INVENTARIO == "PEPS" and "costo_peps" in insumo.index:
        return _numero(insumo, "costo_peps", _numero(insumo, "costo_unitario"))

    # Si no es PEPS pero existe costo_promedio, usamos promedio ponderado.
    if "costo_promedio" in insumo.index:
        return _numero(insumo, "costo_promedio", _numero(insumo, "costo_unitario"))

    # Si no hay columnas especiales, usamos costo_unitario normal.
    return _numero(insumo, "costo_unitario")


def obtener_umbral_margen_producto(id_producto) -> tuple[bool, float | str]:
    """Obtiene el margen minimo exigido para la familia/categoria del producto."""
    # Cargamos todos los productos.
    productos = listar_productos()

    # Buscamos el producto por ID; si no hay productos, producto queda vacio.
    producto = productos[productos["id_producto"] == id_producto] if not productos.empty else productos
    if producto.empty:
        return False, "Producto no encontrado."

    # Familia es mas especifica; si no existe, usamos categoria; si tampoco, "otros".
    familia = str(producto.iloc[0].get("familia", producto.iloc[0].get("categoria", "otros"))).strip().lower()

    # Buscamos el margen minimo de esa familia; si no esta, usamos el default.
    return True, MARGEN_MINIMO_POR_FAMILIA.get(familia, MARGEN_MINIMO_DEFAULT)


def obtener_desglose_costo_producto(id_producto) -> tuple[bool, pd.DataFrame | str]:
    """Calcula el costo de cada insumo de la receta de un producto."""
    # La receta dice que insumos y cantidades usa el producto.
    receta = obtener_receta_producto(id_producto)

    # La tabla de insumos tiene costos, unidades y merma.
    insumos = listar_insumos()
    if receta.empty:
        return False, "El producto no tiene receta configurada."
    if insumos.empty:
        return False, "No hay insumos disponibles."

    # Aqui guardaremos una fila de costo por cada insumo de la receta.
    filas = []
    for _, item in receta.iterrows():
        # item representa una linea de receta.
        insumo = insumos[insumos["id_insumo"] == item["id_insumo"]]
        if insumo.empty:
            return False, f"Insumo {item['id_insumo']} no encontrado."

        # Tomamos la primera fila del insumo encontrado.
        insumo = insumo.iloc[0]

        # Cantidad teorica que pide la receta.
        cantidad_receta = float(item["cantidad"])

        # Costo unitario segun metodo de valuacion.
        costo_unitario = _costo_unitario_valuado(insumo)

        # Merma es porcentaje de perdida adicional.
        merma_pct = _numero(insumo, "merma_pct")
        factor_merma = 1 + merma_pct / 100
        # Se separa costo teorico y costo por merma para explicar desperdicio.
        cantidad_con_merma = cantidad_receta * factor_merma
        costo_teorico = cantidad_receta * costo_unitario
        costo_merma = (cantidad_con_merma - cantidad_receta) * costo_unitario
        costo_aportado = costo_teorico + costo_merma

        # Agregamos una fila explicando el aporte de este insumo al costo.
        filas.append(
            {
                "id_insumo": item["id_insumo"],
                "insumo": insumo.get("nombre", item["id_insumo"]),
                "cantidad_receta": cantidad_receta,
                "unidad": insumo.get("unidad", ""),
                "costo_unitario_insumo": costo_unitario,
                "metodo_valuacion": METODO_VALUACION_INVENTARIO,
                "merma_pct": merma_pct,
                "cantidad_con_merma": cantidad_con_merma,
                "costo_insumo_teorico": costo_teorico,
                "costo_merma": costo_merma,
                "costo_aportado": costo_aportado,
            }
        )

    # Convertimos la lista de diccionarios en una tabla.
    return True, pd.DataFrame(filas)


def calcular_componentes_costo_producto(id_producto) -> tuple[bool, dict | str]:
    """Resume costo directo, costo indirecto y costo total del producto."""
    # Cargamos productos para leer precio, mano de obra y CIF.
    productos = listar_productos()
    producto = productos[productos["id_producto"] == id_producto] if not productos.empty else productos
    if producto.empty:
        return False, "Producto no encontrado."

    # Obtenemos el detalle de insumos calculado antes.
    ok, desglose = obtener_desglose_costo_producto(id_producto)
    if not ok:
        return False, desglose

    # Tomamos la fila del producto.
    producto = producto.iloc[0]

    # Mano de obra directa por unidad producida.
    mano_obra = _numero(producto, "mano_obra_directa_unitaria")
    # CIF = costos indirectos de fabricacion.
    cif_gas = _numero(producto, "cif_gas_unitario")
    cif_energia = _numero(producto, "cif_energia_unitario")
    cif_depreciacion = _numero(producto, "cif_depreciacion_unitario")
    cif_otros = _numero(producto, "cif_otros_unitario")

    # Sumamos costos teoricos de insumos.
    costo_insumos_teorico = float(desglose["costo_insumo_teorico"].sum())

    # Sumamos costos generados por merma.
    costo_mermas = float(desglose["costo_merma"].sum())

    # Directo = insumos teoricos + mano de obra directa.
    costo_directo = costo_insumos_teorico + mano_obra

    # Indirecto = merma + CIF.
    costo_indirecto = costo_mermas + cif_gas + cif_energia + cif_depreciacion + cif_otros

    # Devolvemos un diccionario con todos los componentes importantes.
    return True, {
        "insumos_teoricos": costo_insumos_teorico,
        "mano_obra_directa": mano_obra,
        "costo_directo": costo_directo,
        "mermas": costo_mermas,
        "gas": cif_gas,
        "energia": cif_energia,
        "depreciacion": cif_depreciacion,
        "otros_cif": cif_otros,
        "costo_indirecto": costo_indirecto,
        "costo_total": costo_directo + costo_indirecto,
    }


def calcular_costo_producto(id_producto) -> tuple[bool, float | str]:
    """Devuelve solo el costo total unitario del producto."""
    # Reutilizamos el calculo completo de componentes.
    ok, componentes = calcular_componentes_costo_producto(id_producto)
    if not ok:
        return False, componentes

    # Extraemos solo el costo_total.
    return True, float(componentes["costo_total"])


def calcular_margen_producto(id_producto) -> tuple[bool, float | str]:
    """Calcula margen porcentual: (precio - costo) / precio * 100."""
    # Cargamos el producto para leer su precio de venta.
    productos = listar_productos()
    producto = productos[productos["id_producto"] == id_producto] if not productos.empty else productos
    if producto.empty:
        return False, "Producto no encontrado."
    precio = float(producto.iloc[0]["precio_venta"])

    # No se puede calcular margen si el precio es cero o negativo.
    if precio <= 0:
        return False, "El precio de venta debe ser mayor que cero."

    # Calculamos costo del producto.
    ok, costo = calcular_costo_producto(id_producto)
    if not ok:
        return False, costo

    # Formula: porcentaje de ganancia sobre el precio.
    margen = ((precio - float(costo)) / precio) * 100
    return True, margen


def calcular_margen_contribucion_producto(id_producto) -> tuple[bool, float | str]:
    """Calcula cuanto queda por unidad luego de cubrir costos directos."""
    # Cargamos el producto para leer precio.
    productos = listar_productos()
    producto = productos[productos["id_producto"] == id_producto] if not productos.empty else productos
    if producto.empty:
        return False, "Producto no encontrado."
    precio = float(producto.iloc[0]["precio_venta"])

    # Obtenemos costos directos e indirectos.
    ok, componentes = calcular_componentes_costo_producto(id_producto)
    if not ok:
        return False, componentes

    # Margen de contribucion = precio - costo directo.
    return True, precio - float(componentes["costo_directo"])


def calcular_punto_equilibrio_producto(id_producto) -> tuple[bool, float | str]:
    """Calcula unidades necesarias para cubrir el costo fijo asignado."""
    # Cargamos el producto para leer costo fijo asignado.
    productos = listar_productos()
    producto = productos[productos["id_producto"] == id_producto] if not productos.empty else productos
    if producto.empty:
        return False, "Producto no encontrado."
    costo_fijo = _numero(producto.iloc[0], "costo_fijo_asignado")

    # Calculamos cuanto aporta cada unidad vendida.
    ok, margen_contribucion = calcular_margen_contribucion_producto(id_producto)
    if not ok:
        return False, margen_contribucion

    # Si cada unidad no aporta nada, no existe punto de equilibrio positivo.
    if float(margen_contribucion) <= 0:
        return False, "Margen de contribucion no positivo."

    # Punto de equilibrio = costo fijo / aporte por unidad.
    return True, costo_fijo / float(margen_contribucion)
