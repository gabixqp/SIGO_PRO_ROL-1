"""Generacion de graficos PNG para reportes."""

import matplotlib.pyplot as plt

from analytics.indicadores import calcular_pedidos_por_estado, calcular_ventas_por_producto
from config import GRAFICOS_DIR
from modules.productos import obtener_productos_criticos


def _guardar_figura(fig, nombre_archivo: str) -> str:
    """Guarda una figura Matplotlib en output/graficos y libera memoria."""
    # Creamos output/graficos si no existe.
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    # Construimos la ruta final del PNG.
    ruta = GRAFICOS_DIR / nombre_archivo

    # Ajusta margenes para que titulos y etiquetas no salgan cortados.
    fig.tight_layout()

    # Guarda la imagen en disco con resolucion decente.
    fig.savefig(ruta, dpi=120)

    # Cierra la figura para liberar memoria.
    plt.close(fig)

    # Devolvemos la ruta como texto para mostrarla al usuario.
    return str(ruta)


def generar_grafico_ventas_por_producto() -> tuple[bool, str]:
    """Genera grafico de barras con ventas acumuladas por producto."""
    # Calculamos la tabla de ventas por producto.
    df = calcular_ventas_por_producto()
    if df.empty:
        return False, "No hay ventas para graficar."

    # Usamos nombre si existe; si no, mostramos id_producto.
    etiquetas = df.get("nombre", df["id_producto"]).fillna(df["id_producto"])

    # Creamos una figura y un area de dibujo.
    fig, ax = plt.subplots(figsize=(8, 4))

    # Dibujamos barras: eje X productos, eje Y subtotal vendido.
    ax.bar(etiquetas.astype(str), df["subtotal"])
    ax.set_title("Ventas por producto")
    ax.set_ylabel("Ventas")
    ax.tick_params(axis="x", rotation=45)
    return True, _guardar_figura(fig, "ventas_por_producto.png")


def generar_grafico_pedidos_por_estado() -> tuple[bool, str]:
    """Genera grafico de barras con cantidad de pedidos por estado."""
    # Calculamos cantidad de pedidos por estado.
    df = calcular_pedidos_por_estado()
    if df.empty:
        return False, "No hay pedidos para graficar."

    # Creamos la figura.
    fig, ax = plt.subplots(figsize=(7, 4))

    # Dibujamos una barra por cada estado.
    ax.bar(df["estado"].astype(str), df["cantidad"])
    ax.set_title("Pedidos por estado")
    ax.set_ylabel("Cantidad")
    return True, _guardar_figura(fig, "pedidos_por_estado.png")


def generar_grafico_stock_critico_productos() -> tuple[bool, str]:
    """Genera grafico de barras con productos bajo stock minimo."""
    # Obtenemos productos cuyo stock esta critico.
    df = obtener_productos_criticos()
    if df.empty:
        return False, "No hay productos criticos para graficar."

    # Usamos nombre si existe; si no, ID.
    etiquetas = df.get("nombre", df["id_producto"]).fillna(df["id_producto"])

    # Creamos grafico de barras.
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(etiquetas.astype(str), df["stock_actual"])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Stock critico de productos")
    ax.set_ylabel("Stock actual")
    ax.tick_params(axis="x", rotation=45)
    return True, _guardar_figura(fig, "stock_critico_productos.png")
