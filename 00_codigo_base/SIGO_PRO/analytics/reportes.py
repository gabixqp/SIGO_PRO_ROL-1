"""Exportacion de reportes ejecutivos e indicadores."""

from datetime import datetime

import pandas as pd

from analytics.indicadores import (
    calcular_indicadores_generales,
    calcular_pedidos_por_cliente,
    calcular_pedidos_por_estado,
    calcular_ventas_por_producto,
)
from config import EXPORTACIONES_DIR, REPORTES_DIR
from modules.recomendaciones import generar_recomendaciones


def generar_reporte_ejecutivo() -> tuple[bool, str]:
    """Crea un TXT con indicadores generales y recomendaciones."""
    # Creamos la carpeta output/reportes si no existe.
    REPORTES_DIR.mkdir(parents=True, exist_ok=True)

    # Calculamos los numeros principales.
    indicadores = calcular_indicadores_generales()

    # Generamos lista de alertas/recomendaciones.
    recomendaciones = generar_recomendaciones()

    # El nombre incluye fecha y hora para no pisar reportes anteriores.
    ruta = REPORTES_DIR / f"reporte_ejecutivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    # Se arma como texto simple para que pueda abrirse sin Excel ni dependencias.
    lineas = ["SIGO-PRO FoodOps - Reporte ejecutivo", ""]

    # Agregamos cada indicador como una linea "clave: valor".
    lineas.extend([f"{clave}: {valor}" for clave, valor in indicadores.items()])

    # Agregamos seccion de recomendaciones.
    lineas.extend(["", "Recomendaciones:"])

    # Cada recomendacion se escribe con guion.
    lineas.extend([f"- {item}" for item in recomendaciones])

    # Escribimos todo el texto en el archivo.
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return True, str(ruta)


def exportar_indicadores_csv() -> tuple[bool, str]:
    """Exporta los indicadores generales a un CSV con timestamp."""
    # Creamos la carpeta output/exportaciones si no existe.
    EXPORTACIONES_DIR.mkdir(parents=True, exist_ok=True)

    # El nombre incluye fecha y hora para mantener historico.
    ruta = EXPORTACIONES_DIR / f"indicadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Calculamos indicadores generales.
    indicadores = calcular_indicadores_generales()

    # Convertimos un diccionario en tabla de una fila.
    resumen = pd.DataFrame([indicadores])

    # Guardamos esa tabla como CSV.
    resumen.to_csv(ruta, index=False)

    # Estas tablas se calculan para saber cuantos registros de detalle existen.
    ventas = calcular_ventas_por_producto()
    clientes = calcular_pedidos_por_cliente()
    estados = calcular_pedidos_por_estado()

    # extras queda preparado para ampliar exportaciones futuras.
    extras = {
        "ventas_por_producto": len(ventas),
        "pedidos_por_cliente": len(clientes),
        "pedidos_por_estado": len(estados),
    }
    if extras:
        # Reservado para ampliar el CSV con mas hojas/archivos en una etapa futura.
        pass
    return True, str(ruta)
