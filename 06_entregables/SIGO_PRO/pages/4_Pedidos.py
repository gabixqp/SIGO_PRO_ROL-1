"""Pagina de pedidos con captura de multiples productos."""

import streamlit as st
import pandas as pd

try:
    from config import IGV_PCT_DEFAULT
except ImportError:
    # Fallback para recargas de Streamlit si config aun no expone el valor.
    IGV_PCT_DEFAULT = 18.0
from core.ui import aplicar_estilos
from modules.clientes import obtener_clientes_activos
try:
    from modules.pedidos import listar_detalle_pedidos, listar_pedidos, registrar_pedido_multiple
except ImportError:
    # Mensaje amable si Streamlit mantiene en memoria una version vieja.
    from modules.pedidos import listar_detalle_pedidos, listar_pedidos

    def registrar_pedido_multiple(*_args, **_kwargs):
        return False, "Reinicia Streamlit para cargar el registro de pedidos con multiples productos."
from modules.productos import obtener_productos_activos


aplicar_estilos()


def _feedback(ok: bool, msg: str) -> None:
    """Muestra exito o error segun el resultado de una operacion."""
    # Si ok es True mostramos mensaje verde; si es False mostramos mensaje rojo.
    if ok:
        st.success(msg)
    else:
        st.error(msg)


@st.dialog("Registrar pedido", width="large")
def modal_registrar_pedido(clientes, productos):
    """Modal que arma la cabecera del pedido y su detalle de productos."""
    # Creamos un diccionario: nombre visible del cliente -> id_cliente real.
    cliente_opciones = dict(zip(clientes["nombre"], clientes["id_cliente"]))

    # Columna izquierda: datos generales del pedido.
    col_izq, col_der = st.columns([0.30, 0.70])
    with col_izq:
        # Selector de cliente usando nombres legibles.
        cliente_nombre = st.selectbox("Cliente", list(cliente_opciones.keys()), key="pedido_cliente")

        # Fecha requerida por el cliente.
        fecha = st.date_input("Fecha requerida", key="pedido_fecha")

        # Tipo de comprobante para el pedido.
        tipo_comprobante = st.selectbox(
            "Comprobante",
            ["boleta", "factura", "nota_venta"],
            key="pedido_tipo_comprobante",
        )
        # IGV configurado por defecto.
        igv_pct = float(IGV_PCT_DEFAULT)

        # Campo deshabilitado: se muestra pero no se edita.
        st.text_input("IGV", value=f"{igv_pct:.0f}%", disabled=True)

        # Canal inicia vacio; si el cliente tiene canal, se reemplaza abajo.
        canal_default = ""

        # Convertimos el nombre seleccionado al ID interno.
        cliente_id = cliente_opciones[cliente_nombre]
        if "canal" in clientes.columns:
            # Tomamos el canal guardado del cliente seleccionado.
            canal_default = str(clientes.loc[clientes["id_cliente"] == cliente_id, "canal"].iloc[0])
        # Si el cliente ya tiene canal, se propone como valor inicial.
        canales = ["tienda", "delivery", "whatsapp", "web", "mayorista", "corporativo", "feria", "otro"]

        # Normalizamos el canal para compararlo sin mayusculas ni espacios.
        canal_default_normalizado = canal_default.strip().lower()
        if canal_default_normalizado and canal_default_normalizado not in canales:
            # Si el canal del cliente no esta en la lista, lo agregamos.
            canales.append(canal_default_normalizado)

        # Buscamos que opcion debe quedar seleccionada inicialmente.
        indice_canal = canales.index(canal_default_normalizado) if canal_default_normalizado in canales else 0

        # Selector final de canal.
        canal = st.selectbox("Canal", canales, index=indice_canal, key="pedido_canal")

    with col_der:
        # El usuario solo edita cantidades; producto y precio quedan bloqueados.
        st.subheader("Productos")
        st.caption("Ingresa cantidad solo en los productos que va a pedir el cliente.")

        # Estas columnas son las necesarias para armar el detalle del pedido.
        columnas_base = ["id_producto", "nombre", "precio_venta"]

        # Copiamos solo esas columnas para no editar la tabla original.
        productos_editor = productos[columnas_base].copy()

        # Renombramos columnas para que sean mas claras en pantalla.
        productos_editor = productos_editor.rename(
            columns={
                "nombre": "producto",
                "precio_venta": "precio_unitario",
            }
        )
        # Agregamos columna cantidad en cero; el usuario la cambia.
        productos_editor["cantidad"] = 0.0

        # Ordenamos columnas para el editor.
        productos_editor = productos_editor[["id_producto", "producto", "precio_unitario", "cantidad"]]

        # data_editor muestra una tabla editable.
        detalle_editado = st.data_editor(
            productos_editor,
            use_container_width=True,
            hide_index=True,
            height=300,
            disabled=["id_producto", "producto", "precio_unitario"],
            column_config={
                "id_producto": None,
                "producto": st.column_config.TextColumn("Producto", width="medium"),
                "precio_unitario": st.column_config.NumberColumn("P. unitario", format="%.2f", width="small"),
                "cantidad": st.column_config.NumberColumn("Cantidad", min_value=0.0, step=1.0, format="%.2f", width="small"),
            },
            key="pedido_detalle_editor",
        )

    st.divider()
    # Convierte lo editado a DataFrame para calcular subtotal, valor venta e IGV.
    detalle_editado = pd.DataFrame(detalle_editado)

    # Aseguramos que cantidad sea numerica; valores invalidos pasan a cero.
    detalle_editado["cantidad"] = pd.to_numeric(detalle_editado["cantidad"], errors="coerce").fillna(0)

    # Aseguramos que precio sea numerico.
    detalle_editado["precio_unitario"] = pd.to_numeric(detalle_editado["precio_unitario"], errors="coerce").fillna(0)

    # Subtotal por linea = cantidad * precio unitario.
    detalle_editado["subtotal"] = detalle_editado["cantidad"] * detalle_editado["precio_unitario"]

    # Valor venta es el total sin IGV.
    detalle_editado["valor_venta"] = detalle_editado["subtotal"] / (1 + igv_pct / 100) if igv_pct else detalle_editado["subtotal"]

    # IGV por linea = subtotal final menos valor sin IGV.
    detalle_editado["igv"] = detalle_editado["subtotal"] - detalle_editado["valor_venta"]

    # Para el resumen solo usamos productos con cantidad mayor a cero.
    detalle_preview = detalle_editado[detalle_editado["cantidad"] > 0].copy()
    # Solo se envian al modulo de pedidos las filas con cantidad real.
    items = detalle_preview[["id_producto", "cantidad"]].to_dict("records")

    # Total del pedido = suma de subtotales de productos elegidos.
    total = float(detalle_preview["subtotal"].sum()) if not detalle_preview.empty else 0.0

    # Mostramos dos indicadores pequenos: cantidad de productos y total.
    m1, m2 = st.columns(2)
    m1.metric("Productos", len([item for item in items if item["cantidad"] > 0]))
    m2.metric("Total", f"{total:.2f}")
    if not detalle_preview.empty:
        # Si el cliente eligio productos, mostramos resumen antes de guardar.
        st.subheader("Resumen del pedido")
        st.dataframe(
            detalle_preview[["producto", "cantidad", "precio_unitario", "valor_venta", "igv", "subtotal"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "precio_unitario": st.column_config.NumberColumn("P. unitario", format="%.2f"),
                "valor_venta": st.column_config.NumberColumn("Valor venta", format="%.2f"),
                "igv": st.column_config.NumberColumn("IGV", format="%.2f"),
                "subtotal": st.column_config.NumberColumn("Total", format="%.2f"),
            },
        )

    if st.button("Guardar pedido", type="primary", use_container_width=True):
        # La logica de guardado vive en modules/pedidos.py; la pagina solo captura datos.
        ok, msg = registrar_pedido_multiple(
            cliente_opciones[cliente_nombre],
            items,
            fecha.isoformat(),
            canal,
            tipo_comprobante,
            igv_pct,
        )
        _feedback(ok, msg)
        if ok:
            st.rerun()


st.title("Pedidos")
st.caption("Registro de pedidos con detalle generado desde el producto seleccionado.")

clientes = obtener_clientes_activos()
productos = obtener_productos_activos()

# Encabezado con titulo a la izquierda y boton a la derecha.
left, right = st.columns([0.72, 0.28], vertical_alignment="center")
left.subheader("Pedidos")
# No permite registrar pedidos si faltan clientes o productos.
if clientes.empty or productos.empty:
    right.button("Registrar pedido", disabled=True, use_container_width=True)
    st.warning("Para registrar pedidos se requieren clientes y productos disponibles.")
elif right.button("Registrar pedido", type="primary", use_container_width=True):
    # Abre el modal de registro.
    modal_registrar_pedido(clientes, productos)

# Cargamos cabeceras de pedidos.
pedidos = listar_pedidos()
if pedidos.empty:
    st.info("Sin pedidos disponibles.")
else:
    # Mostramos cabeceras de pedidos.
    st.dataframe(pedidos, use_container_width=True, hide_index=True)

st.subheader("Detalle")
# La cabecera y el detalle se muestran separados porque viven en CSV distintos.
detalle = listar_detalle_pedidos()
# Mostramos lineas de productos vendidos por pedido.
if detalle.empty:
    st.info("Sin detalle de pedidos disponible.")
else:
    st.dataframe(detalle, use_container_width=True, hide_index=True)
