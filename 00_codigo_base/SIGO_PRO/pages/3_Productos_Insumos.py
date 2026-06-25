"""Pagina para administrar productos terminados e insumos."""

import streamlit as st

from core.ui import aplicar_estilos
from modules.insumos import listar_insumos, obtener_insumos_criticos, registrar_insumo
from modules.productos import listar_productos, obtener_productos_criticos, registrar_producto


aplicar_estilos()


def _resaltar_stock_critico(row):
    """Pinta en rojo suave la fila si stock_actual esta bajo o igual al minimo."""
    try:
        stock_actual = float(row.get("stock_actual", 0))
        stock_minimo = float(row.get("stock_minimo", 0))
    except (TypeError, ValueError):
        return [""] * len(row)

    if stock_actual <= stock_minimo:
        return ["background-color: #F8D7DA; color: #7F1713; font-weight: 600"] * len(row)
    return [""] * len(row)


@st.dialog("Registrar producto", width="large")
def modal_registrar_producto() -> None:
    """Muestra el formulario de producto dentro de un modal."""
    # Alta de productos: precio y stock alimentan ventas, costos y alertas.
    with st.form("form_producto"):
        # Dividimos campos en dos columnas.
        c1, c2 = st.columns(2)
        with c1:
            # Datos descriptivos del producto.
            nombre = st.text_input("Nombre producto")
            categoria = st.selectbox("Categoria", ["panaderia", "pasteleria", "bebidas", "comidas", "otros"])
            unidad = st.selectbox("Unidad", ["unidad", "porcion", "kg", "g", "litro", "ml", "caja", "paquete"])
        with c2:
            # Datos numericos del producto.
            precio = st.number_input("Precio venta", min_value=0.0, step=0.1)
            stock = st.number_input("Stock actual", min_value=0.0, step=0.1)
            minimo = st.number_input("Stock minimo", min_value=0.0, step=0.1)
        if st.form_submit_button("Registrar producto", use_container_width=True):
            # Envia los datos al modulo de productos para validar y guardar.
            ok, msg = registrar_producto(nombre, categoria, unidad, precio, stock, minimo)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
            if ok:
                st.rerun()


@st.dialog("Registrar insumo", width="large")
def modal_registrar_insumo() -> None:
    """Muestra el formulario de insumo dentro de un modal."""
    # Alta de insumos: costo y merma alimentan el calculo de costo de producto.
    with st.form("form_insumo"):
        # Dividimos el formulario en dos columnas.
        c1, c2 = st.columns(2)
        with c1:
            # Datos descriptivos y stock actual del insumo.
            nombre_i = st.text_input("Nombre insumo")
            unidad_i = st.selectbox("Unidad insumo", ["kg", "g", "litro", "ml", "unidad", "paquete", "caja", "bolsa"])
            stock_i = st.number_input("Stock actual insumo", min_value=0.0, step=0.1)
        with c2:
            # Datos de control y costo del insumo.
            minimo_i = st.number_input("Stock minimo insumo", min_value=0.0, step=0.1)
            costo_i = st.number_input("Costo unitario", min_value=0.0, step=0.1)
            merma_i = st.number_input("Merma %", min_value=0.0, step=0.1)
        if st.form_submit_button("Registrar insumo", use_container_width=True):
            # Envia datos al modulo de insumos para validar y guardar.
            ok, msg = registrar_insumo(nombre_i, unidad_i, stock_i, minimo_i, costo_i, merma_i)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
            if ok:
                st.rerun()


# Titulo de la pagina.
st.title("Productos e Insumos")

# Texto pequeno que resume la funcion de esta pagina.
st.caption("Registro y consulta de productos e insumos.")

# Dos pestanas separan inventario vendible de materia prima.
tab_productos, tab_insumos = st.tabs(["Productos", "Insumos"])

with tab_productos:
    col_titulo, col_boton = st.columns([0.72, 0.28], vertical_alignment="center")
    col_titulo.subheader("Listado de productos")
    # Boton visible sobre la tabla; el formulario real se abre en modal.
    if col_boton.button("Registrar producto", type="primary", use_container_width=True):
        modal_registrar_producto()

    # Mostramos todos los productos si existen.
    productos = listar_productos()
    criticos = obtener_productos_criticos()
    if not criticos.empty:
        st.warning(f"{len(criticos)} producto(s) con stock critico resaltado(s) en rojo.")
    if productos.empty:
        st.info("Sin productos disponibles.")
    else:
        st.dataframe(productos.style.apply(_resaltar_stock_critico, axis=1), use_container_width=True, hide_index=True)

with tab_insumos:
    col_titulo, col_boton = st.columns([0.72, 0.28], vertical_alignment="center")
    col_titulo.subheader("Listado de insumos")
    # Boton visible sobre la tabla; el formulario real se abre en modal.
    if col_boton.button("Registrar insumo", type="primary", use_container_width=True):
        modal_registrar_insumo()

    # Mostramos todos los insumos si existen.
    insumos = listar_insumos()
    criticos_i = obtener_insumos_criticos()
    if not criticos_i.empty:
        st.warning(f"{len(criticos_i)} insumo(s) con stock critico resaltado(s) en rojo.")
    if insumos.empty:
        st.info("Sin insumos disponibles.")
    else:
        st.dataframe(insumos.style.apply(_resaltar_stock_critico, axis=1), use_container_width=True, hide_index=True)
