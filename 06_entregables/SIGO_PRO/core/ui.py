"""Utilidades compartidas para la interfaz Streamlit.

Este modulo centraliza la identidad visual de SIGO-PRO FoodOps.
Debe ser usado por app.py y por las paginas de pages/ para evitar estilos
duplicados y lograr una experiencia visual consistente.
"""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

try:
    from config import ASSETS, COLORES, EMPRESA, MODULOS_APP, TEXTOS_APP
except ImportError:
    # Fallback defensivo para evitar que la UI se rompa si se ejecuta fuera
    # del contexto normal del proyecto.
    ASSETS = {}
    MODULOS_APP = []
    EMPRESA = {
        "nombre_comercial": "Gourmet Senor de Locumba",
        "ruc": "20612215546",
        "ubicacion": "Tiabaya, Arequipa",
        "sistema": "SIGO-PRO FoodOps",
    }
    TEXTOS_APP = {
        "titulo": "SIGO-PRO FoodOps",
        "subtitulo": "Gestion operativa inteligente",
        "hero_titulo": "Gestiona pedidos, produccion, inventario y costos desde un solo lugar.",
        "hero_descripcion": "Sistema de gestion operativa para servicios de alimentacion.",
        "footer": "SIGO-PRO FoodOps",
    }
    COLORES = {
        "rojo_vino": "#8B0F1A",
        "rojo_vino_oscuro": "#5E0810",
        "negro_carbon": "#111111",
        "gris_carbon": "#1C1C1C",
        "gris_medio": "#4B4B4B",
        "crema": "#F6EFE3",
        "crema_suave": "#FFF9F0",
        "blanco": "#FFFFFF",
        "dorado": "#C9A44C",
        "dorado_suave": "#E2C878",
        "verde": "#2E7D32",
        "amarillo": "#F9A825",
        "rojo_alerta": "#C62828",
        "azul_info": "#1565C0",
    }


# ============================================================
# 1. UTILIDADES INTERNAS
# ============================================================

def _color(clave: str, fallback: str = "#FFFFFF") -> str:
    """Devuelve un color desde config.COLORES con fallback seguro."""
    return COLORES.get(clave, fallback)


def _path_to_data_uri(path: Path | str | None) -> str:
    """Convierte una imagen local a data URI para usarla en CSS/HTML."""
    if not path:
        return ""

    ruta = Path(path)
    if not ruta.exists() or not ruta.is_file():
        return ""

    extension = ruta.suffix.lower().replace(".", "")
    mime = "jpeg" if extension in {"jpg", "jpeg"} else extension

    try:
        contenido = ruta.read_bytes()
        encoded = base64.b64encode(contenido).decode("utf-8")
        return f"data:image/{mime};base64,{encoded}"
    except OSError:
        return ""


def _leer_svg(path: Path | str | None) -> str:
    """Lee un SVG local como texto. Si no existe, devuelve cadena vacia."""
    if not path:
        return ""

    ruta = Path(path)
    if not ruta.exists() or not ruta.is_file():
        return ""

    try:
        return ruta.read_text(encoding="utf-8")
    except OSError:
        return ""


# ============================================================
# 2. CSS GLOBAL
# ============================================================

def aplicar_estilos() -> None:
    """Inyecta el CSS corporativo usado por todas las paginas."""
    st.markdown(
        f"""
        <style>
        :root {{
            --sigo-primary: {_color("rojo_vino")};
            --sigo-primary-dark: {_color("rojo_vino_oscuro")};
            --sigo-gold: {_color("dorado")};
            --sigo-gold-soft: {_color("dorado_suave")};
            --sigo-bg: {_color("crema")};
            --sigo-bg-soft: {_color("crema_suave")};
            --sigo-card: {_color("blanco")};
            --sigo-dark: {_color("negro_carbon")};
            --sigo-dark-soft: {_color("gris_carbon")};
            --sigo-border: rgba(94, 8, 16, 0.16);
            --sigo-text: #2B211E;
            --sigo-muted: {_color("gris_medio")};
            --sigo-success: {_color("verde")};
            --sigo-warning: {_color("amarillo")};
            --sigo-danger: {_color("rojo_alerta")};
            --sigo-info: {_color("azul_info")};
            --sigo-shadow: 0 18px 42px rgba(17, 17, 17, 0.12);
            --sigo-shadow-soft: 0 8px 22px rgba(17, 17, 17, 0.08);
            --sigo-radius: 18px;
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background:
                radial-gradient(circle at top left, rgba(201, 164, 76, 0.14), transparent 34%),
                linear-gradient(135deg, var(--sigo-bg) 0%, var(--sigo-bg-soft) 48%, #EFE1CB 100%);
            color: var(--sigo-text);
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1320px;
        }}

        [data-testid="stHeader"] {{
            background: rgba(246, 239, 227, 0.78);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid var(--sigo-border);
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(255, 249, 240, 0.98), rgba(246, 239, 227, 0.98));
            border-right: 1px solid var(--sigo-border);
        }}

        [data-testid="stSidebarNav"]::before {{
            content: "SIGO-PRO FoodOps";
            display: block;
            padding: 1.15rem 1.1rem 0.9rem 1.1rem;
            color: var(--sigo-primary-dark);
            font-size: 1.05rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            border-bottom: 1px solid var(--sigo-border);
            margin-bottom: 0.55rem;
        }}

        [data-testid="stSidebarNav"] ul li:first-child {{
            display: none;
        }}

        [data-testid="stSidebar"] * {{
            color: var(--sigo-text);
        }}

        h1, h2, h3 {{
            color: var(--sigo-primary-dark);
            letter-spacing: -0.035em;
        }}

        h1 {{
            font-weight: 900;
        }}

        p, label, span, div {{
            color: var(--sigo-text);
        }}

        .stCaptionContainer, [data-testid="stCaptionContainer"] p {{
            color: var(--sigo-muted);
        }}

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, var(--sigo-primary), var(--sigo-primary-dark));
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 12px;
            font-weight: 800;
            box-shadow: var(--sigo-shadow-soft);
            transition: all 0.18s ease;
        }}

        .stButton > button *,
        div[data-testid="stFormSubmitButton"] button * {{
            color: #FFFFFF !important;
        }}

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {{
            transform: translateY(-1px);
            background: linear-gradient(135deg, var(--sigo-primary-dark), #3F050B);
            color: #FFFFFF !important;
            border-color: var(--sigo-gold);
        }}

        .stButton > button:focus,
        .stButton > button:active,
        div[data-testid="stFormSubmitButton"] button:focus {{
            box-shadow: 0 0 0 0.18rem rgba(139, 15, 26, 0.22);
            color: #FFFFFF !important;
            border-color: var(--sigo-primary-dark);
        }}

        .stButton > button:disabled {{
            background: rgba(75, 75, 75, 0.28);
            color: #FFFFFF !important;
            border-color: rgba(75, 75, 75, 0.15);
            box-shadow: none;
            transform: none;
        }}

        [data-testid="stMetric"] {{
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid var(--sigo-border);
            border-radius: var(--sigo-radius);
            padding: 1rem 1.1rem;
            box-shadow: var(--sigo-shadow-soft);
            backdrop-filter: blur(12px);
        }}

        [data-testid="stMetricLabel"] p {{
            color: var(--sigo-muted);
            font-weight: 800;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--sigo-primary-dark);
        }}

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {{
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid var(--sigo-border);
            border-radius: 14px;
            padding: 0.35rem;
            box-shadow: var(--sigo-shadow-soft);
        }}

        [data-testid="stDataFrame"] div[role="columnheader"] {{
            background: rgba(246, 239, 227, 0.95);
            color: var(--sigo-primary-dark);
            font-weight: 900;
        }}

        [data-testid="stAlert"] {{
            border-radius: 14px;
            border: 1px solid var(--sigo-border);
        }}

        input, textarea, [data-baseweb="select"] > div {{
            background: rgba(255, 255, 255, 0.92);
            border-color: var(--sigo-border);
            color: var(--sigo-text);
            border-radius: 12px;
        }}

        input:focus, textarea:focus {{
            border-color: var(--sigo-primary);
            box-shadow: 0 0 0 0.14rem rgba(139, 15, 26, 0.18);
        }}

        [data-testid="stTabs"] button {{
            color: var(--sigo-muted);
            font-weight: 800;
        }}

        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: var(--sigo-primary-dark);
            border-bottom-color: var(--sigo-primary);
        }}

        hr {{
            border-color: var(--sigo-border);
        }}

        .sigo-glass {{
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.38);
            box-shadow: var(--sigo-shadow-soft);
            backdrop-filter: blur(18px);
            border-radius: var(--sigo-radius);
        }}

        .sigo-section {{
            margin-top: 1.15rem;
            margin-bottom: 1.15rem;
        }}

        .sigo-section-title {{
            font-size: 1.15rem;
            font-weight: 900;
            color: var(--sigo-primary-dark);
            margin-bottom: 0.2rem;
        }}

        .sigo-section-subtitle {{
            color: var(--sigo-muted);
            margin-bottom: 0.9rem;
        }}

        .sigo-page-header {{
            padding: 1.45rem 1.55rem;
            border-radius: 22px;
            background:
                linear-gradient(135deg, rgba(139, 15, 26, 0.96), rgba(17, 17, 17, 0.94)),
                radial-gradient(circle at top right, rgba(201, 164, 76, 0.34), transparent 32%);
            box-shadow: var(--sigo-shadow);
            border: 1px solid rgba(255, 255, 255, 0.12);
            margin-bottom: 1.35rem;
        }}

        .sigo-page-header h1 {{
            color: #FFFFFF;
            margin: 0;
            font-size: 2.05rem;
            line-height: 1.08;
        }}

        .sigo-page-header p {{
            color: rgba(255, 249, 240, 0.84);
            margin: 0.5rem 0 0 0;
            max-width: 760px;
        }}

        .sigo-kpi-card {{
            padding: 1.1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--sigo-border);
            box-shadow: var(--sigo-shadow-soft);
            height: 100%;
        }}

        .sigo-kpi-label {{
            color: var(--sigo-muted);
            font-size: 0.86rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .sigo-kpi-value {{
            color: var(--sigo-primary-dark);
            font-size: 1.9rem;
            font-weight: 950;
            line-height: 1.1;
            margin-top: 0.28rem;
        }}

        .sigo-kpi-help {{
            color: var(--sigo-muted);
            font-size: 0.84rem;
            margin-top: 0.3rem;
        }}

        .sigo-module-card {{
            padding: 1.15rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--sigo-border);
            box-shadow: var(--sigo-shadow-soft);
            min-height: 155px;
            transition: all 0.18s ease;
        }}

        .sigo-module-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(201, 164, 76, 0.55);
            box-shadow: var(--sigo-shadow);
        }}

        .sigo-module-icon {{
            width: 42px;
            height: 42px;
            border-radius: 14px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, rgba(139, 15, 26, 0.12), rgba(201, 164, 76, 0.18));
            margin-bottom: 0.72rem;
        }}

        .sigo-module-card svg {{
            width: 24px;
            height: 24px;
            color: var(--sigo-primary-dark);
            stroke: var(--sigo-primary-dark);
        }}

        .sigo-module-title {{
            font-weight: 900;
            color: var(--sigo-primary-dark);
            font-size: 1.03rem;
            margin-bottom: 0.35rem;
        }}

        .sigo-module-desc {{
            color: var(--sigo-muted);
            font-size: 0.88rem;
            line-height: 1.45;
        }}

        .sigo-alert {{
            padding: 0.9rem 1rem;
            border-radius: 16px;
            margin: 0.65rem 0;
            border: 1px solid var(--sigo-border);
            background: rgba(255, 255, 255, 0.82);
            box-shadow: var(--sigo-shadow-soft);
        }}

        .sigo-alert strong {{
            display: block;
            margin-bottom: 0.15rem;
        }}

        .sigo-alert-success {{
            border-left: 5px solid var(--sigo-success);
        }}

        .sigo-alert-info {{
            border-left: 5px solid var(--sigo-info);
        }}

        .sigo-alert-warning {{
            border-left: 5px solid var(--sigo-warning);
        }}

        .sigo-alert-danger {{
            border-left: 5px solid var(--sigo-danger);
        }}

        .sigo-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.28rem 0.62rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 900;
            letter-spacing: 0.02em;
            border: 1px solid transparent;
            white-space: nowrap;
        }}

        .sigo-badge-success {{
            background: rgba(46, 125, 50, 0.12);
            color: var(--sigo-success);
            border-color: rgba(46, 125, 50, 0.22);
        }}

        .sigo-badge-info {{
            background: rgba(21, 101, 192, 0.12);
            color: var(--sigo-info);
            border-color: rgba(21, 101, 192, 0.22);
        }}

        .sigo-badge-warning {{
            background: rgba(249, 168, 37, 0.16);
            color: #8A5A00;
            border-color: rgba(249, 168, 37, 0.28);
        }}

        .sigo-badge-danger {{
            background: rgba(198, 40, 40, 0.12);
            color: var(--sigo-danger);
            border-color: rgba(198, 40, 40, 0.22);
        }}

        .sigo-footer {{
            margin-top: 2rem;
            padding: 1rem 0;
            color: var(--sigo-muted);
            font-size: 0.82rem;
            border-top: 1px solid var(--sigo-border);
            text-align: center;
        }}

        @media (max-width: 760px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .sigo-page-header {{
                padding: 1.1rem;
            }}

            .sigo-page-header h1 {{
                font-size: 1.58rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Alias util por si luego se prefiere llamar la funcion de forma mas explicita.
cargar_css_global = aplicar_estilos


# ============================================================
# 3. COMPONENTES VISUALES REUTILIZABLES
# ============================================================

def mostrar_titulo_pagina(titulo: str, subtitulo: str = "") -> None:
    """Muestra un encabezado consistente para paginas internas."""
    st.markdown(
        f"""
        <div class="sigo-page-header">
            <h1>{escape(titulo)}</h1>
            <p>{escape(subtitulo)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_seccion(titulo: str, subtitulo: str = "") -> None:
    """Muestra un titulo de seccion reutilizable."""
    st.markdown(
        f"""
        <div class="sigo-section">
            <div class="sigo-section-title">{escape(titulo)}</div>
            <div class="sigo-section-subtitle">{escape(subtitulo)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_tarjeta_kpi(
    titulo: str,
    valor: str | int | float,
    ayuda: str = "",
) -> None:
    """Muestra una tarjeta KPI personalizada."""
    st.markdown(
        f"""
        <div class="sigo-kpi-card">
            <div class="sigo-kpi-label">{escape(str(titulo))}</div>
            <div class="sigo-kpi-value">{escape(str(valor))}</div>
            <div class="sigo-kpi-help">{escape(str(ayuda))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_alerta(
    titulo: str,
    mensaje: str,
    tipo: str = "info",
) -> None:
    """Muestra una alerta visual.

    Tipos soportados: success, info, warning, danger.
    """
    tipo_normalizado = tipo if tipo in {"success", "info", "warning", "danger"} else "info"

    st.markdown(
        f"""
        <div class="sigo-alert sigo-alert-{tipo_normalizado}">
            <strong>{escape(titulo)}</strong>
            <span>{escape(mensaje)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def crear_badge_estado(texto: str, tipo: str = "info") -> str:
    """Devuelve HTML de badge para estados en tablas o tarjetas."""
    tipo_normalizado = tipo if tipo in {"success", "info", "warning", "danger"} else "info"

    return (
        f'<span class="sigo-badge sigo-badge-{tipo_normalizado}">'
        f'{escape(texto)}'
        "</span>"
    )


def mostrar_badge_estado(texto: str, tipo: str = "info") -> None:
    """Muestra un badge de estado."""
    st.markdown(crear_badge_estado(texto, tipo), unsafe_allow_html=True)


def mostrar_tarjeta_modulo(
    nombre: str,
    descripcion: str,
    icono_path: Path | str | None = None,
) -> None:
    """Muestra una tarjeta visual para un modulo del sistema."""
    svg = _leer_svg(icono_path)
    icono_html = svg if svg else "•"

    st.markdown(
        f"""
        <div class="sigo-module-card">
            <div class="sigo-module-icon">{icono_html}</div>
            <div class="sigo-module-title">{escape(nombre)}</div>
            <div class="sigo-module-desc">{escape(descripcion)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_grid_modulos(modulos: list[dict[str, Any]] | None = None) -> None:
    """Muestra los modulos configurados en tarjetas de 3 columnas."""
    lista_modulos = modulos if modulos is not None else MODULOS_APP

    if not lista_modulos:
        mostrar_alerta(
            "Modulos no configurados",
            "No se encontraron modulos para mostrar en la interfaz.",
            "warning",
        )
        return

    columnas = st.columns(3)
    for indice, modulo in enumerate(lista_modulos):
        with columnas[indice % 3]:
            mostrar_tarjeta_modulo(
                nombre=str(modulo.get("nombre", "Modulo")),
                descripcion=str(modulo.get("descripcion", "")),
                icono_path=modulo.get("icono"),
            )


def mostrar_footer(texto: str | None = None) -> None:
    """Muestra un footer institucional simple."""
    contenido = texto or TEXTOS_APP.get("footer", "SIGO-PRO FoodOps")
    st.markdown(
        f"""
        <div class="sigo-footer">
            {escape(contenido)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_resumen_empresa() -> None:
    """Muestra una tarjeta breve con datos de la empresa piloto."""
    nombre = EMPRESA.get("nombre_comercial", "Gourmet Senor de Locumba")
    ruc = EMPRESA.get("ruc", "20612215546")
    ubicacion = EMPRESA.get("ubicacion", "Tiabaya, Arequipa")
    rubro = EMPRESA.get("rubro", "Servicios de alimentacion")

    st.markdown(
        f"""
        <div class="sigo-glass" style="padding: 1rem 1.1rem; margin-bottom: 1rem;">
            <div style="font-weight: 900; color: var(--sigo-primary-dark); font-size: 1.05rem;">
                {escape(nombre)}
            </div>
            <div style="color: var(--sigo-muted); font-size: 0.9rem; margin-top: 0.25rem;">
                RUC {escape(ruc)} · {escape(ubicacion)}
            </div>
            <div style="color: var(--sigo-muted); font-size: 0.86rem; margin-top: 0.25rem;">
                {escape(rubro)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_hero_inicio() -> None:
    """Muestra una seccion hero para la portada.

    Esta funcion se usara principalmente en app.py o pages/1_Inicio.py.
    Por ahora usa imagen de fondo estatica. El video se puede agregar en una
    fase posterior sin cambiar la estructura visual.
    """
    hero_uri = _path_to_data_uri(ASSETS.get("hero"))
    fallback_uri = _path_to_data_uri(ASSETS.get("fallback"))
    background_uri = hero_uri or fallback_uri

    background_css = (
        f"background-image: linear-gradient(90deg, rgba(17,17,17,0.88), "
        f"rgba(17,17,17,0.48), rgba(17,17,17,0.18)), url('{background_uri}');"
        if background_uri
        else "background: linear-gradient(135deg, #111111, #5E0810);"
    )

    titulo = TEXTOS_APP.get("titulo", "SIGO-PRO FoodOps")
    subtitulo = TEXTOS_APP.get("subtitulo", "Gestion operativa inteligente")
    hero_titulo = TEXTOS_APP.get("hero_titulo", "")
    hero_descripcion = TEXTOS_APP.get("hero_descripcion", "")

    st.markdown(
        f"""
        <div style="
            {background_css}
            background-size: cover;
            background-position: center;
            min-height: 520px;
            border-radius: 28px;
            padding: 1.4rem;
            display: flex;
            align-items: flex-end;
            box-shadow: var(--sigo-shadow);
            border: 1px solid rgba(255,255,255,0.14);
            overflow: hidden;
            margin-bottom: 1.4rem;
        ">
            <div style="
                max-width: 720px;
                padding: 1.45rem;
                border-radius: 24px;
                background: rgba(255,255,255,0.12);
                border: 1px solid rgba(255,255,255,0.22);
                backdrop-filter: blur(18px);
            ">
                <div style="
                    display: inline-flex;
                    padding: 0.32rem 0.68rem;
                    border-radius: 999px;
                    background: rgba(201,164,76,0.18);
                    border: 1px solid rgba(201,164,76,0.35);
                    color: #F6EFE3;
                    font-weight: 900;
                    font-size: 0.78rem;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    margin-bottom: 0.8rem;
                ">
                    {escape(subtitulo)}
                </div>
                <h1 style="
                    color: #FFFFFF;
                    font-size: 3rem;
                    line-height: 0.98;
                    margin: 0 0 0.55rem 0;
                    font-weight: 950;
                    letter-spacing: -0.055em;
                ">
                    {escape(titulo)}
                </h1>
                <h2 style="
                    color: #FFF9F0;
                    font-size: 1.42rem;
                    line-height: 1.2;
                    margin: 0 0 0.65rem 0;
                    font-weight: 850;
                    letter-spacing: -0.025em;
                ">
                    {escape(hero_titulo)}
                </h2>
                <p style="
                    color: rgba(255,249,240,0.84);
                    font-size: 0.98rem;
                    line-height: 1.55;
                    margin: 0;
                ">
                    {escape(hero_descripcion)}
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 4. COMPATIBILIDAD CON TABLAS / SELECCIONES
# ============================================================

def obtener_filas_seleccionadas(evento) -> list[int]:
    """Extrae indices seleccionados desde eventos de Streamlit.

    Streamlit puede devolver eventos como objetos o como diccionarios segun la
    version/componente. Esta funcion soporta ambos formatos y devuelve siempre
    una lista simple de filas.
    """
    if evento is None:
        return []

    seleccion = getattr(evento, "selection", None)
    if seleccion is None and isinstance(evento, dict):
        seleccion = evento.get("selection")

    if seleccion is None:
        return []

    filas = getattr(seleccion, "rows", None)
    if filas is None and isinstance(seleccion, dict):
        filas = seleccion.get("rows")

    return list(filas or [])