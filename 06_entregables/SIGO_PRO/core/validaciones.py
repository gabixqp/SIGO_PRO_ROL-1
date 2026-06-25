"""Validaciones reutilizables para formularios y reglas de negocio."""

import pandas as pd


def validar_texto_obligatorio(valor, nombre_campo: str) -> tuple[bool, str]:
    """Valida que un campo de texto tenga algun contenido real."""
    # Si el valor no existe o queda vacio despues de quitar espacios, no sirve.
    if valor is None or str(valor).strip() == "":
        # Devolvemos False para indicar error y un mensaje para mostrar al usuario.
        return False, f"{nombre_campo} es obligatorio."

    # Si llegamos aqui, el campo tiene texto.
    return True, "OK"


def validar_numero_no_negativo(valor, nombre_campo: str) -> tuple[bool, str]:
    """Valida que el valor sea numerico y mayor o igual que cero."""
    try:
        # Intentamos convertir el valor a numero decimal.
        numero = float(valor)
    except (TypeError, ValueError):
        # Si no se puede convertir, avisamos que debe ser numerico.
        return False, f"{nombre_campo} debe ser numerico."

    # En este sistema no se aceptan cantidades, costos o stocks negativos.
    if numero < 0:
        return False, f"{nombre_campo} no puede ser negativo."

    # Si es numero y no es negativo, pasa la validacion.
    return True, "OK"


def validar_fecha(fecha) -> tuple[bool, str]:
    """Valida que una fecha exista y Pandas pueda interpretarla."""
    # pd.isna detecta si la fecha esta vacia.
    if pd.isna(fecha):
        return False, "La fecha es obligatoria."
    try:
        # Intentamos convertir el valor recibido a una fecha entendible por Pandas.
        pd.to_datetime(fecha)
    except Exception:
        # Si Pandas no puede convertirla, la fecha no es valida.
        return False, "La fecha no es valida."

    # Si no hubo error, la fecha es usable.
    return True, "OK"


def validar_estado(valor, estados_permitidos: list[str]) -> tuple[bool, str]:
    """Valida que un estado pertenezca a la lista permitida."""
    # Comparamos el valor recibido contra la lista de estados aceptados.
    if valor not in estados_permitidos:
        # join convierte la lista de estados en texto separado por comas.
        return False, f"Estado no permitido. Usa: {', '.join(estados_permitidos)}."

    # Si el estado esta en la lista, es valido.
    return True, "OK"


def validar_columnas(df: pd.DataFrame, columnas_requeridas: list[str]) -> tuple[bool, str]:
    """Comprueba que un DataFrame traiga todas las columnas necesarias."""
    # Revisamos cada columna requerida y guardamos las que no esten en la tabla.
    faltantes = [col for col in columnas_requeridas if col not in df.columns]

    # Si falta al menos una columna, devolvemos error.
    if faltantes:
        # El mensaje enumera exactamente que columnas faltan.
        return False, f"Faltan columnas: {', '.join(faltantes)}."

    # Si no falta ninguna columna, la estructura esta correcta.
    return True, "OK"
