"""Utilidades para leer y escribir archivos de datos.

La aplicacion usa CSV como almacenamiento simple. Este modulo concentra el
acceso a disco para que las pantallas y reglas de negocio no repitan rutas,
validaciones basicas ni manejo de errores.
"""

import json
from pathlib import Path

import pandas as pd

from config import COLUMNAS_CSV, DATA_DIR


def _resolver_ruta(nombre_archivo: str) -> Path:
    """Convierte un nombre de archivo en una ruta dentro de data/."""
    # DATA_DIR es la carpeta data/. Al usar / unimos carpeta + archivo.
    return DATA_DIR / nombre_archivo


def existe_archivo(nombre_archivo: str) -> bool:
    """Indica si un archivo esperado ya existe en la carpeta data/."""
    # Primero calculamos la ruta completa y luego preguntamos si es un archivo.
    return _resolver_ruta(nombre_archivo).is_file()


def cargar_csv(nombre_archivo: str) -> pd.DataFrame:
    """Carga un CSV y devuelve un DataFrame vacio si no existe o esta vacio."""
    # Convertimos el nombre simple, por ejemplo "clientes.csv", en ruta completa.
    ruta = _resolver_ruta(nombre_archivo)

    # Si el archivo no existe, devolvemos una tabla vacia para que la app no falle.
    if not ruta.exists():
        return pd.DataFrame()
    try:
        # read_csv lee el archivo CSV y lo convierte en una tabla de Pandas.
        return pd.read_csv(ruta)
    except pd.errors.EmptyDataError:
        # Si el CSV existe pero no tiene contenido, tambien devolvemos tabla vacia.
        return pd.DataFrame()
    except Exception as exc:
        # Cualquier otro error se vuelve un mensaje claro para saber que archivo fallo.
        raise RuntimeError(f"No se pudo cargar {nombre_archivo}: {exc}") from exc


def guardar_csv(df: pd.DataFrame, nombre_archivo: str) -> None:
    """Guarda un DataFrame en data/ creando la carpeta si hiciera falta."""
    # Calculamos donde debe guardarse el archivo.
    ruta = _resolver_ruta(nombre_archivo)

    # Creamos la carpeta data/ si todavia no existe.
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # Guardamos la tabla sin el indice automatico de Pandas.
    df.to_csv(ruta, index=False)


def cargar_json(nombre_archivo: str) -> dict:
    """Carga un JSON de configuracion y devuelve diccionario vacio si no existe."""
    # Calculamos la ruta completa del JSON.
    ruta = _resolver_ruta(nombre_archivo)

    # Si no existe, no es error: devolvemos configuracion vacia.
    if not ruta.exists():
        return {}
    try:
        # Abrimos el archivo en modo lectura usando UTF-8 para soportar acentos.
        with ruta.open("r", encoding="utf-8") as archivo:
            # json.load convierte el texto JSON en un diccionario de Python.
            return json.load(archivo)
    except json.JSONDecodeError as exc:
        # Si el JSON esta mal escrito, lanzamos un error entendible.
        raise RuntimeError(f"JSON invalido en {nombre_archivo}: {exc}") from exc


def guardar_json(data: dict, nombre_archivo: str) -> None:
    """Guarda un diccionario como JSON legible para humanos."""
    # Calculamos donde guardar el archivo.
    ruta = _resolver_ruta(nombre_archivo)

    # Creamos la carpeta data/ si no existe.
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # Abrimos el archivo en escritura. Si ya existe, se reemplaza.
    with ruta.open("w", encoding="utf-8") as archivo:
        # ensure_ascii=False conserva acentos; indent=2 lo deja facil de leer.
        json.dump(data, archivo, ensure_ascii=False, indent=2)


def nuevo_id(df: pd.DataFrame, columna_id: str, prefijo: str) -> str:
    """Genera IDs secuenciales tipo CLI001, PRO001, PED001, etc."""
    # Si no hay tabla o no existe la columna de IDs, arrancamos en 001.
    if df.empty or columna_id not in df.columns:
        return f"{prefijo}001"

    # Quita el prefijo, extrae el numero y calcula el siguiente correlativo.
    # Primero tomamos la columna de IDs, quitamos vacios y la tratamos como texto.
    serie = df[columna_id].dropna().astype(str)

    # Ejemplo: "CLI015" -> quitamos "CLI" -> "015" -> extraemos 15.
    numeros = (
        serie.str.replace(prefijo, "", regex=False)
        .str.extract(r"(\d+)", expand=False)
        .dropna()
        .astype(int)
    )

    # Si ya habia numeros, sumamos 1 al mayor; si no, empezamos en 1.
    siguiente = int(numeros.max()) + 1 if not numeros.empty else 1

    # :03d significa que el numero se muestra con 3 digitos: 1 -> 001.
    return f"{prefijo}{siguiente:03d}"


def validar_disponibilidad_archivo(nombre_archivo: str) -> tuple[bool, str]:
    """Verifica que el CSV exista y tenga sus columnas obligatorias."""
    # Primero verificamos existencia fisica del archivo.
    if not existe_archivo(nombre_archivo):
        return False, f"Falta el archivo data/{nombre_archivo}. Se conectara en una etapa posterior."

    # Si existe, lo cargamos para revisar su estructura.
    df = cargar_csv(nombre_archivo)

    # Buscamos en config.py cuales columnas son obligatorias para este archivo.
    columnas = COLUMNAS_CSV.get(nombre_archivo, [])

    # Guardamos cualquier columna obligatoria que no aparezca en el CSV.
    faltantes = [col for col in columnas if col not in df.columns]

    # Si faltan columnas, devolvemos detalle exacto para corregir el archivo.
    if faltantes:
        return False, f"El archivo {nombre_archivo} no contiene columnas requeridas: {', '.join(faltantes)}."

    # Si existe y tiene columnas correctas, esta listo para usar.
    return True, "Archivo disponible."
