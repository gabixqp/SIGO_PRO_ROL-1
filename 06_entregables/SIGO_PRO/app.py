"""Punto de entrada principal de la aplicacion Streamlit.

Este archivo configura la portada del sistema SIGO-PRO FoodOps.
Las pantallas funcionales viven en la carpeta pages/ y Streamlit las muestra
automaticamente en la barra lateral.

Rol 1 - Integrador:
- Configuracion global de la app.
- Aplicacion de identidad visual.
- Portada profesional.
- Acceso visual a modulos.
- Resumen ejecutivo inicial.
"""

from __future__ import annotations

import csv
from pathlib import Path

import streamlit as st

from config import (
    APP_CONFIG,
    ARCHIVOS_CSV,
    DATA_DIR,
    EMPRESA,
    MODULOS_APP,
    TEXTOS_APP,
    crear_carpetas_base,
)
from core.ui import (
    aplicar_estilos,
    mostrar_alerta,
    mostrar_footer,
    mostrar_grid_modulos,
    mostrar_hero_inicio,
    mostrar_resumen_empresa,
    mostrar_seccion,
    mostrar_tarjeta_kpi,
)


# ============================================================
# 1. CONFIGURACION GLOBAL
# ============================================================

st.set_page_config(
    page_title=APP_CONFIG.get("page_title", "SIGO-PRO FoodOps"),
    page_icon=APP_CONFIG.get("page_icon", "🍽️"),
    layout=APP_CONFIG.get("layout", "wide"),
    initial_sidebar_state=APP_CONFIG.get("initial_sidebar_state", "expanded"),
)

crear_carpetas_base()
aplicar_estilos()


# ============================================================
# 2. FUNCIONES LOCALES DE PORTADA
# ============================================================

def contar_registros_csv(nombre_archivo: str) -> int:
    """Cuenta registros de un CSV ubicado en data/.

    Si el archivo no existe o no puede leerse, devuelve 0.
    """
    ruta = DATA_DIR / nombre_archivo

    if not ruta.exists() or not ruta.is_file():
        return 0

    try:
        with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            return sum(1 for _ in lector)
    except (OSError, UnicodeDecodeError, csv.Error):
        return 0


def obtener_kpis_iniciales() -> dict[str, int]:
    """Obtiene indicadores simples para la portada.

    Estos KPIs no alteran datos ni ejecutan logica de negocio. Solo leen los
    CSV existentes para mostrar una vista general del sistema.
    """
    return {
        "clientes": contar_registros_csv(ARCHIVOS_CSV.get("clientes", "clientes.csv")),
        "productos": contar_registros_csv(ARCHIVOS_CSV.get("productos", "productos.csv")),
        "pedidos": contar_registros_csv(ARCHIVOS_CSV.get("pedidos", "pedidos.csv")),
        "despachos": contar_registros_csv(ARCHIVOS_CSV.get("despachos", "despachos.csv")),
    }


def mostrar_kpis_portada() -> None:
    """Muestra tarjetas KPI iniciales."""
    kpis = obtener_kpis_iniciales()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mostrar_tarjeta_kpi(
            "Clientes",
            kpis["clientes"],
            "Registros en la base de clientes",
        )

    with col2:
        mostrar_tarjeta_kpi(
            "Productos",
            kpis["productos"],
            "Menus y productos registrados",
        )

    with col3:
        mostrar_tarjeta_kpi(
            "Pedidos",
            kpis["pedidos"],
            "Pedidos almacenados en el sistema",
        )

    with col4:
        mostrar_tarjeta_kpi(
            "Despachos",
            kpis["despachos"],
            "Entregas y seguimiento logistico",
        )


def mostrar_guia_uso() -> None:
    """Muestra una guia breve para el usuario."""
    mostrar_seccion(
        "Ruta sugerida de uso",
        "Flujo recomendado para demostrar la integracion del sistema.",
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    pasos = [
        ("1", "Cliente", "Registrar o consultar cliente"),
        ("2", "Pedido", "Crear pedido y revisar estado"),
        ("3", "Produccion", "Planificar preparacion"),
        ("4", "Despacho", "Controlar entrega"),
        ("5", "Reporte", "Analizar indicadores"),
    ]

    for columna, (numero, titulo, descripcion) in zip(
        [col1, col2, col3, col4, col5],
        pasos,
    ):
        with columna:
            st.markdown(
                f"""
                <div class="sigo-kpi-card" style="min-height: 145px;">
                    <div class="sigo-kpi-label">Paso {numero}</div>
                    <div class="sigo-kpi-value" style="font-size: 1.28rem;">
                        {titulo}
                    </div>
                    <div class="sigo-kpi-help">{descripcion}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 3. PORTADA PRINCIPAL
# ============================================================

mostrar_hero_inicio()

mostrar_resumen_empresa()

mostrar_kpis_portada()

mostrar_seccion(
    "Modulos del sistema",
    "Accede desde la barra lateral a cada modulo operativo de SIGO-PRO FoodOps.",
)

mostrar_grid_modulos(MODULOS_APP)

mostrar_guia_uso()

mostrar_alerta(
    "Integracion visual activa",
    (
        "La portada ya utiliza configuracion central, assets visuales, componentes "
        "reutilizables y lectura segura de indicadores iniciales."
    ),
    "success",
)

mostrar_footer(TEXTOS_APP.get("footer"))