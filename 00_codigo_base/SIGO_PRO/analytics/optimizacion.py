"""Sugerencias basicas de optimizacion operativa."""

import pandas as pd

from modules.pedidos import listar_detalle_pedidos
from modules.productos import listar_productos


def sugerir_produccion_preventiva() -> pd.DataFrame:
    """Sugiere producir productos con alta demanda y stock cercano al minimo."""
    # El detalle de pedidos muestra demanda historica por producto.
    detalle = listar_detalle_pedidos()

    # Productos muestra stock actual y stock minimo.
    productos = listar_productos()
    if detalle.empty or productos.empty:
        return pd.DataFrame()

    # Sin id_producto y cantidad no podemos calcular demanda.
    if not {"id_producto", "cantidad"}.issubset(detalle.columns):
        return pd.DataFrame()

    # Sumamos cantidades vendidas por producto.
    demanda = detalle.groupby("id_producto", as_index=False)["cantidad"].sum().rename(columns={"cantidad": "demanda"})

    # Pegamos demanda a la tabla de productos.
    df = productos.merge(demanda, on="id_producto", how="left")

    # Productos sin ventas quedan con demanda 0.
    df["demanda"] = df["demanda"].fillna(0)

    # Necesitamos stock minimo y stock actual para recomendar produccion.
    if "stock_minimo" not in df.columns or "stock_actual" not in df.columns:
        return pd.DataFrame()
    # El percentil 75 toma los productos del grupo de mayor demanda historica.
    umbral_demanda = df["demanda"].quantile(0.75) if len(df) > 1 else df["demanda"].max()

    # Recomienda productos con demanda alta y stock no muy por encima del minimo.
    return df[(df["demanda"] >= umbral_demanda) & (df["stock_actual"] <= df["stock_minimo"] * 1.5)].copy()
