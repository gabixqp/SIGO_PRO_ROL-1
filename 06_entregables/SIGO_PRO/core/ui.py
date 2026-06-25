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
    ASSETS = {}
    MODULOS_APP = []
    EMPRESA = {
        "nombre_comercial": "Gourmet Senor de Locumba",
        "ruc": "20612215546",
        "ubicacion": "Tiabaya, Arequipa",
        "rubro": "Servicios de alimentacion",
        "sistema": "SIGO-PRO FoodOps",
    }
    TEXTOS_APP = {
        "titulo": "SIGO-PRO FoodOps",
        "subtitulo": "Gestion operativa inteligente para servicios de alimentacion",
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



def _resolver_logo_sidebar() -> Path | None:
    """Busca el logo para la barra lateral.

    Prioriza ASSETS["logo_gourmet"] si existe en config.py. Si no esta
    configurado, revisa carpetas comunes del proyecto y toma otro archivo de
    logo distinto a logo_principal. Esto permite cambiar el logo sin tocar el
    codigo: basta con agregarlo en assets/ o declararlo en config.py.
    """
    claves_preferidas = [
        # Logo solicitado para la barra lateral.
        # Debe existir en config.py dentro del diccionario ASSETS, por ejemplo:
        # "logo_gourmet": ASSETS_DIR / "logo_gourmet.png"
        "logo_gourmet",
        "logo_sidebar",
        "logo_lateral",
        "logo_secundario",
        "logo_alterno",
        "logo_alt",
        "logo_horizontal",
        "logo_completo",
        "logo_foodops",
        "logo_sigo",
        "marca",
        "isotipo",
        "logo",
    ]

    for clave in claves_preferidas:
        valor = ASSETS.get(clave) if isinstance(ASSETS, dict) else None
        if valor:
            ruta = Path(valor)
            if ruta.exists() and ruta.is_file():
                return ruta

    ruta_principal = None
    valor_principal = ASSETS.get("logo_principal") if isinstance(ASSETS, dict) else None
    if valor_principal:
        posible_principal = Path(valor_principal)
        if posible_principal.exists() and posible_principal.is_file():
            ruta_principal = posible_principal.resolve()

    carpetas: list[Path] = []
    base_actual = Path(__file__).resolve().parent
    carpetas.extend([
        base_actual,
        base_actual / "assets",
        base_actual / "assets" / "logos",
        base_actual / "imagenes",
        base_actual / "img",
        Path.cwd() / "assets",
        Path.cwd() / "assets" / "logos",
        Path.cwd() / "imagenes",
        Path.cwd() / "img",
    ])

    if isinstance(ASSETS, dict):
        for valor in ASSETS.values():
            if valor:
                ruta = Path(valor)
                if ruta.parent.exists():
                    carpetas.append(ruta.parent)

    extensiones = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
    candidatos: list[Path] = []
    carpetas_unicas: list[Path] = []

    for carpeta in carpetas:
        if carpeta not in carpetas_unicas:
            carpetas_unicas.append(carpeta)

    for carpeta in carpetas_unicas:
        if not carpeta.exists() or not carpeta.is_dir():
            continue
        for archivo in carpeta.iterdir():
            nombre = archivo.stem.lower()
            if archivo.is_file() and archivo.suffix.lower() in extensiones and "logo" in nombre:
                if ruta_principal and archivo.resolve() == ruta_principal:
                    continue
                candidatos.append(archivo)

    if candidatos:
        prioridad = [
            "sidebar",
            "lateral",
            "secundario",
            "alterno",
            "alt",
            "horizontal",
            "completo",
            "foodops",
            "sigo",
            "logo2",
            "logo_2",
            "logo",
        ]

        def puntaje(ruta: Path) -> tuple[int, str]:
            nombre = ruta.stem.lower()
            for indice, palabra in enumerate(prioridad):
                if palabra in nombre:
                    return indice, nombre
            return 999, nombre

        return sorted(candidatos, key=puntaje)[0]

    if ruta_principal:
        return ruta_principal

    return None


def _obtener_logo_sidebar_uri() -> str:
    """Devuelve el logo de la barra lateral como data URI."""
    return _path_to_data_uri(_resolver_logo_sidebar())


# ============================================================
# 2. CSS GLOBAL
# ============================================================

def aplicar_estilos() -> None:
    """Inyecta el CSS corporativo usado por todas las paginas."""
    logo_uri = _obtener_logo_sidebar_uri()

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
            --sigo-border: rgba(94, 8, 16, 0.14);
            --sigo-border-strong: rgba(94, 8, 16, 0.22);
            --sigo-text: #2B211E;
            --sigo-muted: {_color("gris_medio")};
            --sigo-success: {_color("verde")};
            --sigo-warning: {_color("amarillo")};
            --sigo-danger: {_color("rojo_alerta")};
            --sigo-info: {_color("azul_info")};
            --sigo-shadow: 0 22px 52px rgba(17, 17, 17, 0.14);
            --sigo-shadow-soft: 0 10px 26px rgba(17, 17, 17, 0.08);
            --sigo-shadow-glow: 0 20px 70px rgba(139, 15, 26, 0.16);
            --sigo-radius: 20px;
        }}

        html,
        body,
        [data-testid="stAppViewContainer"],
        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(201, 164, 76, 0.16), transparent 34%),
                radial-gradient(circle at bottom right, rgba(139, 15, 26, 0.08), transparent 30%),
                linear-gradient(135deg, var(--sigo-bg) 0%, var(--sigo-bg-soft) 48%, #EFE1CB 100%);
            color: var(--sigo-text);
        }}

        .block-container {{
            padding-top: 1.95rem;
            padding-bottom: 3rem;
            max-width: 1320px;
        }}

        [data-testid="stHeader"] {{
            background: rgba(246, 239, 227, 0.76);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-bottom: 1px solid var(--sigo-border);
        }}

        /* =====================================================
           Barra lateral premium
        ===================================================== */

        section[data-testid="stSidebar"],
        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(255, 249, 240, 0.99) 0%, rgba(246, 239, 227, 0.98) 52%, rgba(239, 225, 203, 0.98) 100%) !important;
            border-right: 1px solid var(--sigo-border) !important;
            box-shadow: 10px 0 30px rgba(17, 17, 17, 0.06);
        }}

        section[data-testid="stSidebar"] .block-container,
        [data-testid="stSidebar"] .block-container {{
            padding-top: 1.15rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }}

        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            width: 160px;
            height: 160px;
            margin: 0.9rem auto 1.15rem auto;
            border-radius: 50%;
            background-color: #1A1314;
            background-image: url("{logo_uri}");
            background-size: 76%;
            background-position: center;
            background-repeat: no-repeat;
            border: 1px solid rgba(226, 200, 120, 0.20);
            box-shadow: 
                0 16px 36px rgba(0, 0, 0, 0.28),
                inset 0 1px 6px rgba(255, 255, 255, 0.04);
        }}

        [data-testid="stSidebarNav"] ul li:first-child {{
            display: none !important;
        }}

        [data-testid="stSidebarNav"] ul {{
            padding: 0 0.55rem 0.5rem 0.55rem;
            gap: 0.18rem;
        }}

        [data-testid="stSidebarNav"] ul li {{
            margin-bottom: 0.2rem;
        }}

        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavLink"] {{
            border-radius: 15px !important;
            padding: 0.72rem 0.9rem !important;
            min-height: 45px;
            color: var(--sigo-text) !important;
            font-weight: 800 !important;
            letter-spacing: -0.01em;
            transition: all 0.18s ease !important;
            border: 1px solid transparent !important;
            background: transparent !important;
        }}

        [data-testid="stSidebarNav"] a span,
        [data-testid="stSidebarNavLink"] span {{
            color: inherit !important;
            font-weight: inherit !important;
        }}

        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNavLink"]:hover {{
            background: rgba(255, 255, 255, 0.78) !important;
            color: var(--sigo-primary-dark) !important;
            border-color: rgba(139, 15, 26, 0.14) !important;
            box-shadow: 0 8px 18px rgba(17, 17, 17, 0.06);
            transform: translateX(4px);
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"],
        [data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: linear-gradient(135deg, var(--sigo-primary), var(--sigo-primary-dark)) !important;
            color: #FFFFFF !important;
            border-color: rgba(255, 255, 255, 0.20) !important;
            box-shadow: 0 14px 30px rgba(94, 8, 16, 0.25);
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] span,
        [data-testid="stSidebarNavLink"][aria-current="page"] span {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] hr,
        [data-testid="stSidebar"] hr {{
            border-color: var(--sigo-border);
        }}

        /* =====================================================
           Tipografia y componentes base
        ===================================================== */

        h1,
        h2,
        h3 {{
            color: var(--sigo-primary-dark);
            letter-spacing: -0.035em;
        }}

        h1 {{
            font-weight: 950;
        }}

        p,
        label,
        span,
        div {{
            color: var(--sigo-text);
        }}

        .stCaptionContainer,
        [data-testid="stCaptionContainer"] p {{
            color: var(--sigo-muted);
        }}

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, var(--sigo-primary), var(--sigo-primary-dark));
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 13px;
            font-weight: 850;
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
            background: rgba(75, 75, 75, 0.28) !important;
            color: #FFFFFF !important;
            border-color: rgba(75, 75, 75, 0.15);
            box-shadow: none;
            transform: none;
        }}

        [data-testid="stMetric"] {{
            background: rgba(255, 255, 255, 0.80);
            border: 1px solid var(--sigo-border);
            border-radius: var(--sigo-radius);
            padding: 1rem 1.1rem;
            box-shadow: var(--sigo-shadow-soft);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}

        [data-testid="stMetricLabel"] p {{
            color: var(--sigo-muted);
            font-weight: 850;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--sigo-primary-dark);
        }}

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {{
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid var(--sigo-border);
            border-radius: 16px;
            padding: 0.35rem;
            box-shadow: var(--sigo-shadow-soft);
        }}

        [data-testid="stDataFrame"] div[role="columnheader"] {{
            background: rgba(246, 239, 227, 0.95);
            color: var(--sigo-primary-dark);
            font-weight: 900;
        }}

        [data-testid="stAlert"] {{
            border-radius: 15px;
            border: 1px solid var(--sigo-border);
        }}

        input,
        textarea,
        [data-baseweb="select"] > div {{
            background: rgba(255, 255, 255, 0.92);
            border-color: var(--sigo-border);
            color: var(--sigo-text);
            border-radius: 12px;
        }}

        input:focus,
        textarea:focus {{
            border-color: var(--sigo-primary);
            box-shadow: 0 0 0 0.14rem rgba(139, 15, 26, 0.18);
        }}

        [data-testid="stTabs"] button {{
            color: var(--sigo-muted);
            font-weight: 850;
        }}

        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: var(--sigo-primary-dark);
            border-bottom-color: var(--sigo-primary);
        }}

        hr {{
            border-color: var(--sigo-border);
        }}

        /* =====================================================
           Tarjetas y bloques reutilizables
        ===================================================== */

        .sigo-glass,
        .sigo-info-card,
        .sigo-kpi-card,
        .sigo-module-card {{
            background: rgba(255, 255, 255, 0.84);
            border: 1px solid rgba(255, 255, 255, 0.56);
            box-shadow: var(--sigo-shadow-soft);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-radius: var(--sigo-radius);
        }}

        .sigo-section {{
            margin-top: 1.15rem;
            margin-bottom: 1.15rem;
        }}

        .sigo-section-title {{
            font-size: 1.18rem;
            font-weight: 950;
            color: var(--sigo-primary-dark);
            margin-bottom: 0.2rem;
        }}

        .sigo-section-subtitle {{
            color: var(--sigo-muted);
            margin-bottom: 0.9rem;
        }}

        .sigo-page-header {{
            padding: 1.5rem 1.6rem;
            border-radius: 24px;
            background:
                radial-gradient(circle at top right, rgba(201, 164, 76, 0.35), transparent 32%),
                linear-gradient(135deg, rgba(139, 15, 26, 0.97), rgba(17, 17, 17, 0.95));
            box-shadow: var(--sigo-shadow);
            border: 1px solid rgba(255, 255, 255, 0.13);
            margin-bottom: 1.35rem;
        }}

        .sigo-page-header h1 {{
            color: #FFFFFF !important;
            margin: 0;
            font-size: 2.15rem;
            line-height: 1.06;
            text-shadow: 0 5px 20px rgba(0, 0, 0, 0.28);
        }}

        .sigo-page-header p {{
            color: rgba(255, 249, 240, 0.86) !important;
            margin: 0.52rem 0 0 0;
            max-width: 780px;
        }}

        .sigo-kpi-card {{
            padding: 1.14rem;
            height: 100%;
            border: 1px solid var(--sigo-border);
            transition: all 0.18s ease;
        }}

        .sigo-kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--sigo-shadow);
        }}

        .sigo-kpi-label {{
            color: var(--sigo-muted);
            font-size: 0.82rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.055em;
        }}

        .sigo-kpi-value {{
            color: var(--sigo-primary-dark);
            font-size: 2rem;
            font-weight: 950;
            line-height: 1.08;
            margin-top: 0.3rem;
        }}

        .sigo-kpi-help {{
            color: var(--sigo-muted);
            font-size: 0.86rem;
            margin-top: 0.32rem;
        }}

        .sigo-module-card {{
            padding: 1.18rem;
            border: 1px solid var(--sigo-border);
            min-height: 160px;
            transition: all 0.18s ease;
        }}

        .sigo-module-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(201, 164, 76, 0.58);
            box-shadow: var(--sigo-shadow);
        }}

        .sigo-module-icon {{
            width: 44px;
            height: 44px;
            border-radius: 15px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, rgba(139, 15, 26, 0.12), rgba(201, 164, 76, 0.18));
            margin-bottom: 0.76rem;
            color: var(--sigo-primary-dark);
            font-weight: 900;
        }}

        .sigo-module-card svg {{
            width: 24px;
            height: 24px;
            color: var(--sigo-primary-dark);
            stroke: var(--sigo-primary-dark);
        }}

        .sigo-module-title {{
            font-weight: 950;
            color: var(--sigo-primary-dark);
            font-size: 1.06rem;
            margin-bottom: 0.35rem;
        }}

        .sigo-module-desc {{
            color: var(--sigo-muted);
            font-size: 0.9rem;
            line-height: 1.48;
        }}

        .sigo-alert {{
            padding: 0.92rem 1rem;
            border-radius: 16px;
            margin: 0.65rem 0;
            border: 1px solid var(--sigo-border);
            background: rgba(255, 255, 255, 0.84);
            box-shadow: var(--sigo-shadow-soft);
        }}

        .sigo-alert strong {{
            display: block;
            margin-bottom: 0.15rem;
            color: var(--sigo-primary-dark);
        }}

        .sigo-alert-success {{ border-left: 5px solid var(--sigo-success); }}
        .sigo-alert-info {{ border-left: 5px solid var(--sigo-info); }}
        .sigo-alert-warning {{ border-left: 5px solid var(--sigo-warning); }}
        .sigo-alert-danger {{ border-left: 5px solid var(--sigo-danger); }}

        .sigo-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.3rem 0.68rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 900;
            letter-spacing: 0.025em;
            border: 1px solid transparent;
            white-space: nowrap;
        }}

        .sigo-badge-success {{
            background: rgba(46, 125, 50, 0.12);
            color: var(--sigo-success) !important;
            border-color: rgba(46, 125, 50, 0.22);
        }}

        .sigo-badge-info {{
            background: rgba(21, 101, 192, 0.12);
            color: var(--sigo-info) !important;
            border-color: rgba(21, 101, 192, 0.22);
        }}

        .sigo-badge-warning {{
            background: rgba(249, 168, 37, 0.16);
            color: #8A5A00 !important;
            border-color: rgba(249, 168, 37, 0.28);
        }}

        .sigo-badge-danger {{
            background: rgba(198, 40, 40, 0.12);
            color: var(--sigo-danger) !important;
            border-color: rgba(198, 40, 40, 0.22);
        }}

        /* =====================================================
           Hero / portada
        ===================================================== */

        .sigo-hero-wrapper {{
            position: relative;
            min-height: 548px;
            border-radius: 32px;
            padding: 1.65rem;
            display: flex;
            align-items: flex-end;
            background-size: cover;
            background-position: center;
            box-shadow: var(--sigo-shadow), var(--sigo-shadow-glow);
            border: 1px solid rgba(255, 255, 255, 0.15);
            overflow: hidden;
            margin-bottom: 1.45rem;
            isolation: isolate;
        }}

        .sigo-hero-wrapper::before {{
            content: "";
            position: absolute;
            inset: 0;
            z-index: 0;
            background:
                radial-gradient(circle at 23% 22%, rgba(201, 164, 76, 0.18), transparent 34%),
                linear-gradient(90deg, rgba(17, 17, 17, 0.80) 0%, rgba(17, 17, 17, 0.54) 43%, rgba(17, 17, 17, 0.18) 100%);
        }}

        .sigo-hero-wrapper::after {{
            content: "";
            position: absolute;
            inset: auto 0 0 0;
            height: 38%;
            z-index: 0;
            background: linear-gradient(0deg, rgba(0, 0, 0, 0.38), transparent);
        }}

        .sigo-hero-panel {{
            position: relative;
            z-index: 2;
            max-width: 805px;
            padding: 2rem 2.1rem;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(17, 17, 17, 0.62), rgba(43, 33, 30, 0.44));
            border: 1px solid rgba(255, 255, 255, 0.24);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
        }}

        .sigo-hero-eyebrow {{
            display: inline-flex;
            align-items: center;
            padding: 0.46rem 0.95rem;
            border-radius: 999px;
            background: rgba(201, 164, 76, 0.22);
            border: 1px solid rgba(226, 200, 120, 0.58);
            color: #FFF4C7 !important;
            font-weight: 950;
            font-size: 0.78rem;
            letter-spacing: 0.085em;
            text-transform: uppercase;
            margin-bottom: 1.05rem;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.45);
        }}

        .sigo-hero-title {{
            color: #FFFFFF !important;
            font-size: clamp(3.15rem, 6.3vw, 5.85rem) !important;
            line-height: 0.92 !important;
            margin: 0 0 0.95rem 0 !important;
            font-weight: 950 !important;
            letter-spacing: -0.078em !important;
            text-shadow:
                0 5px 18px rgba(0, 0, 0, 0.48),
                0 16px 42px rgba(0, 0, 0, 0.35) !important;
        }}

        .sigo-hero-title span {{
            color: var(--sigo-gold-soft) !important;
            text-shadow:
                0 5px 18px rgba(0, 0, 0, 0.48),
                0 0 24px rgba(226, 200, 120, 0.28) !important;
        }}

        .sigo-hero-subtitle {{
            color: #FFF9F0 !important;
            font-size: clamp(1.18rem, 2vw, 1.7rem) !important;
            line-height: 1.22 !important;
            margin: 0 0 0.95rem 0 !important;
            font-weight: 900 !important;
            letter-spacing: -0.035em;
            text-shadow: 0 4px 18px rgba(0, 0, 0, 0.42);
        }}

        .sigo-hero-description {{
            color: rgba(255, 249, 240, 0.92) !important;
            font-size: 1.04rem !important;
            line-height: 1.68 !important;
            margin: 0 !important;
            max-width: 705px;
            text-shadow: 0 3px 14px rgba(0, 0, 0, 0.42);
        }}

        /* =====================================================
           Tarjeta resumen empresa
        ===================================================== */

        .sigo-info-card {{
            position: relative;
            padding: 1.35rem 1.45rem;
            margin-bottom: 1.15rem;
            border: 1px solid rgba(94, 8, 16, 0.10);
            overflow: hidden;
        }}

        .sigo-info-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 6px;
            background: linear-gradient(180deg, var(--sigo-primary), var(--sigo-gold));
        }}

        .sigo-info-title {{
            font-weight: 950;
            color: var(--sigo-primary-dark);
            font-size: 1.28rem;
            letter-spacing: -0.035em;
        }}

        .sigo-info-meta {{
            color: var(--sigo-muted);
            font-size: 0.94rem;
            margin-top: 0.18rem;
        }}

        .sigo-info-rubro {{
            color: #4d4642;
            font-size: 0.94rem;
            line-height: 1.55;
            margin-top: 0.45rem;
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
                padding-top: 1rem;
            }}

            .sigo-page-header {{
                padding: 1.15rem;
                border-radius: 20px;
            }}

            .sigo-page-header h1 {{
                font-size: 1.62rem;
            }}

            .sigo-hero-wrapper {{
                min-height: 520px;
                padding: 1rem;
                border-radius: 24px;
                align-items: flex-end;
            }}

            .sigo-hero-panel {{
                padding: 1.35rem;
                border-radius: 22px;
            }}

            .sigo-hero-title {{
                font-size: clamp(2.45rem, 14vw, 3.55rem) !important;
                letter-spacing: -0.065em !important;
            }}

            .sigo-hero-subtitle {{
                font-size: 1.12rem !important;
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
    estado = EMPRESA.get("estado", "Activo")
    condicion = EMPRESA.get("condicion", "Habido")

    st.markdown(
        f"""
        <div class="sigo-info-card">
            <div class="sigo-info-title">{escape(nombre)}</div>
            <div class="sigo-info-meta">RUC {escape(ruc)} · {escape(ubicacion)}</div>
            <div class="sigo-info-rubro">{escape(rubro)}</div>
            <div style="margin-top: 0.75rem;">
                {crear_badge_estado(estado, "success")}
                {crear_badge_estado(condicion, "info")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_hero_inicio() -> None:
    """Muestra una seccion hero para la portada.

    Importante: el HTML se envia sin sangrias ni lineas vacias para que
    Streamlit no lo interprete como bloque de codigo Markdown.
    """
    hero_uri = _path_to_data_uri(ASSETS.get("hero"))
    fallback_uri = _path_to_data_uri(ASSETS.get("fallback"))
    background_uri = hero_uri or fallback_uri

    background_style = (
        f"background-image: url('{background_uri}');"
        if background_uri
        else "background: linear-gradient(135deg, #111111, #5E0810);"
    )

    titulo = TEXTOS_APP.get("titulo", "SIGO-PRO FoodOps")
    subtitulo = TEXTOS_APP.get(
        "subtitulo",
        "Gestion operativa inteligente para servicios de alimentacion",
    )
    hero_titulo = TEXTOS_APP.get(
        "hero_titulo",
        "Gestiona pedidos, produccion, inventario y costos desde un solo lugar.",
    )
    hero_descripcion = TEXTOS_APP.get(
        "hero_descripcion",
        "Sistema desarrollado para Gourmet Senor de Locumba S.A.C., orientado a mejorar el control operativo, la toma de decisiones y la experiencia de gestion interna.",
    )

    titulo_seguro = escape(str(titulo))
    titulo_html = titulo_seguro.replace("FoodOps", "<span>FoodOps</span>")

    html = (
        f'<div class="sigo-hero-wrapper" style="{background_style}">'
        f'<div class="sigo-hero-panel">'
        f'<div class="sigo-hero-eyebrow">{escape(str(subtitulo))}</div>'
        f'<h1 class="sigo-hero-title">{titulo_html}</h1>'
        f'<div class="sigo-hero-subtitle">{escape(str(hero_titulo))}</div>'
        f'<div class="sigo-hero-description">{escape(str(hero_descripcion))}</div>'
        f'</div>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def mostrar_metricas_inicio() -> None:
    """Muestra indicadores visuales de portada para elevar el diseno."""
    columnas = st.columns(4)
    metricas = [
        ("Pedidos", "Control diario", "Registro y seguimiento operativo"),
        ("Produccion", "Planificada", "Preparacion segun demanda"),
        ("Inventario", "Alertas", "Stock critico y reposicion"),
        ("Costos", "Analisis", "Margenes y rentabilidad"),
    ]

    for columna, (titulo, valor, ayuda) in zip(columnas, metricas):
        with columna:
            mostrar_tarjeta_kpi(titulo, valor, ayuda)


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