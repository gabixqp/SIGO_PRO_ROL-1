"""Pagina para crear ordenes de produccion."""

import streamlit as st

from core.ui import aplicar_estilos
from modules.produccion import listar_produccion, registrar_orden_produccion
from modules.productos import obtener_productos_activos


aplicar_estilos()


@st.dialog("Registrar orden de produccion", width="large")
def modal_registrar_produccion(productos) -> None:
    """Muestra el formulario de produccion dentro de un modal."""
    # El usuario elige por nombre, pero internamente se guarda el id_producto.
    opciones = dict(zip(productos["nombre"], productos["id_producto"]))

    # Formulario para crear una orden.
    with st.form("form_produccion"):
        c1, c2 = st.columns(2)
        with c1:
            # Producto a fabricar y cantidad deseada.
            producto_nombre = st.selectbox("Producto", list(opciones.keys()))
            cantidad = st.number_input("Cantidad", min_value=0.0, step=1.0)
        with c2:
            # Fecha y estado de la orden.
            fecha = st.date_input("Fecha")
            estado = st.selectbox("Estado", ["pendiente", "completada"])
        if estado == "completada":
            # Completar una orden mueve inventario: consume insumos y sube stock.
            st.info("Al guardar se validara receta, stock de insumos y se movera inventario.")
        if st.form_submit_button("Registrar orden", use_container_width=True):
            # Convertimos nombre seleccionado a ID y llamamos la regla de negocio.
            ok, msg = registrar_orden_produccion(opciones[producto_nombre], cantidad, fecha.isoformat(), estado)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
            if ok:
                st.rerun()


# Titulo visible de la pagina.
st.title("Produccion")

# Explicacion corta del comportamiento principal.
st.caption("Ordenes de produccion con consumo de insumos solo al completar.")

# Cargamos productos que se pueden fabricar.
productos = obtener_productos_activos()
col_titulo, col_boton = st.columns([0.72, 0.28], vertical_alignment="center")
col_titulo.subheader("Ordenes")
if productos.empty:
    col_boton.button("Registrar orden", disabled=True, use_container_width=True)
    st.warning("Para registrar produccion se requieren productos disponibles.")
else:
    # Boton visible sobre la tabla; el formulario real se abre en modal.
    if col_boton.button("Registrar orden", type="primary", use_container_width=True):
        modal_registrar_produccion(productos)

# Consulta historica de ordenes ya guardadas.
produccion = listar_produccion()
# Si hay ordenes, se muestran; si no, se informa que falta data.
if produccion.empty:
    st.info("Sin ordenes de produccion disponibles.")
else:
    st.dataframe(produccion, use_container_width=True, hide_index=True)
