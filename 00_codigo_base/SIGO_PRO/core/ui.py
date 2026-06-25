"""Utilidades compartidas para la interfaz Streamlit."""

import streamlit as st


def aplicar_estilos() -> None:
    """Inyecta el CSS corporativo usado por todas las paginas."""
    st.markdown(
        """
        <style>
        :root {
            --sigo-primary: #A5211C;
            --sigo-primary-dark: #7F1713;
            --sigo-terracotta: #BD5E57;
            --sigo-bg: #F4EBD8;
            --sigo-card: #FBF6EF;
            --sigo-border: #D6CAC0;
            --sigo-text: #2B211E;
            --sigo-muted: #6B5A55;
            --sigo-white: #FFFFFF;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background: var(--sigo-bg);
            color: var(--sigo-text);
        }

        [data-testid="stHeader"] {
            background: rgba(244, 235, 216, 0.92);
            border-bottom: 1px solid var(--sigo-border);
        }

        [data-testid="stSidebar"] {
            background: var(--sigo-card);
            border-right: 1px solid var(--sigo-border);
        }

        [data-testid="stSidebarNav"]::before {
            content: "SIGO-PRO FoodOps";
            display: block;
            padding: 1.1rem 1.1rem 0.85rem 1.1rem;
            color: var(--sigo-primary-dark);
            font-size: 1.05rem;
            font-weight: 800;
            letter-spacing: 0;
            border-bottom: 1px solid var(--sigo-border);
            margin-bottom: 0.55rem;
        }

        [data-testid="stSidebarNav"] ul li:first-child {
            display: none;
        }

        [data-testid="stSidebar"] * {
            color: var(--sigo-text);
        }

        h1, h2, h3 {
            color: var(--sigo-primary-dark);
            letter-spacing: 0;
        }

        p, label, span, div {
            color: var(--sigo-text);
        }

        .stCaptionContainer, [data-testid="stCaptionContainer"] p {
            color: var(--sigo-muted);
        }

        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            background: var(--sigo-primary);
            color: var(--sigo-white) !important;
            border: 1px solid var(--sigo-primary);
            border-radius: 8px;
            font-weight: 600;
        }

        .stButton > button *,
        div[data-testid="stFormSubmitButton"] button * {
            color: var(--sigo-white) !important;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            background: var(--sigo-primary-dark);
            color: var(--sigo-white) !important;
            border-color: var(--sigo-primary-dark);
        }

        .stButton > button:focus,
        .stButton > button:active,
        div[data-testid="stFormSubmitButton"] button:focus {
            box-shadow: 0 0 0 0.18rem rgba(165, 33, 28, 0.22);
            color: var(--sigo-white) !important;
            border-color: var(--sigo-primary-dark);
        }

        .stButton > button[kind="secondary"] {
            background: var(--sigo-primary);
            color: var(--sigo-white) !important;
            border-color: var(--sigo-primary);
        }

        .stButton > button:disabled {
            background: var(--sigo-border);
            color: var(--sigo-white) !important;
            border-color: var(--sigo-border);
        }

        [data-testid="stMetric"] {
            background: var(--sigo-card);
            border: 1px solid var(--sigo-border);
            border-radius: 12px;
            padding: 1rem 1.1rem;
            box-shadow: 0 1px 2px rgba(43, 33, 30, 0.06);
        }

        [data-testid="stMetricLabel"] p {
            color: var(--sigo-muted);
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--sigo-primary-dark);
        }

        div[data-testid="stDialog"] [data-testid="stMetric"] {
            padding: 0.75rem 0.85rem;
        }

        div[data-testid="stDialog"] [data-testid="stMetricLabel"] p {
            font-size: 0.78rem;
            line-height: 1.1;
            white-space: normal;
        }

        div[data-testid="stDialog"] [data-testid="stMetricValue"] {
            font-size: 1.35rem;
            line-height: 1.15;
            white-space: normal;
        }

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: var(--sigo-card);
            border: 1px solid var(--sigo-border);
            border-radius: 10px;
            padding: 0.35rem;
        }

        [data-testid="stDataFrame"] div[role="columnheader"] {
            background: var(--sigo-card);
            color: var(--sigo-primary-dark);
            font-weight: 700;
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
            border: 1px solid var(--sigo-border);
        }

        [data-testid="stInfo"] {
            background: var(--sigo-card);
        }

        input, textarea, [data-baseweb="select"] > div {
            background: var(--sigo-white);
            border-color: var(--sigo-border);
            color: var(--sigo-text);
        }

        input:focus, textarea:focus {
            border-color: var(--sigo-primary);
            box-shadow: 0 0 0 0.14rem rgba(165, 33, 28, 0.18);
        }

        [data-testid="stTabs"] button {
            color: var(--sigo-muted);
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--sigo-primary-dark);
            border-bottom-color: var(--sigo-primary);
        }

        div[data-testid="stDialog"] {
            background: var(--sigo-card) !important;
            border: 1px solid var(--sigo-border) !important;
            border-radius: 12px !important;
            box-shadow: 0 18px 42px rgba(43, 33, 30, 0.22) !important;
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: calc(100vw - 2rem) !important;
            height: calc(100vh - 2rem) !important;
            max-width: calc(100vw - 2rem) !important;
            max-height: calc(100vh - 2rem) !important;
            overflow: hidden !important;
            margin: 0 !important;
        }

        div[data-testid="stDialog"] > div {
            background: var(--sigo-card) !important;
            border-radius: 12px !important;
            width: 100% !important;
            max-width: 100% !important;
            height: 100% !important;
            max-height: 100% !important;
            overflow-y: auto !important;
            padding: 1.25rem 1.5rem 1.5rem 1.5rem !important;
        }

        div[data-testid="stDialog"] h2 {
            color: var(--sigo-primary-dark) !important;
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
            margin-bottom: 0.75rem !important;
        }

        div[data-testid="stDialog"] section,
        div[data-testid="stDialog"] form,
        div[data-testid="stDialog"] [data-testid="stVerticalBlock"],
        div[data-testid="stDialog"] [data-testid="stHorizontalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        div[data-testid="stDialog"] [data-testid="stForm"] {
            background: transparent !important;
            border: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stDialog"] [data-testid="stDataFrame"] {
            background: var(--sigo-white) !important;
        }

        @media (max-width: 760px) {
            div[data-testid="stDialog"] {
                width: calc(100vw - 1rem) !important;
                height: calc(100vh - 1rem) !important;
                max-width: calc(100vw - 1rem) !important;
                max-height: calc(100vh - 1rem) !important;
            }

            div[data-testid="stDialog"] > div {
                padding: 1rem !important;
            }
        }

        hr {
            border-color: var(--sigo-border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
