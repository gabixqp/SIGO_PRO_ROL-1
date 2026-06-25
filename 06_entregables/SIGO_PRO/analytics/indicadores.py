"""Indicadores resumidos para tableros y reportes."""

import numpy as np
import pandas as pd

from modules.clientes import listar_clientes
try:
    from modules.costos import calcular_margen_contribucion_producto, calcular_punto_equilibrio_producto
except ImportError:
    # Permite que la pantalla cargue aunque el modulo de costos no este listo.
    def calcular_margen_contribucion_producto(_id_producto):
        return False, "Indicador financiero no disponible."

    def calcular_punto_equilibrio_producto(_id_producto):
        return False, "Indicador financiero no disponible."
from modules.despachos import listar_despachos
from modules.insumos import listar_insumos
from modules.pedidos import listar_detalle_pedidos, listar_pedidos
from modules.productos import listar_productos, obtener_productos_criticos


def calcular_indicadores_generales() -> dict:
    """Calcula las metricas principales que se muestran en el inicio."""
    # Cargamos las tablas base necesarias para los indicadores.
    pedidos = listar_pedidos()
    clientes = listar_clientes()
    productos = listar_productos()
    despachos = listar_despachos()

    # Cantidad de pedidos = numero de filas en pedidos.csv.
    total_pedidos = len(pedidos)

    # Ventas = suma de la columna total; si no existe, usamos 0.
    ventas = float(pedidos["total"].sum()) if not pedidos.empty and "total" in pedidos.columns else 0.0

    # Empezamos con 0% de retrasos y solo calculamos si hay despachos.
    retrasados = 0.0
    if not despachos.empty and "estado" in despachos.columns:
        # Promedio booleano: True vale 1, False vale 0; multiplicado por 100 da %.
        retrasados = float(np.mean(despachos["estado"].astype(str).eq("retrasado")) * 100)

    # Devolvemos un diccionario porque es facil acceder por nombre de indicador.
    return {
        "total_pedidos": total_pedidos,
        "ventas_totales": ventas,
        "clientes": len(clientes),
        "productos": len(productos),
        "productos_criticos": len(obtener_productos_criticos()),
        "porcentaje_despachos_retrasados": retrasados,
    }


def calcular_ventas_por_producto() -> pd.DataFrame:
    """Agrupa subtotales de detalle para saber que productos venden mas."""
    # El detalle tiene el subtotal de cada producto vendido.
    detalle = listar_detalle_pedidos()

    # Productos sirve para agregar el nombre del producto.
    productos = listar_productos()

    # Si falta detalle o columnas clave, no se puede calcular.
    if detalle.empty or not {"id_producto", "subtotal"}.issubset(detalle.columns):
        return pd.DataFrame()

    # groupby suma subtotal por cada id_producto.
    ventas = detalle.groupby("id_producto", as_index=False)["subtotal"].sum()

    # Si tenemos nombres de producto, los pegamos a la tabla de ventas.
    if not productos.empty and {"id_producto", "nombre"}.issubset(productos.columns):
        ventas = ventas.merge(productos[["id_producto", "nombre"]], on="id_producto", how="left")

    # Ordenamos de mayor a menor venta.
    return ventas.sort_values("subtotal", ascending=False)


def calcular_pedidos_por_cliente() -> pd.DataFrame:
    """Agrupa cantidad de pedidos e importe total por cliente."""
    # Pedidos tiene id_cliente y total de cada pedido.
    pedidos = listar_pedidos()

    # Clientes sirve para mostrar nombres en vez de solo IDs.
    clientes = listar_clientes()
    if pedidos.empty or "id_cliente" not in pedidos.columns:
        return pd.DataFrame()

    # agg calcula dos cosas: cantidad de pedidos y suma total.
    resumen = pedidos.groupby("id_cliente", as_index=False).agg(pedidos=("id_pedido", "count"), total=("total", "sum"))

    # Agregamos nombre del cliente si esta disponible.
    if not clientes.empty and {"id_cliente", "nombre"}.issubset(clientes.columns):
        resumen = resumen.merge(clientes[["id_cliente", "nombre"]], on="id_cliente", how="left")

    # Ordenamos por importe acumulado, de mayor a menor.
    return resumen.sort_values("total", ascending=False)


def calcular_pedidos_por_estado() -> pd.DataFrame:
    """Cuenta pedidos por estado operativo/comercial."""
    # Cargamos pedidos.
    pedidos = listar_pedidos()
    if pedidos.empty or "estado" not in pedidos.columns:
        return pd.DataFrame()

    # groupby cuenta cuantas filas hay por cada estado.
    return pedidos.groupby("estado", as_index=False).size().rename(columns={"size": "cantidad"})


def calcular_indicadores_financieros_productos() -> pd.DataFrame:
    """Calcula margen de contribucion y punto de equilibrio por producto."""
    # Cargamos productos para recorrerlos uno por uno.
    productos = listar_productos()
    if productos.empty or "id_producto" not in productos.columns:
        return pd.DataFrame()

    # Lista donde se acumula una fila de indicador por producto.
    filas = []
    for _, producto in productos.iterrows():
        # Leemos el ID del producto actual.
        id_producto = producto["id_producto"]

        # Calculamos margen de contribucion con el modulo de costos.
        ok_mc, margen_contribucion = calcular_margen_contribucion_producto(id_producto)

        # Calculamos punto de equilibrio con el modulo de costos.
        ok_pe, punto_equilibrio = calcular_punto_equilibrio_producto(id_producto)

        # Si algun calculo falla, ponemos NaN para indicar dato no disponible.
        filas.append(
            {
                "id_producto": id_producto,
                "producto": producto.get("nombre", id_producto),
                "precio_venta": producto.get("precio_venta", 0),
                "margen_contribucion": float(margen_contribucion) if ok_mc else np.nan,
                "punto_equilibrio_unidades": float(punto_equilibrio) if ok_pe else np.nan,
            }
        )

    # Convertimos la lista en tabla para mostrar en Streamlit.
    return pd.DataFrame(filas)


def calcular_rotacion_inventarios() -> pd.DataFrame:
    """Prepara valor de inventario; rotacion queda pendiente sin consumos historicos."""
    # Cargamos insumos porque el inventario se mide sobre materias primas.
    insumos = listar_insumos()
    if insumos.empty:
        return pd.DataFrame()

    # Trabajamos sobre una copia para no alterar la tabla original.
    df = insumos.copy()
    if "valor_inventario" not in df.columns:
        # Si no vino valorizado desde el CSV, se estima costo_unitario * stock.
        costo = pd.to_numeric(df.get("costo_unitario", 0), errors="coerce").fillna(0)
        stock = pd.to_numeric(df.get("stock_actual", 0), errors="coerce").fillna(0)
        df["valor_inventario"] = costo * stock

    # Todavia no hay historico de consumos, por eso se deja vacio.
    df["rotacion_inventario"] = np.nan

    # Devolvemos solo columnas utiles para el reporte.
    return df[["id_insumo", "nombre", "stock_actual", "valor_inventario", "rotacion_inventario"]]
