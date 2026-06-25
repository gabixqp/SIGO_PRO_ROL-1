"""Pagina para registrar y consultar despachos."""

import streamlit as st

from core.ui import aplicar_estilos
from modules.despachos import ESTADOS, listar_despachos, registrar_despacho
from modules.pedidos import listar_pedidos


aplicar_estilos()


def _feedback(ok: bool, msg: str) -> None:
    """Muestra exito o error segun el resultado de una operacion."""
    if ok:
        st.success(msg)
    else:
        st.error(msg)


@st.dialog("Registrar despacho", width="large")
def modal_registrar_despacho(pedidos):
    """Modal para capturar fechas y estado de entrega de un pedido."""
    # Convertimos los IDs de pedido a texto para mostrarlos en el selector.
    ids = pedidos["id_pedido"].astype(str).tolist()

    # Formulario dentro del modal.
    with st.form("form_registrar_despacho"):
        # Pedido que se va a despachar.
        id_pedido = st.selectbox("Pedido", ids)

        # Fechas de plan y entrega real.
        fecha_programada = st.date_input("Fecha programada")
        fecha_entrega = st.date_input("Fecha entrega")

        # Estado del despacho.
        estado = st.selectbox("Estado", ESTADOS)
        if fecha_entrega > fecha_programada:
            # Advertencia visual; la regla de negocio tambien sugiere usar retrasado.
            st.warning("La fecha de entrega supera la programada.")
        if st.form_submit_button("Guardar", use_container_width=True):
            # Guardamos despacho usando fechas en formato texto ISO.
            ok, msg = registrar_despacho(id_pedido, fecha_programada.isoformat(), fecha_entrega.isoformat(), estado)
            _feedback(ok, msg)
            if ok:
                # Recarga la pantalla para ver el registro nuevo.
                st.rerun()


# Titulo de la pagina.
st.title("Despachos")

# Texto breve del objetivo.
st.caption("Seguimiento de despachos y actualizacion de pedidos entregados.")

# Cargamos pedidos para saber que puede despacharse.
pedidos = listar_pedidos()

# Encabezado con boton a la derecha.
left, right = st.columns([0.72, 0.28], vertical_alignment="center")
left.subheader("Despachos")
# Solo se puede despachar algo si ya existe un pedido.
if pedidos.empty:
    right.button("Registrar despacho", disabled=True, use_container_width=True)
    st.warning("Para registrar despachos se requieren pedidos disponibles.")
elif right.button("Registrar despacho", type="primary", use_container_width=True):
    # Abre el modal para registrar despacho.
    modal_registrar_despacho(pedidos)

despachos = listar_despachos()
# Tabla historica de despachos registrados.
if despachos.empty:
    st.info("Sin despachos disponibles.")
else:
    st.dataframe(despachos, use_container_width=True, hide_index=True)
