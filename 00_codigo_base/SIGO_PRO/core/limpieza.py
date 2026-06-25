"""Funciones pequeñas para limpiar datos antes de usarlos."""

import pandas as pd


def limpiar_fechas(df: pd.DataFrame, columnas_fecha: list[str]) -> pd.DataFrame:
    """Convierte columnas indicadas a fechas; valores invalidos quedan como NaT."""
    # Hacemos una copia para no modificar directamente la tabla original que nos pasaron.
    limpio = df.copy()

    # Recorremos una por una las columnas que deberian contener fechas.
    for columna in columnas_fecha:
        # Solo intentamos convertir la columna si realmente existe en la tabla.
        if columna in limpio.columns:
            # Pandas intenta transformar el texto a fecha.
            # Si no puede entender una fecha, pone NaT, que significa "fecha vacia/invalida".
            limpio[columna] = pd.to_datetime(limpio[columna], errors="coerce")

    # Devolvemos la copia ya corregida.
    return limpio


def convertir_numericos(df: pd.DataFrame, columnas_numericas: list[str]) -> pd.DataFrame:
    """Convierte columnas indicadas a numeros y reemplaza errores por cero."""
    # Copiamos la tabla para evitar cambiar la tabla original por accidente.
    limpio = df.copy()

    # Recorremos cada nombre de columna que deberia ser numerica.
    for columna in columnas_numericas:
        # Si la columna no existe, no hacemos nada; asi evitamos errores.
        if columna in limpio.columns:
            # pd.to_numeric convierte textos como "10" o "10.5" en numeros reales.
            # errors="coerce" convierte valores incorrectos en NaN.
            # fillna(0) reemplaza esos NaN por 0 para que los calculos no fallen.
            limpio[columna] = pd.to_numeric(limpio[columna], errors="coerce").fillna(0)

    # Retornamos la tabla con las columnas convertidas.
    return limpio


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas repetidas y recompone el indice desde cero."""
    # drop_duplicates quita filas exactamente iguales.
    # reset_index(drop=True) vuelve a numerar las filas desde 0.
    return df.drop_duplicates().reset_index(drop=True)


def normalizar_texto(valor) -> str:
    """Devuelve texto limpio; None/NaN se convierten en cadena vacia."""
    # None significa "no hay valor" en Python.
    # pd.isna detecta valores vacios de Pandas, como NaN.
    if valor is None or pd.isna(valor):
        # Si no hay texto real, devolvemos texto vacio para no romper formularios.
        return ""

    # Convertimos cualquier valor a texto y quitamos espacios al inicio y al final.
    return str(valor).strip()
