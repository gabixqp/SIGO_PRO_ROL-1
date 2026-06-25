"""Pagina para analizar costos, margen y desglose por producto."""

import streamlit as st
import pandas as pd

try:
    from config import MARGEN_MINIMO_DEFAULT, MARGEN_MINIMO_POR_FAMILIA, METODO_VALUACION_INVENTARIO
except ImportError:
    # Fallback para evitar errores si Streamlit conserva una version vieja.
    MARGEN_MINIMO_DEFAULT = 20.0
    MARGEN_MINIMO_POR_FAMILIA = {}
    METODO_VALUACION_INVENTARIO = "PROMEDIO_PONDERADO"
from core.ui import aplicar_estilos
from modules.costos import calcular_costo_producto, calcular_margen_producto
from modules.insumos import listar_insumos
from modules.productos import obtener_productos_activos
from modules.recetas import obtener_receta_producto


aplicar_estilos()

# Titulo de la pagina.
st.title("Costos")


def _obtener_desglose_costo_producto(id_producto) -> tuple[bool, pd.DataFrame | str]:
    """Calcula el costo detallado de insumos para mostrarlo en pantalla."""
    # Obtenemos la receta del producto elegido.
    receta = obtener_receta_producto(id_producto)

    # Obtenemos todos los insumos con sus costos y mermas.
    insumos = listar_insumos()
    if receta.empty:
        return False, "El producto no tiene receta configurada."
    if insumos.empty:
        return False, "No hay insumos disponibles."

    # Lista donde se guardara una fila de costo por insumo.
    filas = []
    for _, item in receta.iterrows():
        # Buscamos el insumo que aparece en esta linea de receta.
        insumo = insumos[insumos["id_insumo"] == item["id_insumo"]]
        if insumo.empty:
            return False, f"Insumo {item['id_insumo']} no encontrado."
        insumo = insumo.iloc[0]
        # Cantidad de insumo requerida por receta.
        cantidad_receta = float(item["cantidad"])

        # Costo por unidad del insumo.
        costo_unitario = float(insumo.get("costo_promedio", insumo.get("costo_unitario", 0)))

        # Porcentaje de merma o desperdicio.
        merma_pct = float(insumo.get("merma_pct", 0))

        # Factor para aumentar cantidad segun merma: 10% -> 1.10.
        factor_merma = 1 + merma_pct / 100
        # Se separa el costo teorico del costo por merma para explicar desperdicio.
        costo_teorico = cantidad_receta * costo_unitario
        costo_merma = (cantidad_receta * factor_merma - cantidad_receta) * costo_unitario
        # Agregamos una fila explicativa para este insumo.
        filas.append(
            {
                "id_insumo": item["id_insumo"],
                "insumo": insumo.get("nombre", item["id_insumo"]),
                "cantidad_receta": cantidad_receta,
                "unidad": insumo.get("unidad", ""),
                "costo_unitario_insumo": costo_unitario,
                "metodo_valuacion": METODO_VALUACION_INVENTARIO,
                "merma_pct": merma_pct,
                "cantidad_con_merma": cantidad_receta * factor_merma,
                "costo_insumo_teorico": costo_teorico,
                "costo_merma": costo_merma,
                "costo_aportado": costo_teorico + costo_merma,
            }
        )
    # Convertimos la lista a tabla.
    return True, pd.DataFrame(filas)


def _numero(row, columna: str) -> float:
    """Lee una columna numerica opcional del producto; si falla devuelve 0."""
    try:
        return float(row.get(columna, 0))
    except (TypeError, ValueError):
        return 0.0


def _umbral_margen(producto) -> float:
    """Obtiene el margen minimo exigido segun familia o categoria."""
    familia = str(producto.get("familia", producto.get("categoria", "otros"))).strip().lower()
    return MARGEN_MINIMO_POR_FAMILIA.get(familia, MARGEN_MINIMO_DEFAULT)

productos = obtener_productos_activos()
if productos.empty:
    st.warning("Para calcular costos se requieren productos y recetas disponibles.")
else:
    # El usuario selecciona por nombre; el calculo usa el ID interno.
    opciones = dict(zip(productos["nombre"], productos["id_producto"]))

    # Selector de producto para analizar.
    producto_nombre = st.selectbox("Producto", list(opciones.keys()))

    # Boton que dispara el calculo.
    if st.button("Calcular"):
        # Convertimos nombre seleccionado a ID real.
        id_producto = opciones[producto_nombre]

        # Tomamos la fila completa del producto.
        producto = productos[productos["id_producto"] == id_producto].iloc[0]

        # Leemos precio de venta.
        precio_venta = float(producto["precio_venta"])

        # Calculamos costo, margen y desglose.
        ok_costo, costo = calcular_costo_producto(id_producto)
        ok_margen, margen = calcular_margen_producto(id_producto)
        ok_desglose, desglose = _obtener_desglose_costo_producto(id_producto)
        if ok_costo:
            # Costos directos: insumos teoricos + mano de obra directa.
            mano_obra = _numero(producto, "mano_obra_directa_unitaria")
            # CIF: costos indirectos de fabricacion configurados por producto.
            cif_gas = _numero(producto, "cif_gas_unitario")
            cif_energia = _numero(producto, "cif_energia_unitario")
            cif_depreciacion = _numero(producto, "cif_depreciacion_unitario")
            cif_otros = _numero(producto, "cif_otros_unitario")
            costo_insumos = float(desglose["costo_insumo_teorico"].sum()) if ok_desglose else 0.0
            costo_mermas = float(desglose["costo_merma"].sum()) if ok_desglose else 0.0
            costo_directo = costo_insumos + mano_obra
            costo_indirecto = costo_mermas + cif_gas + cif_energia + cif_depreciacion + cif_otros
            costo_total = costo_directo + costo_indirecto
            # Margen porcentual sobre precio de venta.
            margen_real = ((precio_venta - costo_total) / precio_venta) * 100 if precio_venta > 0 else 0.0
            umbral = _umbral_margen(producto)

            # Mostramos cuatro metricas principales.
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precio venta", f"{precio_venta:.2f}")
            c2.metric("Costo directo", f"{costo_directo:.2f}")
            c3.metric("Costo indirecto", f"{costo_indirecto:.2f}")
            c4.metric("Margen", f"{margen_real:.2f}%")
        else:
            # Si no se pudo calcular costo, mostramos el mensaje devuelto.
            st.error(costo)

        if ok_margen and ok_desglose:
            # Advierte si el margen cae bajo el minimo esperado para esa familia.
            if margen_real < umbral:
                st.warning(f"Margen menor al umbral de la familia ({umbral:.2f}%). Revisar precio o costo.")
        else:
            # Si margen o desglose fallan, mostramos el error.
            st.error(margen)

        if ok_desglose:
            st.subheader("Estructura de costos")
            # Tabla ejecutiva: resume los conceptos principales del costo total.
            componentes = pd.DataFrame(
                [
                    {"tipo": "Directo", "concepto": "Insumos teoricos", "importe": costo_insumos},
                    {"tipo": "Directo", "concepto": "Mano de obra directa", "importe": mano_obra},
                    {"tipo": "Indirecto", "concepto": "Mermas y desperdicios", "importe": costo_mermas},
                    {"tipo": "Indirecto", "concepto": "Gas", "importe": cif_gas},
                    {"tipo": "Indirecto", "concepto": "Energia", "importe": cif_energia},
                    {"tipo": "Indirecto", "concepto": "Depreciacion", "importe": cif_depreciacion},
                    {"tipo": "Indirecto", "concepto": "Otros CIF", "importe": cif_otros},
                ]
            )
            st.dataframe(componentes, use_container_width=True, hide_index=True)

            st.subheader("Desglose del costo")
            # Tabla tecnica: muestra cada insumo de la receta y su aporte al costo.
            st.caption(
                "El costo directo separa insumos teoricos y mano de obra. La merma se muestra como costo indirecto para revelar desperdicio operativo."
            )
            st.dataframe(
                desglose,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "cantidad_receta": st.column_config.NumberColumn("Cantidad receta", format="%.4f"),
                    "costo_unitario_insumo": st.column_config.NumberColumn("Costo unitario insumo", format="%.4f"),
                    "merma_pct": st.column_config.NumberColumn("Merma %", format="%.2f"),
                    "cantidad_con_merma": st.column_config.NumberColumn("Cantidad con merma", format="%.4f"),
                    "costo_insumo_teorico": st.column_config.NumberColumn("Costo teorico", format="%.4f"),
                    "costo_merma": st.column_config.NumberColumn("Costo merma", format="%.4f"),
                    "costo_aportado": st.column_config.NumberColumn("Costo aportado", format="%.4f"),
                },
            )
            st.info(
                f"Inventario valorizado con {METODO_VALUACION_INVENTARIO}. Margen = ((precio venta {precio_venta:.2f} - costo total {costo_total:.2f}) / precio venta {precio_venta:.2f}) x 100."
            )
            st.caption(
                "Para activar mano de obra y CIF en los CSV reales, agrega columnas opcionales: mano_obra_directa_unitaria, cif_gas_unitario, cif_energia_unitario, cif_depreciacion_unitario y cif_otros_unitario."
            )
        else:
            st.error(desglose)
