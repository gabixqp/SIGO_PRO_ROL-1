"""Punto de entrada principal de la aplicacion Streamlit.

Este archivo solo configura la pagina inicial. Las pantallas reales viven en
la carpeta ``pages/`` y Streamlit las muestra automaticamente en la barra
lateral.
"""

import streamlit as st

from core.ui import aplicar_estilos


# Configuracion global de la ventana: titulo, icono y ancho de pantalla.
st.set_page_config(
    # Texto que aparece en la pestana del navegador.
    page_title="SIGO-PRO FoodOps",
    # Icono simple que Streamlit muestra en la pestana/barra.
    page_icon="SIGO",
    # "wide" usa mas ancho de pantalla para tablas y dashboards.
    layout="wide",
)

# Aplica el tema visual compartido antes de pintar cualquier contenido.
aplicar_estilos()

# Titulo grande de la pantalla principal.
st.title("SIGO-PRO FoodOps")

# Texto pequeno debajo del titulo.
st.caption("Sistema operativo para gestion de clientes, inventario, pedidos, produccion, despachos y reportes.")

# Mensajes de estado para dejar claro que esta pantalla es solo la portada.
st.info("Usa la barra lateral para navegar por los modulos del sistema.")
st.warning(
    "Esta etapa contiene solo codigo fuente. Los CSV reales y la configuracion de empresa se conectaran posteriormente."
)
