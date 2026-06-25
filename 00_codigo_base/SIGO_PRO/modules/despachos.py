"""Registro y seguimiento de despachos."""

import pandas as pd

from config import COLUMNAS_CSV
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_estado, validar_texto_obligatorio
from modules.pedidos import listar_pedidos


ARCHIVO = "despachos.csv"
ESTADOS = ["programado", "en_ruta", "entregado", "retrasado", "cancelado"]


def listar_despachos() -> pd.DataFrame:
    """Devuelve todos los despachos registrados."""
    # Lee data/despachos.csv y lo entrega como tabla.
    return cargar_csv(ARCHIVO)


def registrar_despacho(id_pedido, fecha_programada, fecha_entrega, estado) -> tuple[bool, str]:
    """Registra un despacho y marca el pedido como entregado si corresponde."""
    # Todo despacho debe estar relacionado con un pedido.
    ok, msg = validar_texto_obligatorio(id_pedido, "Pedido")
    if not ok:
        return ok, msg

    # El estado debe ser uno de los permitidos en la lista ESTADOS.
    ok, msg = validar_estado(estado, ESTADOS)
    if not ok:
        return ok, msg

    sugerencia = ""
    # La app permite guardar, pero avisa si la fecha indica retraso.
    # pd.to_datetime convierte las fechas de texto a fechas comparables.
    if fecha_entrega and fecha_programada and pd.to_datetime(fecha_entrega) > pd.to_datetime(fecha_programada) and estado != "retrasado":
        sugerencia = " La fecha de entrega supera la programada; considera usar estado retrasado."

    # Cargamos despachos existentes.
    despachos = listar_despachos()
    if despachos.empty:
        # Si no hay despachos, creamos tabla con columnas oficiales.
        despachos = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO])

    # Armamos la fila del nuevo despacho.
    fila = {
        "id_despacho": nuevo_id(despachos, "id_despacho", "DSP"),
        "id_pedido": id_pedido,
        "fecha_programada": fecha_programada,
        "fecha_entrega": fecha_entrega,
        "estado": estado,
    }
    # Agregamos el despacho al CSV.
    guardar_csv(pd.concat([despachos, pd.DataFrame([fila])], ignore_index=True), ARCHIVO)

    if estado == "entregado":
        # Mantiene sincronizado el estado comercial del pedido con el despacho.
        # Si el despacho fue entregado, tambien actualizamos el pedido.
        pedidos = listar_pedidos()
        if not pedidos.empty and "id_pedido" in pedidos.columns:
            # Buscamos el pedido correspondiente.
            idx = pedidos.index[pedidos["id_pedido"] == id_pedido]
            if not idx.empty:
                # Cambiamos su estado y guardamos pedidos.csv.
                pedidos.loc[idx[0], "estado"] = "entregado"
                guardar_csv(pedidos, "pedidos.csv")
    return True, "Despacho registrado." + sugerencia
