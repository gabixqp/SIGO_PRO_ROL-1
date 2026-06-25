"""Pagina inicial: portada visual y resumen rapido del sistema."""

from __future__ import annotations

import streamlit as st

from analytics.indicadores import calcular_indicadores_generales
from config import ARCHIVOS_CSV, MODULOS_APP, TEXTOS_APP
from core.storage import validar_disponibilidad_archivo
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
# 1. CONFIGURACION VISUAL DE LA PAGINA
# ============================================================

aplicar_estilos()


# ============================================================
# 2. FUNCIONES DE APOYO
# ============================================================

def revisar_archivos_datos() -> list[str]:
    """Valida disponibilidad de archivos CSV esperados."""
    faltantes = []

    for archivo in ARCHIVOS_CSV.values():
        ok, mensaje = validar_disponibilidad_archivo(archivo)
        if not ok:
            faltantes.append(mensaje)

    return faltantes


def obtener_indicadores_inicio() -> dict:
    """Obtiene indicadores generales con fallback seguro."""
    try:
        return calcular_indicadores_generales()
    except Exception as exc:
        mostrar_alerta(
            "No se pudieron calcular los indicadores",
            f"El sistema encontro un problema al leer los datos: {exc}",
            "warning",
        )
        return {
            "total_pedidos": 0,
            "ventas_totales": 0.0,
            "clientes": 0,
            "productos_criticos": 0,
        }


def mostrar_kpis_inicio(indicadores: dict) -> None:
    """Muestra KPIs principales del panel de inicio."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mostrar_tarjeta_kpi(
            "Pedidos",
            indicadores.get("total_pedidos", 0),
            "Pedidos registrados en el sistema",
        )

    with col2:
        mostrar_tarjeta_kpi(
            "Ventas",
            f"S/ {float(indicadores.get('ventas_totales', 0.0)):.2f}",
            "Importe total registrado",
        )

    with col3:
        mostrar_tarjeta_kpi(
            "Clientes",
            indicadores.get("clientes", 0),
            "Clientes registrados",
        )

    with col4:
        mostrar_tarjeta_kpi(
            "Productos criticos",
            indicadores.get("productos_criticos", 0),
            "Productos bajo nivel minimo",
        )


def mostrar_flujo_integrado() -> None:
    """Muestra el flujo principal que se usara como evidencia de integracion."""
    mostrar_seccion(
        "Flujo operativo integrado",
        "Ruta sugerida para demostrar el funcionamiento del sistema en la defensa.",
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    pasos = [
        ("01", "Clientes", "Registrar o consultar clientes."),
        ("02", "Pedidos", "Crear pedidos y revisar estados."),
        ("03", "Produccion", "Planificar preparacion de productos."),
        ("04", "Despachos", "Controlar entrega y seguimiento."),
        ("05", "Reportes", "Analizar indicadores y recomendaciones."),
    ]

    for columna, (numero, titulo, descripcion) in zip(
        [col1, col2, col3, col4, col5],
        pasos,
    ):
        with columna:
            st.markdown(
                f"""
                <div class="sigo-kpi-card" style="min-height: 150px;">
                    <div class="sigo-kpi-label">Paso {numero}</div>
                    <div class="sigo-kpi-value" style="font-size: 1.18rem;">
                        {titulo}
                    </div>
                    <div class="sigo-kpi-help">{descripcion}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# 3. CONTENIDO PRINCIPAL
# ============================================================

mostrar_hero_inicio()

mostrar_resumen_empresa()

faltantes = revisar_archivos_datos()

if faltantes:
    mostrar_alerta(
        "Archivos de datos pendientes",
        "Algunos archivos CSV no estan disponibles o no tienen la estructura esperada.",
        "warning",
    )

    with st.expander("Ver detalle de archivos pendientes"):
        for mensaje in faltantes:
            st.caption(mensaje)
else:
    mostrar_alerta(
        "Base de datos operativa",
        "Los archivos principales del sistema estan disponibles para consulta.",
        "success",
    )

mostrar_seccion(
    "Resumen operativo",
    "Indicadores iniciales calculados a partir de los archivos de datos.",
)

indicadores = obtener_indicadores_inicio()
mostrar_kpis_inicio(indicadores)

mostrar_seccion(
    "Modulos del sistema",
    "Cada modulo corresponde a una parte del flujo operativo de SIGO-PRO FoodOps.",
)

mostrar_grid_modulos(MODULOS_APP)

mostrar_flujo_integrado()

mostrar_alerta(
    "Rol 1 Integrador",
    (
        "Esta pantalla evidencia la integracion visual del sistema: configuracion "
        "central, assets, componentes UI, KPIs, modulos y flujo operativo."
    ),
    "info",
)

mostrar_footer(TEXTOS_APP.get("footer"))