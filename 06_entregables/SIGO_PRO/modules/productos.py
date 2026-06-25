"""Operaciones de negocio para productos terminados."""

import pandas as pd

from config import COLUMNAS_CSV
from core.limpieza import convertir_numericos, normalizar_texto
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_numero_no_negativo, validar_texto_obligatorio


ARCHIVO = "productos.csv"


def listar_productos() -> pd.DataFrame:
    """Carga productos y asegura que los campos numericos sean numeros."""
    # Primero se carga el CSV y luego se convierten precio y stocks a numeros.
    return convertir_numericos(cargar_csv(ARCHIVO), ["precio_venta", "stock_actual", "stock_minimo"])


def registrar_producto(nombre, categoria, unidad, precio_venta, stock_actual, stock_minimo) -> tuple[bool, str]:
    """Valida y agrega un producto nuevo al inventario."""
    # Nombre, categoria y unidad son textos obligatorios.
    for valor, campo in [(nombre, "Nombre"), (categoria, "Categoria"), (unidad, "Unidad")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # Precio y stocks deben ser numeros mayores o iguales que cero.
    for valor, campo in [(precio_venta, "Precio de venta"), (stock_actual, "Stock actual"), (stock_minimo, "Stock minimo")]:
        ok, msg = validar_numero_no_negativo(valor, campo)
        if not ok:
            return ok, msg

    # Cargamos productos existentes para agregar el nuevo.
    df = listar_productos()
    if df.empty:
        # Si no hay productos, arrancamos con las columnas configuradas.
        df = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO])

    # Armamos la fila nueva con ID automatico y valores limpios.
    fila = {
        "id_producto": nuevo_id(df, "id_producto", "PRO"),
        "nombre": normalizar_texto(nombre),
        "categoria": normalizar_texto(categoria),
        "precio_venta": float(precio_venta),
        "stock_actual": float(stock_actual),
        "stock_minimo": float(stock_minimo),
        "unidad": normalizar_texto(unidad),
    }
    # Agregamos la fila nueva y guardamos el CSV.
    guardar_csv(pd.concat([df, pd.DataFrame([fila])], ignore_index=True), ARCHIVO)
    return True, "Producto registrado."


def actualizar_producto(id_producto, nombre, categoria, unidad, precio_venta, stock_actual, stock_minimo) -> tuple[bool, str]:
    """Actualiza nombre, categoria, unidad, precio y stocks de un producto."""
    # Cargamos productos existentes.
    df = listar_productos()
    if df.empty or "id_producto" not in df.columns:
        return False, "No hay productos disponibles."

    # Buscamos el producto exacto por su ID.
    idx = df.index[df["id_producto"] == id_producto]
    if idx.empty:
        return False, "Producto no encontrado."

    # Validamos textos obligatorios.
    for valor, campo in [(nombre, "Nombre"), (categoria, "Categoria"), (unidad, "Unidad")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # Validamos numeros obligatorios.
    for valor, campo in [(precio_venta, "Precio de venta"), (stock_actual, "Stock actual"), (stock_minimo, "Stock minimo")]:
        ok, msg = validar_numero_no_negativo(valor, campo)
        if not ok:
            return ok, msg

    # Reemplazamos los datos del producto encontrado.
    df.loc[idx[0], ["nombre", "categoria", "unidad", "precio_venta", "stock_actual", "stock_minimo"]] = [
        normalizar_texto(nombre),
        normalizar_texto(categoria),
        normalizar_texto(unidad),
        float(precio_venta),
        float(stock_actual),
        float(stock_minimo),
    ]
    # Guardamos el CSV actualizado.
    guardar_csv(df, ARCHIVO)
    return True, "Producto actualizado."


def eliminar_producto(id_producto) -> tuple[bool, str]:
    """Elimina un producto si el ID existe."""
    # Cargamos productos para poder filtrar uno.
    df = listar_productos()
    if df.empty or "id_producto" not in df.columns:
        return False, "No hay productos disponibles."

    # Dejamos todas las filas excepto la que tiene el ID recibido.
    filtrado = df[df["id_producto"] != id_producto].copy()

    # Si no cambio la cantidad de filas, no existia ese producto.
    if len(filtrado) == len(df):
        return False, "Producto no encontrado."

    # Guardamos la tabla sin ese producto.
    guardar_csv(filtrado, ARCHIVO)
    return True, "Producto eliminado."


def obtener_productos_activos() -> pd.DataFrame:
    """Devuelve productos disponibles para formularios operativos."""
    # Por ahora no hay columna de estado; todos los productos cargados se consideran activos.
    return listar_productos()


def obtener_productos_criticos() -> pd.DataFrame:
    """Lista productos cuyo stock actual esta en o debajo del minimo."""
    # Cargamos productos con columnas numericas ya convertidas.
    df = listar_productos()
    if df.empty or not {"stock_actual", "stock_minimo"}.issubset(df.columns):
        return pd.DataFrame()

    # Comparamos stock_actual contra stock_minimo y devolvemos solo los criticos.
    return df[df["stock_actual"] <= df["stock_minimo"]].copy()
