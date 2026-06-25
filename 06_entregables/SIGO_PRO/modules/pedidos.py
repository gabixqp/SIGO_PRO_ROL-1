"""Registro de pedidos y detalle de productos vendidos."""

from datetime import date

import pandas as pd

try:
    from config import COLUMNAS_CSV, IGV_PCT_DEFAULT
except ImportError:
    # Fallback para versiones antiguas del config durante recargas de Streamlit.
    from config import COLUMNAS_CSV
    IGV_PCT_DEFAULT = 18.0
from core.limpieza import convertir_numericos
from core.storage import cargar_csv, guardar_csv, nuevo_id
from core.validaciones import validar_numero_no_negativo, validar_texto_obligatorio
from modules.productos import listar_productos


ARCHIVO_PEDIDOS = "pedidos.csv"
ARCHIVO_DETALLE = "detalle_pedidos.csv"


def listar_pedidos() -> pd.DataFrame:
    """Carga pedidos y convierte el total a numero."""
    # pedidos.csv guarda la cabecera: cliente, fecha, canal, estado y total.
    return convertir_numericos(cargar_csv(ARCHIVO_PEDIDOS), ["total"])


def listar_detalle_pedidos() -> pd.DataFrame:
    """Carga el detalle de pedidos con cantidades, precios y subtotales numericos."""
    # detalle_pedidos.csv guarda las lineas: que producto, cuanta cantidad y subtotal.
    return convertir_numericos(cargar_csv(ARCHIVO_DETALLE), ["cantidad", "precio_unitario", "subtotal"])


def registrar_pedido(
    id_cliente,
    id_producto,
    cantidad,
    fecha_requerida=None,
    canal="",
    tipo_comprobante="boleta",
    igv_pct=IGV_PCT_DEFAULT,
) -> tuple[bool, str]:
    """Registra un pedido de un solo producto.

    Se conserva para pantallas o integraciones simples. La pagina principal usa
    registrar_pedido_multiple para permitir varios productos en una venta.
    """
    # Validamos textos basicos: cliente, producto y canal.
    for valor, campo in [(id_cliente, "Cliente"), (id_producto, "Producto"), (canal, "Canal")]:
        ok, msg = validar_texto_obligatorio(valor, campo)
        if not ok:
            return ok, msg

    # Validamos que cantidad sea numero no negativo.
    ok, msg = validar_numero_no_negativo(cantidad, "Cantidad")
    if not ok:
        return ok, msg

    # En un pedido la cantidad debe ser mayor que cero; cero no vende nada.
    if float(cantidad) <= 0:
        return False, "Cantidad debe ser mayor que cero."

    # Cargamos productos para buscar el precio del producto vendido.
    productos = listar_productos()
    if productos.empty or "id_producto" not in productos.columns:
        return False, "No hay productos disponibles."

    # Filtramos el producto elegido por ID.
    producto = productos[productos["id_producto"] == id_producto]
    if producto.empty:
        return False, "Producto no encontrado."

    # Tomamos el precio de venta de la primera fila encontrada.
    precio_unitario = float(producto.iloc[0]["precio_venta"])

    # Subtotal = cantidad comprada multiplicada por precio unitario.
    subtotal = float(cantidad) * precio_unitario
    # El subtotal se trata como precio final con IGV incluido.
    valor_venta = subtotal / (1 + float(igv_pct) / 100)
    igv = subtotal - valor_venta

    # Cargamos cabecera y detalle existentes para agregar el pedido.
    pedidos = listar_pedidos()
    detalle = listar_detalle_pedidos()
    if pedidos.empty:
        # Si no hay pedidos, creamos tabla con columnas oficiales.
        pedidos = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO_PEDIDOS])
    if detalle.empty:
        # Si no hay detalle, creamos tabla con columnas oficiales.
        detalle = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO_DETALLE])

    # Generamos ID de pedido nuevo, por ejemplo PED004.
    id_pedido = nuevo_id(pedidos, "id_pedido", "PED")

    # Esta es la cabecera del pedido: datos generales de la venta.
    pedido = {
        "id_pedido": id_pedido,
        "id_cliente": id_cliente,
        "fecha": fecha_requerida or date.today().isoformat(),
        "canal": canal,
        "estado": "registrado",
        "total": subtotal,
    }
    # Solo se escriben columnas tributarias si el CSV ya las trae.
    if "tipo_comprobante" in pedidos.columns:
        pedido["tipo_comprobante"] = tipo_comprobante
    if "valor_venta" in pedidos.columns:
        pedido["valor_venta"] = valor_venta
    if "igv_pct" in pedidos.columns:
        pedido["igv_pct"] = float(igv_pct)
    if "igv" in pedidos.columns:
        pedido["igv"] = igv
    if "total_con_igv" in pedidos.columns:
        pedido["total_con_igv"] = subtotal

    # Esta es la linea de detalle: producto vendido dentro del pedido.
    det = {
        "id_detalle": nuevo_id(detalle, "id_detalle", "DET"),
        "id_pedido": id_pedido,
        "id_producto": id_producto,
        "cantidad": float(cantidad),
        "precio_unitario": precio_unitario,
        "subtotal": subtotal,
    }
    # Guardamos cabecera en pedidos.csv.
    guardar_csv(pd.concat([pedidos, pd.DataFrame([pedido])], ignore_index=True), ARCHIVO_PEDIDOS)

    # Guardamos detalle en detalle_pedidos.csv.
    guardar_csv(pd.concat([detalle, pd.DataFrame([det])], ignore_index=True), ARCHIVO_DETALLE)
    return True, f"Pedido {id_pedido} registrado."


def registrar_pedido_multiple(
    id_cliente,
    items,
    fecha_requerida=None,
    canal="",
    tipo_comprobante="boleta",
    igv_pct=IGV_PCT_DEFAULT,
) -> tuple[bool, str]:
    """Registra un pedido con multiples productos en una sola cabecera."""
    # El cliente es obligatorio.
    ok, msg = validar_texto_obligatorio(id_cliente, "Cliente")
    if not ok:
        return ok, msg

    # El canal de venta tambien es obligatorio.
    ok, msg = validar_texto_obligatorio(canal, "Canal")
    if not ok:
        return ok, msg

    # Si la lista de productos viene vacia, no hay nada que registrar.
    if not items:
        return False, "Agrega al menos un producto al pedido."

    # Cargamos productos para saber precios y validar IDs.
    productos = listar_productos()
    if productos.empty or "id_producto" not in productos.columns:
        return False, "No hay productos disponibles."

    # Cargamos tablas actuales de pedidos y detalles.
    pedidos = listar_pedidos()
    detalle = listar_detalle_pedidos()
    if pedidos.empty:
        pedidos = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO_PEDIDOS])
    if detalle.empty:
        detalle = pd.DataFrame(columns=COLUMNAS_CSV[ARCHIVO_DETALLE])

    # Creamos el ID de cabecera que compartiran todas las lineas del detalle.
    id_pedido = nuevo_id(pedidos, "id_pedido", "PED")

    # Aqui juntaremos las lineas nuevas del detalle antes de guardar.
    detalle_nuevo = []

    # Total acumulado del pedido completo.
    total = 0.0

    # Copia del detalle existente para calcular IDs sin repetir.
    detalle_base = detalle.copy()

    for item in items:
        # Cada item llega desde el editor de Streamlit como diccionario.
        id_producto = item.get("id_producto")
        cantidad = item.get("cantidad", 0)

        # Validamos que cada linea tenga producto.
        ok, msg = validar_texto_obligatorio(id_producto, "Producto")
        if not ok:
            return ok, msg

        # Validamos que cada cantidad sea numerica.
        ok, msg = validar_numero_no_negativo(cantidad, "Cantidad")
        if not ok:
            return ok, msg
        if float(cantidad) <= 0:
            # Filas con cantidad cero se ignoran: estaban visibles solo para elegir.
            continue

        # Buscamos el producto para obtener su precio.
        producto = productos[productos["id_producto"] == id_producto]
        if producto.empty:
            return False, f"Producto {id_producto} no encontrado."

        # Calculamos subtotal de esta linea.
        precio_unitario = float(producto.iloc[0]["precio_venta"])
        subtotal = float(cantidad) * precio_unitario

        # Sumamos esta linea al total del pedido.
        total += subtotal
        # El ID de detalle se calcula considerando los ya existentes y los nuevos
        # de este mismo pedido para no repetir DET001, DET002, etc.
        id_detalle = nuevo_id(pd.concat([detalle_base, pd.DataFrame(detalle_nuevo)], ignore_index=True), "id_detalle", "DET")

        # Guardamos la linea en memoria; todavia no escribimos el archivo.
        detalle_nuevo.append(
            {
                "id_detalle": id_detalle,
                "id_pedido": id_pedido,
                "id_producto": id_producto,
                "cantidad": float(cantidad),
                "precio_unitario": precio_unitario,
                "subtotal": subtotal,
            }
        )

    # Si todas las cantidades eran cero, no se registra el pedido.
    if not detalle_nuevo:
        return False, "Las cantidades deben ser mayores que cero."

    # Calculamos valor venta e IGV a partir del total final.
    valor_venta = total / (1 + float(igv_pct) / 100)
    igv = total - valor_venta

    # Cabecera del pedido: un solo registro para toda la venta.
    pedido = {
        "id_pedido": id_pedido,
        "id_cliente": id_cliente,
        "fecha": fecha_requerida or date.today().isoformat(),
        "canal": canal,
        "estado": "registrado",
        "total": total,
    }
    if "tipo_comprobante" in pedidos.columns:
        pedido["tipo_comprobante"] = tipo_comprobante
    if "valor_venta" in pedidos.columns:
        pedido["valor_venta"] = valor_venta
    if "igv_pct" in pedidos.columns:
        pedido["igv_pct"] = float(igv_pct)
    if "igv" in pedidos.columns:
        pedido["igv"] = igv
    if "total_con_igv" in pedidos.columns:
        pedido["total_con_igv"] = total

    # Guardamos la cabecera.
    guardar_csv(pd.concat([pedidos, pd.DataFrame([pedido])], ignore_index=True), ARCHIVO_PEDIDOS)

    # Guardamos todas las lineas de detalle de golpe.
    guardar_csv(pd.concat([detalle, pd.DataFrame(detalle_nuevo)], ignore_index=True), ARCHIVO_DETALLE)
    return True, f"Pedido {id_pedido} registrado con {len(detalle_nuevo)} producto(s)."
