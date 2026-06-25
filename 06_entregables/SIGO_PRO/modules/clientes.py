"""Operaciones de negocio para clientes."""

from datetime import date

import pandas as pd

from config import COLUMNAS_CSV
from core.limpieza import normalizar_texto
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_texto_obligatorio


ARCHIVO = "clientes.csv"


def listar_clientes() -> pd.DataFrame:
    """Devuelve todos los clientes registrados en data/clientes.csv."""
    # cargar_csv abre data/clientes.csv y lo transforma en una tabla.
    return cargar_csv(ARCHIVO)


def registrar_cliente(nombre, tipo, canal, contacto, telefono) -> tuple[bool, str]:
    """Valida datos minimos, crea un ID y agrega un cliente activo."""
    # Solo estos tres campos son obligatorios para poder operar.
    for valor, campo in [(nombre, "Nombre"), (tipo, "Tipo"), (canal, "Canal")]:
        # Revisamos campo por campo que no venga vacio.
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            # Si un campo falla, detenemos el registro y devolvemos el mensaje.
            return ok, msg

    # Cargamos los clientes actuales para agregar el nuevo al final.
    df = listar_clientes()
    if df.empty:
        # Si no habia datos, creamos una tabla nueva con las columnas oficiales.
        df = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO])

    # Los datos de texto se normalizan para evitar espacios y valores nulos.
    fila = {
        "id_cliente": nuevo_id(df, "id_cliente", "CLI"),
        "nombre": normalizar_texto(nombre),
        "tipo": normalizar_texto(tipo),
        "canal": normalizar_texto(canal),
        "contacto": normalizar_texto(contacto),
        "telefono": normalizar_texto(telefono),
        "estado": "activo",
        "fecha_registro": date.today().isoformat(),
    }
    # pd.concat pega la tabla anterior con una tabla de una sola fila nueva.
    # ignore_index=True vuelve a numerar las filas.
    guardar_csv(pd.concat([df, pd.DataFrame([fila])], ignore_index=True), ARCHIVO)
    return True, "Cliente registrado."


def actualizar_cliente(id_cliente, nombre, tipo, canal, contacto, telefono, estado) -> tuple[bool, str]:
    """Actualiza los datos principales de un cliente existente."""
    # Cargamos todos los clientes para encontrar el que se quiere editar.
    df = listar_clientes()
    if df.empty or "id_cliente" not in df.columns:
        return False, "No hay clientes disponibles."

    # Buscamos las filas cuyo id_cliente sea igual al ID recibido.
    idx = df.index[df["id_cliente"] == id_cliente]
    if idx.empty:
        return False, "Cliente no encontrado."

    # Validamos que los campos importantes no queden vacios.
    for valor, campo in [(nombre, "Nombre"), (tipo, "Tipo"), (canal, "Canal"), (estado, "Estado")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # idx puede contener indices; tomamos el primero porque el ID deberia ser unico.
    pos = idx[0]

    # Reemplazamos varias columnas de la fila encontrada en una sola operacion.
    df.loc[pos, ["nombre", "tipo", "canal", "contacto", "telefono", "estado"]] = [
        normalizar_texto(nombre),
        normalizar_texto(tipo),
        normalizar_texto(canal),
        normalizar_texto(contacto),
        normalizar_texto(telefono),
        normalizar_texto(estado),
    ]
    # Guardamos la tabla completa con el cliente ya modificado.
    guardar_csv(df, ARCHIVO)
    return True, "Cliente actualizado."


def eliminar_cliente(id_cliente) -> tuple[bool, str]:
    """Elimina del CSV el cliente indicado por su ID."""
    # Cargamos la tabla completa.
    df = listar_clientes()
    if df.empty or "id_cliente" not in df.columns:
        return False, "No hay clientes disponibles."

    # Creamos una nueva tabla con todos excepto el cliente que queremos eliminar.
    filtrado = df[df["id_cliente"] != id_cliente].copy()

    # Si el largo no cambio, significa que no se encontro ese ID.
    if len(filtrado) == len(df):
        return False, "Cliente no encontrado."

    # Guardamos la tabla filtrada.
    guardar_csv(filtrado, ARCHIVO)
    return True, "Cliente eliminado."


def obtener_clientes_activos() -> pd.DataFrame:
    """Devuelve solo clientes marcados como activos."""
    # Cargamos todos los clientes.
    df = listar_clientes()
    if df.empty or "estado" not in df.columns:
        return pd.DataFrame()

    # Convertimos estado a texto, lo pasamos a minuscula y comparamos con "activo".
    return df[df["estado"].astype(str).str.lower() == "activo"].copy()
