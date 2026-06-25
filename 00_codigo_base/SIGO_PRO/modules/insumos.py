"""Operaciones de negocio para insumos y materias primas."""

import pandas as pd

from config import COLUMNAS_CSV
from core.limpieza import convertir_numericos, normalizar_texto
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_numero_no_negativo, validar_texto_obligatorio


ARCHIVO = "insumos.csv"


def listar_insumos() -> pd.DataFrame:
    """Carga insumos y convierte sus campos numericos principales."""
    # stock, costo y merma deben ser numeros para que inventario y costos funcionen.
    return convertir_numericos(cargar_csv(ARCHIVO), ["stock_actual", "stock_minimo", "costo_unitario", "merma_pct"])


def registrar_insumo(nombre, unidad, stock_actual, stock_minimo, costo_unitario, merma_pct) -> tuple[bool, str]:
    """Valida y registra un insumo con stock, costo y merma."""
    # Nombre y unidad son textos obligatorios.
    for valor, campo in [(nombre, "Nombre"), (unidad, "Unidad")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # Stock, costo y merma no pueden ser negativos.
    for valor, campo in [(stock_actual, "Stock actual"), (stock_minimo, "Stock minimo"), (costo_unitario, "Costo unitario"), (merma_pct, "Merma")]:
        ok, msg = validar_numero_no_negativo(valor, campo)
        if not ok:
            return ok, msg

    # Cargamos insumos actuales para agregar uno nuevo.
    df = listar_insumos()
    if df.empty:
        # Si el CSV esta vacio, creamos una tabla con las columnas obligatorias.
        df = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO])

    # Construimos la nueva fila con ID automatico.
    fila = {
        "id_insumo": nuevo_id(df, "id_insumo", "INS"),
        "nombre": normalizar_texto(nombre),
        "unidad": normalizar_texto(unidad),
        "stock_actual": float(stock_actual),
        "stock_minimo": float(stock_minimo),
        "costo_unitario": float(costo_unitario),
        "merma_pct": float(merma_pct),
    }
    # Pegamos la nueva fila al final y guardamos.
    guardar_csv(pd.concat([df, pd.DataFrame([fila])], ignore_index=True), ARCHIVO)
    return True, "Insumo registrado."


def actualizar_insumo(id_insumo, nombre, unidad, stock_actual, stock_minimo, costo_unitario, merma_pct) -> tuple[bool, str]:
    """Actualiza los datos operativos de un insumo existente."""
    # Cargamos todos los insumos.
    df = listar_insumos()
    if df.empty or "id_insumo" not in df.columns:
        return False, "No hay insumos disponibles."

    # Buscamos el insumo por ID.
    idx = df.index[df["id_insumo"] == id_insumo]
    if idx.empty:
        return False, "Insumo no encontrado."

    # Validamos textos.
    for valor, campo in [(nombre, "Nombre"), (unidad, "Unidad")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # Validamos numeros.
    for valor, campo in [(stock_actual, "Stock actual"), (stock_minimo, "Stock minimo"), (costo_unitario, "Costo unitario"), (merma_pct, "Merma")]:
        ok, msg = validar_numero_no_negativo(valor, campo)
        if not ok:
            return ok, msg

    # Reemplazamos los valores de la fila encontrada.
    df.loc[idx[0], ["nombre", "unidad", "stock_actual", "stock_minimo", "costo_unitario", "merma_pct"]] = [
        normalizar_texto(nombre),
        normalizar_texto(unidad),
        float(stock_actual),
        float(stock_minimo),
        float(costo_unitario),
        float(merma_pct),
    ]
    # Guardamos cambios en el CSV.
    guardar_csv(df, ARCHIVO)
    return True, "Insumo actualizado."


def eliminar_insumo(id_insumo) -> tuple[bool, str]:
    """Elimina un insumo del CSV si el ID existe."""
    # Cargamos insumos.
    df = listar_insumos()
    if df.empty or "id_insumo" not in df.columns:
        return False, "No hay insumos disponibles."

    # Creamos una tabla sin el insumo elegido.
    filtrado = df[df["id_insumo"] != id_insumo].copy()
    if len(filtrado) == len(df):
        return False, "Insumo no encontrado."

    # Guardamos la tabla filtrada.
    guardar_csv(filtrado, ARCHIVO)
    return True, "Insumo eliminado."


def obtener_insumos_activos() -> pd.DataFrame:
    """Devuelve insumos disponibles para formularios y recetas."""
    # Por ahora no hay estado de insumo; todos los cargados se consideran activos.
    return listar_insumos()


def obtener_insumos_criticos() -> pd.DataFrame:
    """Lista insumos cuyo stock actual esta en o debajo del minimo."""
    # Cargamos insumos con numeros corregidos.
    df = listar_insumos()
    if df.empty or not {"stock_actual", "stock_minimo"}.issubset(df.columns):
        return pd.DataFrame()

    # Filtramos los que necesitan reposicion.
    return df[df["stock_actual"] <= df["stock_minimo"]].copy()


def descontar_insumo(id_insumo, cantidad) -> tuple[bool, str]:
    """Resta stock de un insumo validando que alcance el inventario."""
    # Cargamos insumos.
    df = listar_insumos()
    if df.empty or "id_insumo" not in df.columns:
        return False, "No hay insumos disponibles."

    # Buscamos el insumo por ID.
    idx = df.index[df["id_insumo"] == id_insumo]
    if idx.empty:
        return False, "Insumo no encontrado."

    # Tomamos la posicion exacta dentro de la tabla.
    pos = idx[0]

    # Si el stock disponible es menor que lo que se quiere descontar, no permitimos.
    if float(df.loc[pos, "stock_actual"]) < float(cantidad):
        return False, "Stock insuficiente del insumo."

    # Restamos la cantidad solicitada.
    df.loc[pos, "stock_actual"] = float(df.loc[pos, "stock_actual"]) - float(cantidad)

    # Guardamos el nuevo stock.
    guardar_csv(df, ARCHIVO)
    return True, "Insumo descontado."


def aumentar_insumo(id_insumo, cantidad) -> tuple[bool, str]:
    """Suma stock a un insumo existente."""
    # Cargamos insumos.
    df = listar_insumos()
    if df.empty or "id_insumo" not in df.columns:
        return False, "No hay insumos disponibles."

    # Buscamos el insumo por ID.
    idx = df.index[df["id_insumo"] == id_insumo]
    if idx.empty:
        return False, "Insumo no encontrado."

    # Sumamos la cantidad al stock actual.
    df.loc[idx[0], "stock_actual"] = float(df.loc[idx[0], "stock_actual"]) + float(cantidad)

    # Guardamos el nuevo stock.
    guardar_csv(df, ARCHIVO)
    return True, "Insumo aumentado."
