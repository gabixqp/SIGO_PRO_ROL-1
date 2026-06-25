"""Pagina de configuracion basica de empresa."""

import streamlit as st

from core.storage import cargar_json, existe_archivo, guardar_json
from core.ui import aplicar_estilos


aplicar_estilos()


@st.dialog("Editar configuracion", width="large")
def modal_guardar_configuracion(empresa_actual: dict) -> None:
    """Muestra el formulario de configuracion dentro de un modal."""
    # Formulario simple que escribe la configuracion de empresa en JSON.
    with st.form("form_configuracion"):
        # Datos basicos de empresa.
        nombre = st.text_input("Nombre empresa", value=str(empresa_actual.get("nombre", "")))
        ruc = st.text_input("RUC", value=str(empresa_actual.get("ruc", "")))
        direccion = st.text_input("Direccion", value=str(empresa_actual.get("direccion", "")))
        contacto = st.text_input("Contacto", value=str(empresa_actual.get("contacto", "")))
        if st.form_submit_button("Guardar configuracion", use_container_width=True):
            # Armamos un diccionario con lo escrito en el formulario.
            data = {
                "nombre": nombre,
                "ruc": ruc,
                "direccion": direccion,
                "contacto": contacto,
            }
            # Guardamos el diccionario como data/empresa.json.
            guardar_json(data, "empresa.json")
            st.success("Configuracion guardada en data/empresa.json.")
            st.rerun()


# Titulo de la pagina.
st.title("Configuracion")

empresa = {}
if existe_archivo("empresa.json"):
    try:
        # Cargamos el JSON de empresa para mostrarlo y precargar el modal.
        empresa = cargar_json("empresa.json")
    except RuntimeError as exc:
        # Si el archivo existe pero esta mal escrito, mostramos el error.
        st.error(str(exc))

col_titulo, col_boton = st.columns([0.72, 0.28], vertical_alignment="center")
col_titulo.subheader("Datos de empresa")
if col_boton.button("Editar configuracion", type="primary", use_container_width=True):
    modal_guardar_configuracion(empresa)

# Si ya existe data/empresa.json, se muestra para confirmar la configuracion actual.
if empresa:
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Nombre empresa", value=str(empresa.get("nombre", "")), disabled=True)
        st.text_input("RUC", value=str(empresa.get("ruc", "")), disabled=True)
    with c2:
        st.text_input("Direccion", value=str(empresa.get("direccion", "")), disabled=True)
        st.text_input("Contacto", value=str(empresa.get("contacto", "")), disabled=True)
else:
    st.warning("data/empresa.json no existe. No se creara automaticamente.")
