# SIGO-PRO FoodOps

SIGO-PRO FoodOps es una aplicacion en Streamlit para gestionar la operacion de un negocio alimentario: clientes, productos, insumos, recetas, pedidos, produccion, despachos, costos, indicadores y reportes.

El sistema esta construido solo con codigo Python y archivos planos. La persistencia esta preparada para CSV y la configuracion futura para JSON.

## Estado actual

La aplicacion ya incluye:

- Interfaz Streamlit multipagina.
- Identidad visual calida y gastronomica con paleta institucional.
- Gestion de clientes con registro, edicion y eliminacion mediante modales.
- Gestion de productos e insumos con modales y stock critico.
- Registro de pedidos con multiples productos por cliente.
- Detalle de pedido con tabla editable de productos y cantidades.
- IGV fijo de 18% para pedidos.
- Canal de venta como lista desplegable.
- Produccion con consumo de insumos cuando la orden esta completada.
- Despachos con estados operativos y deteccion de retrasos.
- Costos con desglose por insumo, merma, mano de obra directa y CIF.
- Margen por producto y umbral por familia.
- Preparacion para valuacion de inventarios por Promedio Ponderado o PEPS.
- Reportes separados en ejecutivo, indicadores y graficos.
- Graficos con Matplotlib visibles en pantalla y exportables como PNG.
- Configuracion de empresa mediante `empresa.json` solo cuando el usuario guarda.

## Stack

- Python
- Streamlit
- pandas
- NumPy
- Matplotlib
- CSV para persistencia
- JSON para configuracion

## Estructura del proyecto

```text
SIGO_PRO/
|-- app.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- core/
|   |-- storage.py
|   |-- validaciones.py
|   |-- limpieza.py
|   |-- ui.py
|-- modules/
|   |-- clientes.py
|   |-- productos.py
|   |-- insumos.py
|   |-- recetas.py
|   |-- pedidos.py
|   |-- produccion.py
|   |-- despachos.py
|   |-- costos.py
|   |-- recomendaciones.py
|-- analytics/
|   |-- indicadores.py
|   |-- graficos.py
|   |-- reportes.py
|   |-- optimizacion.py
|-- pages/
|   |-- 1_Inicio.py
|   |-- 2_Clientes.py
|   |-- 3_Productos_Insumos.py
|   |-- 4_Pedidos.py
|   |-- 5_Produccion.py
|   |-- 6_Despachos.py
|   |-- 7_Costos.py
|   |-- 8_Reportes_Inteligentes.py
|   |-- 9_Configuracion.py
|-- data/
|-- output/
|   |-- reportes/
|   |-- graficos/
|   |-- exportaciones/
```

## Instalacion

Crear y activar un entorno virtual es recomendado:

```bash
python -m venv .venv
```

En Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Como levantar el sistema

Desde la carpeta raiz del proyecto:

```bash
streamlit run app.py
```

Luego abrir la URL que muestra Streamlit, normalmente:

```text
http://localhost:8501
```

Si Streamlit queda usando codigo cacheado despues de cambios, detener el servidor con `Ctrl + C` y volver a ejecutar:

```bash
streamlit run app.py
```

## Navegacion

El menu lateral contiene:

- Inicio
- Clientes
- Productos e Insumos
- Pedidos
- Produccion
- Despachos
- Costos
- Reportes Inteligentes
- Configuracion

El item tecnico de `app.py` fue ocultado visualmente del sidebar para que la navegacion empiece en `Inicio`.

## Datos esperados

El sistema espera los siguientes archivos en `data/`:

- `empresa.json`
- `clientes.csv`
- `productos.csv`
- `insumos.csv`
- `recetas.csv`
- `pedidos.csv`
- `detalle_pedidos.csv`
- `produccion.csv`
- `despachos.csv`
- `feedback.csv`

La aplicacion no crea CSV automaticamente al iniciar. Si falta algun archivo, muestra advertencias o tablas vacias sin detener la app.

## Columnas principales

### clientes.csv

```text
id_cliente,nombre,tipo,canal,contacto,telefono,estado,fecha_registro
```

### productos.csv

```text
id_producto,nombre,categoria,precio_venta,stock_actual,stock_minimo,unidad
```

Columnas opcionales preparadas:

```text
familia,mano_obra_directa_unitaria,cif_gas_unitario,cif_energia_unitario,cif_depreciacion_unitario,cif_otros_unitario,costo_fijo_asignado
```

### insumos.csv

```text
id_insumo,nombre,unidad,stock_actual,stock_minimo,costo_unitario,merma_pct
```

Columnas opcionales preparadas:

```text
metodo_valuacion,costo_promedio,costo_peps,valor_inventario
```

### recetas.csv

```text
id_receta,id_producto,id_insumo,cantidad
```

### pedidos.csv

```text
id_pedido,id_cliente,fecha,canal,estado,total
```

Columnas opcionales preparadas:

```text
tipo_comprobante,valor_venta,igv_pct,igv,total_con_igv
```

### detalle_pedidos.csv

```text
id_detalle,id_pedido,id_producto,cantidad,precio_unitario,subtotal
```

### produccion.csv

```text
id_orden,id_producto,cantidad,fecha,estado
```

### despachos.csv

```text
id_despacho,id_pedido,fecha_programada,fecha_entrega,estado
```

### feedback.csv

```text
id_feedback,id_pedido,id_cliente,puntuacion,comentario,fecha
```

## Modulos principales

### Clientes

Permite registrar, editar, eliminar y listar clientes. Los formularios usan modales para mantener la pantalla limpia.

### Productos e Insumos

Permite registrar, editar, eliminar y listar productos e insumos. Tambien muestra alertas de stock critico.

### Pedidos

Permite registrar pedidos con multiples productos para un mismo cliente.

El modal de registro incluye:

- Datos generales del pedido.
- Canal como lista desplegable.
- IGV fijo de 18%.
- Tabla editable de productos y cantidades.
- Resumen con productos y total.
- Tabla de resumen con valor venta, IGV y total por producto.

Un pedido se guarda en `pedidos.csv` y sus productos se guardan como varias lineas en `detalle_pedidos.csv`.

### Produccion

Permite registrar ordenes de produccion.

Si la orden queda como `pendiente`, no mueve inventario.

Si la orden queda como `completada`:

- Busca la receta del producto.
- Calcula consumo real usando merma.
- Valida stock suficiente.
- Descuenta insumos.
- Aumenta stock del producto terminado.

### Despachos

Permite registrar despachos con estados:

- programado
- en_ruta
- entregado
- retrasado
- cancelado

Si el despacho se registra como entregado, actualiza el pedido a `entregado`.

### Costos

El modulo de costos separa:

- Costo directo:
  - insumos teoricos
  - mano de obra directa
- Costo indirecto de fabricacion:
  - mermas
  - gas
  - energia
  - depreciacion
  - otros CIF

Tambien calcula:

- costo total unitario
- margen
- margen de contribucion
- punto de equilibrio
- umbral de margen por familia

La merma se toma desde `merma_pct` por insumo.

### Reportes Inteligentes

La pagina de reportes esta separada en tres pestañas:

- Reporte ejecutivo:
  - KPI principales
  - recomendaciones
  - exportacion de reporte ejecutivo
- Reporte de indicadores:
  - indicadores operativos
  - indicadores comerciales
  - ventas por producto
  - pedidos por cliente
  - pedidos por estado
  - indicadores financieros
  - rotacion de inventarios
- Reporte de graficos:
  - grafico de ventas por producto
  - grafico de pedidos por estado
  - grafico de stock critico
  - botones para guardar PNG en `output/graficos`

## Salidas generadas

Los archivos de salida solo se generan cuando el usuario presiona botones:

- `output/reportes/`
- `output/graficos/`
- `output/exportaciones/`

No se generan reportes, graficos ni exportaciones automaticamente al iniciar la aplicacion.

## Identidad visual

La identidad visual esta centralizada en `core/ui.py`.

Paleta:

- Primario: `#A5211C`
- Primario oscuro: `#7F1713`
- Terracota: `#BD5E57`
- Fondo principal: `#F4EBD8`
- Fondo de tarjetas: `#FBF6EF`
- Bordes: `#D6CAC0`
- Texto principal: `#2B211E`
- Texto secundario: `#6B5A55`

El CSS se inyecta con:

```python
st.markdown(..., unsafe_allow_html=True)
```

## Reglas importantes

- No se usa SQL.
- No se usa SQLite.
- No hay login ni roles.
- No hay API.
- No hay Docker.
- No se crean CSV automaticamente al iniciar.
- No se borran datos existentes.
- Los archivos se escriben solo cuando el usuario ejecuta una accion desde la interfaz.

## Validacion tecnica

Para validar sintaxis:

```bash
python -m compileall app.py config.py core modules analytics pages
```

## Dependencias

Ver `requirements.txt`:

```text
streamlit
pandas
numpy
matplotlib
```
