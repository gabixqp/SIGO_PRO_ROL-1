"""Relacion entre productos terminados e insumos que los componen."""

import pandas as pd

from config import COLUMNAS_CSV
from core.limpieza import convertir_numericos
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_numero_no_negativo, validar_texto_obligatorio
from modules.insumos import listar_insumos
from modules.productos import listar_productos


ARCHIVO = "recetas.csv"


def listar_recetas() -> pd.DataFrame:
    """Carga recetas y convierte la cantidad de insumo a numero."""
    # Cada receta dice cuanto insumo necesita un producto.
    # La columna cantidad debe ser numerica para calcular costos y produccion.
    return convertir_numericos(cargar_csv(ARCHIVO), ["cantidad"])


def registrar_receta(id_producto, id_insumo, cantidad) -> tuple[bool, str]:
    """Agrega una linea de receta: producto + insumo + cantidad requerida."""
    # Producto e insumo deben existir como texto/ID, no pueden venir vacios.
    for valor, campo in [(id_producto, "Producto"), (id_insumo, "Insumo")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # La cantidad de insumo debe ser un numero no negativo.
    ok, msg = validar_numero_no_negativo(cantidad, "Cantidad")
    if not ok:
        return ok, msg

    # Cargamos recetas existentes para agregar una linea nueva.
    df = listar_recetas()
    if df.empty:
        # Si no hay recetas, creamos una tabla vacia con columnas oficiales.
        df = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO])

    # Armamos una fila: un producto usa cierta cantidad de un insumo.
    fila = {
        "id_receta": nuevo_id(df, "id_receta", "REC"),
        "id_producto": id_producto,
        "id_insumo": id_insumo,
        "cantidad": float(cantidad),
    }
    # Agregamos la fila nueva al CSV de recetas.
    guardar_csv(pd.concat([df, pd.DataFrame([fila])], ignore_index=True), ARCHIVO)
    return True, "Receta registrada."


def obtener_receta_producto(id_producto) -> pd.DataFrame:
    """Devuelve todas las lineas de receta de un producto."""
    # Cargamos todas las recetas.
    df = listar_recetas()
    if df.empty or "id_producto" not in df.columns:
        return pd.DataFrame()

    # Filtramos solo las filas que pertenecen al producto pedido.
    return df[df["id_producto"] == id_producto].copy()


def listar_recetas_enriquecidas() -> pd.DataFrame:
    """Devuelve recetas con nombres de producto e insumo para lectura humana."""
    # Partimos de la tabla base de recetas.
    recetas = listar_recetas()
    if recetas.empty:
        return recetas

    # Cargamos tablas maestras para poder reemplazar IDs por nombres.
    productos = listar_productos()
    insumos = listar_insumos()
    if not productos.empty and {"id_producto", "nombre"}.issubset(productos.columns):
        # Agrega nombre del producto sin perder recetas que aun no tengan match.
        recetas = recetas.merge(
            productos[["id_producto", "nombre"]].rename(columns={"nombre": "producto"}),
            on="id_producto",
            how="left",
        )
    if not insumos.empty and {"id_insumo", "nombre"}.issubset(insumos.columns):
        # Agrega nombre del insumo para que la tabla no muestre solo IDs.
        recetas = recetas.merge(
            insumos[["id_insumo", "nombre"]].rename(columns={"nombre": "insumo"}),
            on="id_insumo",
            how="left",
        )
    # Devolvemos recetas con columnas extra "producto" e "insumo" si se pudieron unir.
    return recetas
