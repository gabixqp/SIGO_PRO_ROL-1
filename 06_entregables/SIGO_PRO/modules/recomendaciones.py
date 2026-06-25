"""Motor simple de recomendaciones operativas."""

from analytics.optimizacion import sugerir_produccion_preventiva
try:
    from modules.costos import calcular_margen_producto, obtener_umbral_margen_producto
except ImportError:
    # Compatibilidad si Streamlit conserva una version antigua en memoria.
    from modules.costos import calcular_margen_producto

    def obtener_umbral_margen_producto(_id_producto):
        return True, 20.0
from modules.despachos import listar_despachos
from modules.insumos import obtener_insumos_criticos
from modules.productos import listar_productos, obtener_productos_criticos


def generar_recomendaciones() -> list[str]:
    """Devuelve alertas accionables basadas en stock, margen y despachos."""
    # Empezamos con una lista vacia; iremos agregando mensajes.
    recomendaciones = []

    # Productos terminados bajo minimo: conviene producir o reponer.
    productos_criticos = obtener_productos_criticos()
    for _, row in productos_criticos.iterrows():
        # row representa un producto con stock bajo.
        recomendaciones.append(f"Reponer o producir {row.get('nombre', row.get('id_producto'))}: stock bajo.")

    # Insumos bajo minimo: pueden bloquear produccion futura.
    insumos_criticos = obtener_insumos_criticos()
    for _, row in insumos_criticos.iterrows():
        # row representa un insumo con stock bajo.
        recomendaciones.append(f"Reponer insumo {row.get('nombre', row.get('id_insumo'))}: stock bajo.")

    # Cargamos productos para revisar margen uno por uno.
    productos = listar_productos()
    if not productos.empty and "id_producto" in productos.columns:
        # Revisa margen contra umbral por familia para detectar productos caros.
        for _, row in productos.iterrows():
            # Calculamos margen real del producto.
            ok, margen = calcular_margen_producto(row["id_producto"])

            # Obtenemos el margen minimo esperado para su familia.
            ok_umbral, umbral = obtener_umbral_margen_producto(row["id_producto"])

            # Si no se pudo obtener umbral, usamos 20%.
            umbral = float(umbral) if ok_umbral else 20.0

            # Si el margen existe y esta bajo el umbral, agregamos recomendacion.
            if ok and margen < umbral:
                recomendaciones.append(
                    f"Revisar precio o costo de {row.get('nombre', row['id_producto'])}: margen menor a {umbral:.0f}%."
                )

    # Revisamos si hay demasiados despachos retrasados.
    despachos = listar_despachos()
    if not despachos.empty and "estado" in despachos.columns:
        # Mas de 15% de retrasos indica problema operativo relevante.
        porcentaje = (despachos["estado"].eq("retrasado").sum() / len(despachos)) * 100
        if porcentaje > 15:
            recomendaciones.append("Revisar capacidad operativa: despachos retrasados sobre 15%.")

    # Cruza demanda historica y stock para sugerir fabricacion preventiva.
    preventiva = sugerir_produccion_preventiva()
    for _, row in preventiva.iterrows():
        # row representa un producto con demanda alta y stock bajo/cercano al minimo.
        recomendaciones.append(f"Produccion preventiva sugerida para {row.get('nombre', row.get('id_producto'))}.")

    # Si ningun criterio genero alertas, devolvemos un mensaje positivo/neutro.
    if not recomendaciones:
        recomendaciones.append("No hay recomendaciones criticas con los datos disponibles.")

    # Devolvemos todos los mensajes encontrados.
    return recomendaciones
