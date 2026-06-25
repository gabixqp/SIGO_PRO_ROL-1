"""Pagina inicial: resumen rapido del estado del sistema."""

import streamlit as st

from analytics.indicadores import calcular_indicadores_generales
from config import ARCHIVOS_CSV
from core.storage import validar_disponibilidad_archivo
from core.ui import aplicar_estilos


aplicar_estilos()

# Titulo de esta pagina.
st.title("Inicio")

# Texto breve que explica que se ve aqui.
st.write("Panel inicial de SIGO-PRO FoodOps para monitorear la operacion.")

# Revisa que todos los CSV esperados existan y tengan columnas correctas.
faltantes = []
for archivo in ARCHIVOS_CSV.values():
    # Revisamos archivo por archivo si existe y tiene columnas correctas.
    ok, msg = validar_disponibilidad_archivo(archivo)
    if not ok:
        # Si hay problema, guardamos el mensaje para mostrarlo luego.
        faltantes.append(msg)

if faltantes:
    # Mostramos advertencia general si al menos un archivo falla.
    st.warning("Hay archivos de datos pendientes de conectar.")
    for msg in faltantes:
        # Mostramos cada problema en letra pequena.
        st.caption(msg)

# Muestra KPIs principales en la parte superior del dashboard.
indicadores = calcular_indicadores_generales()

# Creamos cuatro columnas horizontales.
col1, col2, col3, col4 = st.columns(4)

# Cada metric muestra un numero importante del negocio.
col1.metric("Pedidos", indicadores["total_pedidos"])
col2.metric("Ventas", f"{indicadores['ventas_totales']:.2f}")
col3.metric("Clientes", indicadores["clientes"])
col4.metric("Productos criticos", indicadores["productos_criticos"])
