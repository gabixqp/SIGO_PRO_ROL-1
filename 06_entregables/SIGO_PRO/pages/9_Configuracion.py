"""Pagina de configuracion del sistema.

Esta pantalla forma parte del Rol 1 Integrador. Permite visualizar y editar
datos generales de la empresa, revisar rutas principales y evidenciar la
configuracion central del software.
"""

from __future__ import annotations

from html import escape

import streamlit as st

from config import (
    APP_CONFIG,
    ASSETS_DIR,
    BACKUPS_DIR,
    DATA_DIR,
    EMPRESA,
    EXPORTACIONES_DIR,
    GRAFICOS_DIR,
    LOGS_DIR,
    OUTPUT_DIR,
    REPORTES_DIR,
    TEXTOS_APP,
)
from core.storage import cargar_json, existe_archivo, guardar_json
from core.ui import (
    aplicar_estilos,
    crear_badge_estado,
    mostrar_alerta,
    mostrar_footer,
    mostrar_seccion,
    mostrar_titulo_pagina,
)


# ============================================================
# 1. CONFIGURACION VISUAL
# ============================================================

aplicar_estilos()


# ============================================================
# 2. FUNCIONES DE APOYO
# ============================================================

def cargar_empresa_actual() -> dict:
    """Carga data/empresa.json si existe."""
    if not existe_archivo("empresa.json"):
        return {}

    try:
        return cargar_json("empresa.json")
    except RuntimeError as exc:
        st.error(str(exc))
        return {}


def construir_empresa_mostrable(empresa_json: dict) -> dict:
    """Combina datos de config.py con data/empresa.json.

    Se usa config.py como respaldo para que la pantalla siempre tenga datos
    coherentes aunque empresa.json no exista o este incompleto.
    """
    empresa = dict(EMPRESA)

    if not empresa_json:
        return empresa

    nombre = (
        empresa_json.get("nombre_comercial")
        or empresa_json.get("nombre")
        or empresa.get("nombre_comercial", "")
    )

    empresa["nombre_comercial"] = nombre
    empresa["razon_social"] = empresa_json.get(
        "razon_social",
        empresa.get("razon_social", ""),
    )
    empresa["ruc"] = empresa_json.get("ruc", empresa.get("ruc", ""))
    empresa["ubicacion"] = (
        empresa_json.get("ubicacion")
        or empresa_json.get("direccion")
        or empresa.get("ubicacion", "")
    )
    empresa["direccion"] = (
        empresa_json.get("direccion")
        or empresa_json.get("ubicacion")
        or empresa.get("ubicacion", "")
    )
    empresa["contacto"] = empresa_json.get("contacto", "")
    empresa["rubro"] = empresa_json.get("rubro", empresa.get("rubro", ""))
    empresa["estado"] = empresa_json.get("estado", empresa.get("estado", "Activo"))
    empresa["condicion"] = empresa_json.get(
        "condicion",
        empresa.get("condicion", "Habido"),
    )

    return empresa


def mostrar_card_dato(titulo: str, valor: str, ayuda: str = "") -> None:
    """Muestra una tarjeta visual para datos de configuracion."""
    st.markdown(
        f"""
        <div class="sigo-kpi-card" style="min-height: 135px;">
            <div class="sigo-kpi-label">{escape(titulo)}</div>
            <div class="sigo-kpi-value" style="font-size: 1.25rem; line-height: 1.2;">
                {escape(valor)}
            </div>
            <div class="sigo-kpi-help">{escape(ayuda)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_card_ruta(titulo: str, ruta, descripcion: str) -> None:
    """Muestra estado de una ruta principal."""
    existe = ruta.exists()
    tipo = "success" if existe else "warning"
    estado = "Disponible" if existe else "Pendiente"

    st.markdown(
        f"""
        <div class="sigo-module-card" style="min-height: 150px;">
            <div class="sigo-module-title">{escape(titulo)}</div>
            <div class="sigo-module-desc" style="margin-bottom: 0.7rem;">
                {escape(descripcion)}
            </div>
            <div style="margin-bottom: 0.65rem;">
                {crear_badge_estado(estado, tipo)}
            </div>
            <div style="
                font-size: 0.78rem;
                color: var(--sigo-muted);
                word-break: break-all;
                line-height: 1.35;
            ">
                {escape(str(ruta))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 3. MODAL DE EDICION
# ============================================================

@st.dialog("Editar configuracion de empresa", width="large")
def modal_guardar_configuracion(empresa_actual: dict) -> None:
    """Muestra el formulario de configuracion dentro de un modal."""
    with st.form("form_configuracion"):
        st.caption("Actualiza los datos principales de la empresa piloto.")

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input(
                "Nombre comercial",
                value=str(empresa_actual.get("nombre_comercial", "")),
            )
            razon_social = st.text_input(
                "Razon social",
                value=str(empresa_actual.get("razon_social", "")),
            )
            ruc = st.text_input(
                "RUC",
                value=str(empresa_actual.get("ruc", "")),
            )
            contacto = st.text_input(
                "Contacto",
                value=str(empresa_actual.get("contacto", "")),
            )

        with col2:
            ubicacion = st.text_input(
                "Ubicacion / direccion",
                value=str(
                    empresa_actual.get("ubicacion")
                    or empresa_actual.get("direccion")
                    or ""
                ),
            )
            rubro = st.text_area(
                "Rubro",
                value=str(empresa_actual.get("rubro", "")),
                height=90,
            )
            estado = st.selectbox(
                "Estado",
                ["Activo", "Inactivo"],
                index=0 if str(empresa_actual.get("estado", "Activo")).lower() == "activo" else 1,
            )
            condicion = st.selectbox(
                "Condicion",
                ["Habido", "No habido"],
                index=0 if str(empresa_actual.get("condicion", "Habido")).lower() == "habido" else 1,
            )

        guardar = st.form_submit_button(
            "Guardar configuracion",
            use_container_width=True,
        )

        if guardar:
            data = {
                "nombre": nombre,
                "nombre_comercial": nombre,
                "razon_social": razon_social,
                "ruc": ruc,
                "direccion": ubicacion,
                "ubicacion": ubicacion,
                "contacto": contacto,
                "rubro": rubro,
                "estado": estado,
                "condicion": condicion,
            }

            guardar_json(data, "empresa.json")
            st.success("Configuracion guardada correctamente en data/empresa.json.")
            st.rerun()


# ============================================================
# 4. CONTENIDO PRINCIPAL
# ============================================================

empresa_json = cargar_empresa_actual()
empresa = construir_empresa_mostrable(empresa_json)

mostrar_titulo_pagina(
    "Configuracion del sistema",
    "Panel central para datos de empresa, rutas, estructura visual y parametros base del Rol 1 Integrador.",
)

col_estado1, col_estado2, col_estado3 = st.columns([0.34, 0.33, 0.33])

with col_estado1:
    mostrar_card_dato(
        "Sistema",
        TEXTOS_APP.get("titulo", "SIGO-PRO FoodOps"),
        "Nombre operativo de la aplicacion.",
    )

with col_estado2:
    mostrar_card_dato(
        "Empresa piloto",
        str(empresa.get("nombre_comercial", "")),
        "Organizacion usada para validar el sistema.",
    )

with col_estado3:
    mostrar_card_dato(
        "RUC",
        str(empresa.get("ruc", "")),
        "Identificador tributario registrado.",
    )

mostrar_seccion(
    "Datos generales de empresa",
    "Informacion usada para identificar la empresa piloto dentro del sistema.",
)

col_info, col_accion = st.columns([0.72, 0.28], vertical_alignment="center")

with col_info:
    estado_html = crear_badge_estado(str(empresa.get("estado", "Activo")), "success")
    condicion_html = crear_badge_estado(str(empresa.get("condicion", "Habido")), "info")

    st.markdown(
        f"""
        <div class="sigo-info-card">
            <div class="sigo-info-title">{escape(str(empresa.get("nombre_comercial", "")))}</div>
            <div class="sigo-info-meta">
                RUC {escape(str(empresa.get("ruc", "")))} · {escape(str(empresa.get("ubicacion", "")))}
            </div>
            <div class="sigo-info-rubro">
                {escape(str(empresa.get("rubro", "")))}
            </div>
            <div style="margin-top: 0.8rem;">
                {estado_html}
                {condicion_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_accion:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Editar configuracion", type="primary", use_container_width=True):
        modal_guardar_configuracion(empresa)

if empresa_json:
    mostrar_alerta(
        "Configuracion personalizada activa",
        "Los datos se estan leyendo desde data/empresa.json.",
        "success",
    )
else:
    mostrar_alerta(
        "Configuracion base activa",
        "No se encontro data/empresa.json. Se muestran los datos centrales definidos en config.py.",
        "warning",
    )

mostrar_seccion(
    "Detalle de configuracion",
    "Vista rapida de los campos principales actualmente disponibles.",
)

d1, d2 = st.columns(2)

with d1:
    st.text_input(
        "Nombre comercial",
        value=str(empresa.get("nombre_comercial", "")),
        disabled=True,
    )
    st.text_input(
        "Razon social",
        value=str(empresa.get("razon_social", "")),
        disabled=True,
    )
    st.text_input(
        "RUC",
        value=str(empresa.get("ruc", "")),
        disabled=True,
    )

with d2:
    st.text_input(
        "Ubicacion",
        value=str(empresa.get("ubicacion", "")),
        disabled=True,
    )
    st.text_input(
        "Contacto",
        value=str(empresa.get("contacto", "")),
        disabled=True,
    )
    st.text_input(
        "Configuracion Streamlit",
        value=f"{APP_CONFIG.get('layout', 'wide')} · sidebar {APP_CONFIG.get('initial_sidebar_state', 'expanded')}",
        disabled=True,
    )

mostrar_seccion(
    "Rutas principales",
    "Carpetas que sostienen datos, assets, reportes, graficos, logs y respaldos.",
)

r1, r2, r3 = st.columns(3)

with r1:
    mostrar_card_ruta(
        "Datos",
        DATA_DIR,
        "CSV y JSON usados por los modulos.",
    )

with r2:
    mostrar_card_ruta(
        "Assets",
        ASSETS_DIR,
        "Logo, fondos, iconos e imagenes del sistema.",
    )

with r3:
    mostrar_card_ruta(
        "Output",
        OUTPUT_DIR,
        "Carpeta general de resultados generados.",
    )

r4, r5, r6 = st.columns(3)

with r4:
    mostrar_card_ruta(
        "Reportes",
        REPORTES_DIR,
        "Reportes ejecutivos y salidas textuales.",
    )

with r5:
    mostrar_card_ruta(
        "Graficos",
        GRAFICOS_DIR,
        "Imagenes PNG generadas por analitica.",
    )

with r6:
    mostrar_card_ruta(
        "Exportaciones",
        EXPORTACIONES_DIR,
        "Archivos CSV exportados desde el sistema.",
    )

r7, r8 = st.columns(2)

with r7:
    mostrar_card_ruta(
        "Logs",
        LOGS_DIR,
        "Registros tecnicos y trazabilidad futura.",
    )

with r8:
    mostrar_card_ruta(
        "Backups",
        BACKUPS_DIR,
        "Respaldos antes de cambios o guardados criticos.",
    )

mostrar_alerta(
    "Evidencia del Rol 1",
    (
        "Esta pagina muestra configuracion central, datos de empresa, rutas "
        "principales y estado base de carpetas del sistema final."
    ),
    "info",
)

mostrar_footer(TEXTOS_APP.get("footer"))