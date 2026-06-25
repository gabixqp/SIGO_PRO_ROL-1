"""Pagina de registro, consulta y analisis visual de clientes."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import (
    aplicar_estilos,
    mostrar_alerta,
    mostrar_footer,
    mostrar_seccion,
    mostrar_tarjeta_kpi,
    mostrar_titulo_pagina,
)
from modules.clientes import listar_clientes, registrar_cliente


# ============================================================
# 1. CONFIGURACION VISUAL
# ============================================================

aplicar_estilos()


# ============================================================
# 2. CATALOGOS LOCALES
# ============================================================

TIPOS_CLIENTE = [
    "persona",
    "empresa",
    "mayorista",
    "corporativo",
]

CANALES_CLIENTE = [
    "tienda",
    "delivery",
    "whatsapp",
    "web",
    "mayorista",
    "corporativo",
    "feria",
    "otro",
]


# ============================================================
# 3. FUNCIONES DE APOYO
# ============================================================

def cargar_clientes_seguro() -> pd.DataFrame:
    """Carga clientes con manejo visual de errores."""
    try:
        clientes = listar_clientes()
        if clientes is None:
            return pd.DataFrame()
        return clientes
    except Exception as exc:
        mostrar_alerta(
            "No se pudieron cargar los clientes",
            f"Ocurrio un problema al leer la base de clientes: {exc}",
            "danger",
        )
        return pd.DataFrame()


def valores_unicos(df: pd.DataFrame, columna: str) -> list[str]:
    """Devuelve valores unicos no vacios de una columna."""
    if df.empty or columna not in df.columns:
        return []

    valores = (
        df[columna]
        .dropna()
        .astype(str)
        .map(str.strip)
    )

    return sorted([valor for valor in valores.unique() if valor])


def contar_contactables(df: pd.DataFrame) -> int:
    """Cuenta clientes que tienen telefono o contacto registrado."""
    if df.empty:
        return 0

    mascara = pd.Series(False, index=df.index)

    for columna in ["telefono", "contacto"]:
        if columna in df.columns:
            mascara = mascara | df[columna].fillna("").astype(str).str.strip().ne("")

    return int(mascara.sum())


def contar_activos(df: pd.DataFrame) -> int:
    """Cuenta clientes activos si existe la columna estado."""
    if df.empty or "estado" not in df.columns:
        return 0

    return int(
        df["estado"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("activo")
        .sum()
    )


def contar_clientes_empresa(df: pd.DataFrame) -> int:
    """Cuenta clientes de tipo empresa, mayorista o corporativo."""
    if df.empty or "tipo" not in df.columns:
        return 0

    tipos_empresa = {"empresa", "mayorista", "corporativo"}

    return int(
        df["tipo"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(tipos_empresa)
        .sum()
    )


def filtrar_clientes(
    df: pd.DataFrame,
    busqueda: str,
    tipo: str,
    canal: str,
    estado: str,
) -> pd.DataFrame:
    """Aplica filtros visuales sin modificar datos."""
    if df.empty:
        return df

    filtrado = df.copy()

    if busqueda.strip():
        texto = busqueda.strip().lower()
        columnas_busqueda = [
            columna
            for columna in ["nombre", "contacto", "telefono", "canal", "tipo", "estado"]
            if columna in filtrado.columns
        ]

        if columnas_busqueda:
            mascara = pd.Series(False, index=filtrado.index)
            for columna in columnas_busqueda:
                mascara = mascara | (
                    filtrado[columna]
                    .fillna("")
                    .astype(str)
                    .str.lower()
                    .str.contains(texto, na=False)
                )
            filtrado = filtrado[mascara]

    if tipo != "Todos" and "tipo" in filtrado.columns:
        filtrado = filtrado[
            filtrado["tipo"].fillna("").astype(str).str.strip().eq(tipo)
        ]

    if canal != "Todos" and "canal" in filtrado.columns:
        filtrado = filtrado[
            filtrado["canal"].fillna("").astype(str).str.strip().eq(canal)
        ]

    if estado != "Todos" and "estado" in filtrado.columns:
        filtrado = filtrado[
            filtrado["estado"].fillna("").astype(str).str.strip().eq(estado)
        ]

    return filtrado


def mostrar_kpis_clientes(clientes: pd.DataFrame) -> None:
    """Muestra indicadores visuales de clientes."""
    total = len(clientes) if not clientes.empty else 0
    activos = contar_activos(clientes)
    empresas = contar_clientes_empresa(clientes)
    contactables = contar_contactables(clientes)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        mostrar_tarjeta_kpi(
            "Clientes",
            total,
            "Registros totales en la base.",
        )

    with c2:
        mostrar_tarjeta_kpi(
            "Activos",
            activos,
            "Clientes con estado activo.",
        )

    with c3:
        mostrar_tarjeta_kpi(
            "B2B / empresas",
            empresas,
            "Empresas, mayoristas o corporativos.",
        )

    with c4:
        mostrar_tarjeta_kpi(
            "Contactables",
            contactables,
            "Clientes con telefono o contacto.",
        )


# ============================================================
# 4. MODAL DE REGISTRO
# ============================================================

@st.dialog("Registrar cliente", width="large")
def modal_registrar_cliente() -> None:
    """Muestra el formulario de cliente dentro de un modal."""
    st.caption("Registra un nuevo cliente para pedidos, ventas y seguimiento.")

    with st.form("form_cliente"):
        c1, c2 = st.columns(2)

        with c1:
            nombre = st.text_input("Nombre del cliente")
            tipo = st.selectbox("Tipo de cliente", TIPOS_CLIENTE)
            canal = st.selectbox("Canal principal", CANALES_CLIENTE)

        with c2:
            contacto = st.text_input("Contacto")
            telefono = st.text_input("Telefono")

        guardar = st.form_submit_button(
            "Registrar cliente",
            use_container_width=True,
        )

        if guardar:
            ok, msg = registrar_cliente(
                nombre,
                tipo,
                canal,
                contacto,
                telefono,
            )

            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)


# ============================================================
# 5. CONTENIDO PRINCIPAL
# ============================================================

mostrar_titulo_pagina(
    "Clientes",
    "Registro, consulta y seguimiento de clientes para pedidos, ventas y canales de atencion.",
)

clientes = cargar_clientes_seguro()

mostrar_kpis_clientes(clientes)

mostrar_seccion(
    "Gestion de clientes",
    "Administra clientes individuales, empresas, mayoristas y contactos corporativos.",
)

col_info, col_boton = st.columns([0.72, 0.28], vertical_alignment="center")

with col_info:
    mostrar_alerta(
        "Base de clientes",
        "Desde esta pantalla se consulta la cartera de clientes y se registran nuevos contactos comerciales.",
        "info",
    )

with col_boton:
    if st.button("Registrar cliente", type="primary", use_container_width=True):
        modal_registrar_cliente()

if clientes.empty:
    mostrar_alerta(
        "No hay clientes disponibles",
        "No se encontraron registros o falta el archivo data/clientes.csv.",
        "warning",
    )
    mostrar_footer()
    st.stop()

mostrar_seccion(
    "Filtros de consulta",
    "Filtra la tabla para encontrar rapidamente clientes por nombre, tipo, canal o estado.",
)

f1, f2, f3, f4 = st.columns([0.34, 0.22, 0.22, 0.22])

with f1:
    busqueda = st.text_input(
        "Buscar",
        placeholder="Nombre, contacto, telefono, canal...",
    )

with f2:
    tipos_disponibles = ["Todos"] + valores_unicos(clientes, "tipo")
    tipo_filtro = st.selectbox("Tipo", tipos_disponibles)

with f3:
    canales_disponibles = ["Todos"] + valores_unicos(clientes, "canal")
    canal_filtro = st.selectbox("Canal", canales_disponibles)

with f4:
    estados_disponibles = ["Todos"] + valores_unicos(clientes, "estado")
    estado_filtro = st.selectbox("Estado", estados_disponibles)

clientes_filtrados = filtrar_clientes(
    clientes,
    busqueda,
    tipo_filtro,
    canal_filtro,
    estado_filtro,
)

mostrar_seccion(
    "Listado de clientes",
    f"Mostrando {len(clientes_filtrados)} de {len(clientes)} registros disponibles.",
)

if clientes_filtrados.empty:
    mostrar_alerta(
        "Sin resultados",
        "No hay clientes que coincidan con los filtros seleccionados.",
        "warning",
    )
else:
    st.dataframe(
        clientes_filtrados,
        use_container_width=True,
        hide_index=True,
    )

mostrar_alerta(
    "Integracion del modulo Clientes",
    (
        "Esta pagina conserva la logica de registro y consulta del modulo original, "
        "pero ahora usa componentes visuales compartidos desde core/ui.py."
    ),
    "success",
)

mostrar_footer()