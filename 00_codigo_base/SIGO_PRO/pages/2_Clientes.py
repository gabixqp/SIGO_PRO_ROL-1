"""Pagina de registro y consulta de clientes."""

import streamlit as st

from core.ui import aplicar_estilos
from modules.clientes import listar_clientes, registrar_cliente


aplicar_estilos()


@st.dialog("Registrar cliente", width="large")
def modal_registrar_cliente() -> None:
    """Muestra el formulario de cliente dentro de un modal."""
    # Formulario compacto para crear nuevos clientes.
    with st.form("form_cliente"):
        # Dividimos el formulario en dos columnas para ahorrar espacio.
        c1, c2 = st.columns(2)
        with c1:
            # Campos de texto de la primera columna.
            nombre = st.text_input("Nombre")
            tipo = st.selectbox("Tipo", ["persona", "empresa", "mayorista", "corporativo"])
            canal = st.selectbox("Canal", ["tienda", "delivery", "whatsapp", "web", "mayorista", "corporativo", "feria", "otro"])
        with c2:
            # Campos de texto de la segunda columna.
            contacto = st.text_input("Contacto")
            telefono = st.text_input("Telefono")

        # Este boton envia el formulario.
        if st.form_submit_button("Registrar cliente", use_container_width=True):
            # Llamamos la funcion de negocio que valida y guarda.
            ok, msg = registrar_cliente(nombre, tipo, canal, contacto, telefono)
            # Si ok es True muestra exito; si es False muestra error.
            if ok:
                st.success(msg)
            else:
                st.error(msg)
            if ok:
                st.rerun()


# Titulo visible de la pagina.
st.title("Clientes")

# Descripcion corta debajo del titulo.
st.caption("Registro y consulta de clientes.")

# Tabla de consulta: muestra lo que exista en data/clientes.csv.
col_titulo, col_boton = st.columns([0.72, 0.28], vertical_alignment="center")
col_titulo.subheader("Listado")
if col_boton.button("Registrar cliente", type="primary", use_container_width=True):
    modal_registrar_cliente()

clientes = listar_clientes()
if clientes.empty:
    # Si la tabla esta vacia, avisamos que no hay datos.
    st.warning("No hay clientes disponibles o falta data/clientes.csv.")
else:
    # Si hay datos, los mostramos como tabla.
    st.dataframe(clientes, use_container_width=True, hide_index=True)
