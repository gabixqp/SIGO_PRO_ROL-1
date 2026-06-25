"""Ordenes de produccion y movimiento de inventario relacionado."""

import pandas as pd

from config import COLUMNAS_CSV
from core.limpieza import convertir_numericos
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_estado, validar_numero_no_negativo, validar_texto_obligatorio
from modules.insumos import listar_insumos
from modules.productos import listar_productos
from modules.recetas import obtener_receta_producto


ARCHIVO = "produccion.csv"


def listar_produccion() -> pd.DataFrame:
    """Carga ordenes de produccion y convierte cantidad a numero."""
    # Lee produccion.csv y garantiza que cantidad sea numerica.
    return convertir_numericos(cargar_csv(ARCHIVO), ["cantidad"])


def registrar_orden_produccion(id_producto, cantidad, fecha, estado) -> tuple[bool, str]:
    """Crea una orden y, si esta completada, consume insumos y aumenta producto."""
    # La orden debe indicar que producto se producira.
    ok, msg = validar_texto_obligatorio(id_producto, "Producto")
    if not ok:
        return ok, msg

    # La cantidad debe ser un numero valido.
    ok, msg = validar_numero_no_negativo(cantidad, "Cantidad")
    if not ok:
        return ok, msg

    # Solo se aceptan los estados definidos para produccion.
    ok, msg = validar_estado(estado, ["pendiente", "completada"])
    if not ok:
        return ok, msg

    # Convertimos cantidad a numero decimal para poder sumar/restar inventario.
    cantidad = float(cantidad)

    # Cargamos productos para verificar que el producto exista.
    productos = listar_productos()
    if productos.empty or "id_producto" not in productos.columns:
        return False, "No hay productos disponibles."

    # Buscamos la fila del producto que se va a fabricar.
    idx_producto = productos.index[productos["id_producto"] == id_producto]
    if idx_producto.empty:
        return False, "Producto no encontrado."

    # Cargamos insumos porque una orden completada puede descontarlos.
    insumos = listar_insumos()
    if estado == "completada":
        # Una orden completada debe tener receta para saber que insumos descontar.
        receta = obtener_receta_producto(id_producto)
        if receta.empty:
            return False, "El producto no tiene receta configurada."
        consumos = []
        for _, item in receta.iterrows():
            # Por cada linea de receta buscamos el insumo correspondiente.
            insumo = insumos[insumos["id_insumo"] == item["id_insumo"]]
            if insumo.empty:
                return False, f"Insumo {item['id_insumo']} no encontrado."

            # Leemos merma: porcentaje extra que se pierde o desperdicia.
            merma = float(insumo.iloc[0].get("merma_pct", 0))
            # La merma aumenta el consumo real sobre la cantidad teorica.
            consumo = cantidad * float(item["cantidad"]) * (1 + merma / 100)

            # Stock actual disponible de ese insumo.
            stock = float(insumo.iloc[0]["stock_actual"])
            if stock < consumo:
                return False, f"Stock insuficiente para insumo {item['id_insumo']}."

            # Guardamos que fila descontar y cuanto descontar, pero aun no tocamos el CSV.
            consumos.append((insumo.index[0], consumo))
        # Se descuenta todo despues de validar todos los insumos, evitando medias
        # actualizaciones si una linea de la receta falla.
        for idx, consumo in consumos:
            # Restamos consumo al stock del insumo.
            insumos.loc[idx, "stock_actual"] = float(insumos.loc[idx, "stock_actual"]) - consumo

        # Sumamos la cantidad fabricada al stock del producto terminado.
        productos.loc[idx_producto[0], "stock_actual"] = float(productos.loc[idx_producto[0], "stock_actual"]) + cantidad

        # Guardamos los dos inventarios modificados.
        guardar_csv(insumos, "insumos.csv")
        guardar_csv(productos, "productos.csv")

    # Cargamos historial de ordenes de produccion.
    produccion = listar_produccion()
    if produccion.empty:
        # Si no hay historial, creamos la tabla oficial.
        produccion = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO])

    # Armamos la orden para guardarla.
    fila = {
        "id_orden": nuevo_id(produccion, "id_orden", "ORD"),
        "id_producto": id_producto,
        "cantidad": cantidad,
        "fecha": fecha,
        "estado": estado,
    }
    # Agregamos la orden al historial.
    guardar_csv(pd.concat([produccion, pd.DataFrame([fila])], ignore_index=True), ARCHIVO)
    return True, "Orden de produccion registrada."
