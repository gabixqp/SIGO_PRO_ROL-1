"""Pagina de reportes, indicadores y graficos operativos."""

import streamlit as st
import matplotlib.pyplot as plt

from core.ui import aplicar_estilos
from analytics.graficos import (
    generar_grafico_pedidos_por_estado,
    generar_grafico_stock_critico_productos,
    generar_grafico_ventas_por_producto,
)
from analytics.indicadores import (
    calcular_indicadores_generales,
    calcular_pedidos_por_estado,
    calcular_pedidos_por_cliente,
    calcular_ventas_por_producto,
)
try:
    from analytics.indicadores import calcular_indicadores_financieros_productos, calcular_rotacion_inventarios
except ImportError:
    # Fallback para que la pagina siga cargando en recargas parciales de Streamlit.
    def calcular_indicadores_financieros_productos():
        import pandas as pd
        return pd.DataFrame()

    def calcular_rotacion_inventarios():
        import pandas as pd
        return pd.DataFrame()
from analytics.reportes import exportar_indicadores_csv, generar_reporte_ejecutivo
from modules.productos import obtener_productos_criticos
from modules.recomendaciones import generar_recomendaciones


aplicar_estilos()

# Titulo de la pagina.
st.title("Reportes Inteligentes")

# Texto que resume el objetivo de esta pagina.
st.caption("Centro de reportes: ejecutivo, indicadores y graficos operativos.")


def _mostrar_grafico_ventas(ventas):
    """Dibuja en pantalla las ventas por producto sin guardar archivo."""
    # Si no hay datos, no intentamos dibujar.
    if ventas.empty:
        st.info("Sin ventas disponibles para graficar.")
        return

    # Usamos nombre si existe; si no, usamos id_producto.
    etiquetas = ventas.get("nombre", ventas["id_producto"]).fillna(ventas["id_producto"])

    # Creamos figura de Matplotlib.
    fig, ax = plt.subplots(figsize=(8, 4))

    # Dibujamos barras con color corporativo.
    ax.bar(etiquetas.astype(str), ventas["subtotal"], color="#A5211C")
    ax.set_title("Ventas por producto")
    ax.set_ylabel("Ventas")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    # Mostramos el grafico dentro de Streamlit.
    st.pyplot(fig)
    # Cerramos la figura para liberar memoria.
    plt.close(fig)


def _mostrar_grafico_estados(estados):
    """Dibuja en pantalla la cantidad de pedidos por estado."""
    # Si no hay datos, no dibujamos.
    if estados.empty:
        st.info("Sin pedidos disponibles para graficar estados.")
        return

    # Creamos figura.
    fig, ax = plt.subplots(figsize=(7, 4))

    # Cada barra representa un estado de pedido.
    ax.bar(estados["estado"].astype(str), estados["cantidad"], color="#BD5E57")
    ax.set_title("Pedidos por estado")
    ax.set_ylabel("Cantidad")
    fig.tight_layout()
    # Mostramos en pantalla.
    st.pyplot(fig)
    # Cerramos para liberar memoria.
    plt.close(fig)


def _mostrar_grafico_stock(criticos):
    """Dibuja en pantalla los productos con stock critico."""
    # Si no hay productos criticos, no se dibuja nada.
    if criticos.empty:
        st.info("Sin productos criticos para graficar.")
        return

    # Usamos nombre si existe; si no, ID.
    etiquetas = criticos.get("nombre", criticos["id_producto"]).fillna(criticos["id_producto"])

    # Creamos figura.
    fig, ax = plt.subplots(figsize=(8, 4))

    # Dibujamos stock actual de cada producto critico.
    ax.bar(etiquetas.astype(str), criticos["stock_actual"], color="#7F1713")
    ax.set_title("Stock critico de productos")
    ax.set_ylabel("Stock actual")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    # Mostramos en Streamlit.
    st.pyplot(fig)
    # Cerramos figura.
    plt.close(fig)

# Creamos tres pestanas para separar tipos de reporte.
tab_ejecutivo, tab_indicadores, tab_graficos = st.tabs(
    ["Reporte ejecutivo", "Reporte de indicadores", "Reporte de graficos"]
)

with tab_ejecutivo:
    # Vista gerencial: pocos numeros y recomendaciones accionables.
    st.subheader("Reporte ejecutivo")

    # Calculamos indicadores generales.
    indicadores = calcular_indicadores_generales()

    # Mostramos cuatro metricas en columnas.
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pedidos", indicadores["total_pedidos"])
    c2.metric("Ventas", f"{indicadores['ventas_totales']:.2f}")
    c3.metric("Clientes", indicadores["clientes"])
    c4.metric("Despachos retrasados", f"{indicadores['porcentaje_despachos_retrasados']:.1f}%")

    st.subheader("Recomendaciones")
    # Recorremos cada recomendacion y la mostramos como texto con guion.
    for item in generar_recomendaciones():
        st.write(f"- {item}")

    if st.button("Generar reporte ejecutivo", type="primary", use_container_width=True):
        # Genera un TXT en output/reportes para compartir fuera de la app.
        ok, msg = generar_reporte_ejecutivo()
        if ok:
            st.success(f"Reporte generado: {msg}")
        else:
            st.error(msg)

with tab_indicadores:
    # Vista analitica: tablas para revisar detalle comercial, financiero e inventario.
    st.subheader("Reporte de indicadores")
    st.caption("Este reporte resume la operacion en cuatro grupos: operacion, ventas, finanzas e inventario.")

    # Volvemos a calcular indicadores para esta pestana.
    indicadores = calcular_indicadores_generales()
    st.markdown("**Indicadores operativos**")

    # Indicadores operativos: actividad y retrasos.
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Pedidos", indicadores["total_pedidos"])
    k2.metric("Clientes", indicadores["clientes"])
    k3.metric("Productos", indicadores["productos"])
    k4.metric("Despachos retrasados", f"{indicadores['porcentaje_despachos_retrasados']:.1f}%")

    st.markdown("**Indicadores comerciales**")
    # Indicadores comerciales: ventas y productos criticos.
    c1, c2 = st.columns(2)
    c1.metric("Ventas totales", f"{indicadores['ventas_totales']:.2f}")
    c2.metric("Productos con stock critico", indicadores["productos_criticos"])

    st.subheader("Ventas por producto")
    # Identifica productos que concentran ingresos.
    st.caption("Muestra que productos concentran los ingresos registrados en el detalle de pedidos.")
    # Calculamos ventas agrupadas por producto.
    ventas = calcular_ventas_por_producto()
    if ventas.empty:
        st.info("Sin ventas disponibles.")
    else:
        st.dataframe(ventas, use_container_width=True, hide_index=True)

    st.subheader("Pedidos por cliente")
    # Identifica clientes relevantes por frecuencia e importe acumulado.
    st.caption("Permite identificar clientes con mayor volumen de pedidos e importe acumulado.")
    # Calculamos pedidos agrupados por cliente.
    clientes = calcular_pedidos_por_cliente()
    if clientes.empty:
        st.info("Sin pedidos por cliente disponibles.")
    else:
        st.dataframe(clientes, use_container_width=True, hide_index=True)

    st.subheader("Pedidos por estado")
    # Sirve para ver cuellos de botella del flujo comercial-operativo.
    st.caption("Resume el avance comercial-operativo de los pedidos.")
    # Calculamos pedidos agrupados por estado.
    estados = calcular_pedidos_por_estado()
    if estados.empty:
        st.info("Sin estados de pedido disponibles.")
    else:
        st.dataframe(estados, use_container_width=True, hide_index=True)

    st.subheader("Indicadores financieros")
    # Requiere recetas y costos para calcular margen y punto de equilibrio.
    st.caption("Incluye margen de contribucion y punto de equilibrio por producto cuando existan recetas y costos.")
    # Calculamos indicadores financieros por producto.
    financieros = calcular_indicadores_financieros_productos()
    if financieros.empty:
        st.info("Sin indicadores financieros disponibles.")
    else:
        st.dataframe(financieros, use_container_width=True, hide_index=True)

    st.subheader("Rotacion de inventarios")
    # La rotacion real necesita consumos historicos; aqui se deja preparada.
    st.caption("Valoriza existencias de insumos. La rotacion requiere costo de ventas o consumos por periodo.")
    # Calculamos valorizacion de inventario y rotacion pendiente.
    rotacion = calcular_rotacion_inventarios()
    if rotacion.empty:
        st.info("Sin inventario disponible para rotacion.")
    else:
        st.dataframe(rotacion, use_container_width=True, hide_index=True)
        st.caption("La rotacion queda en blanco hasta contar con consumos historicos o costo de ventas por periodo.")

    if st.button("Exportar reporte de indicadores", type="primary", use_container_width=True):
        # Exporta un CSV simple en output/exportaciones.
        ok, msg = exportar_indicadores_csv()
        if ok:
            st.success(f"Indicadores exportados: {msg}")
        else:
            st.error(msg)

with tab_graficos:
    # Vista visual: previsualiza y permite guardar graficos PNG.
    st.subheader("Reporte de graficos")
    st.caption("Las graficas se muestran como vista previa. Los botones guardan una copia PNG en output/graficos.")

    # Calculamos las tres tablas que alimentan los graficos.
    ventas = calcular_ventas_por_producto()
    estados = calcular_pedidos_por_estado()
    criticos = obtener_productos_criticos()

    st.subheader("Ventas por producto")
    # Mostramos vista previa del grafico.
    _mostrar_grafico_ventas(ventas)
    if st.button("Guardar grafico de ventas", type="primary", use_container_width=True):
        # Guarda el mismo grafico como imagen en output/graficos.
        ok, msg = generar_grafico_ventas_por_producto()
        if ok:
            st.success(f"Grafico generado: {msg}")
        else:
            st.warning(msg)

    st.subheader("Pedidos por estado")
    # Mostramos vista previa del grafico.
    _mostrar_grafico_estados(estados)
    if st.button("Guardar grafico de estados", type="primary", use_container_width=True):
        # Guarda el grafico de estados como PNG.
        ok, msg = generar_grafico_pedidos_por_estado()
        if ok:
            st.success(f"Grafico generado: {msg}")
        else:
            st.warning(msg)

    st.subheader("Stock critico")
    # Primero mostramos la tabla de productos criticos.
    if criticos.empty:
        st.info("Sin productos criticos.")
    else:
        st.dataframe(criticos, use_container_width=True, hide_index=True)

    # Luego mostramos el grafico de esos productos.
    _mostrar_grafico_stock(criticos)
    if st.button("Guardar grafico de stock", type="primary", use_container_width=True):
        # Guarda el grafico de stock critico como PNG.
        ok, msg = generar_grafico_stock_critico_productos()
        if ok:
            st.success(f"Grafico generado: {msg}")
        else:
            st.warning(msg)
