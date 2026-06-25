# FASE 2 — UX y Design Brief

## 1. Nombre del sistema

**SIGO-PRO FoodOps**

Sistema de gestión operativa para Gourmet Señor de Locumba S.A.C.

## 2. Propósito del diseño

El propósito del rediseño visual es transformar SIGO-PRO FoodOps en un software más moderno, profesional, claro e integrado, manteniendo la funcionalidad existente y respetando los módulos desarrollados por cada rol del equipo.

La mejora visual no busca cambiar la lógica de negocio, sino mejorar la experiencia del usuario, la navegación, la presentación de datos y la coherencia general del sistema.

## 3. Rol responsable

**Rol 1 — Integrador del sistema**

Responsable de:

* Arquitectura general.
* Configuración central.
* Almacenamiento compartido.
* Navegación multipágina.
* Identidad visual.
* Experiencia de usuario.
* Evidencias de integración.
* Documentación del sistema.

## 4. Usuario objetivo

El sistema está pensado para usuarios administrativos y operativos de una empresa de servicios de alimentación.

Usuarios principales:

1. Administrador general.
2. Encargado de pedidos.
3. Encargado de producción.
4. Encargado de inventario.
5. Encargado de costos.
6. Encargado de despacho.
7. Equipo evaluador o docente.

## 5. Experiencia deseada

El sistema debe sentirse:

* Moderno.
* Ordenado.
* Confiable.
* Profesional.
* Fácil de navegar.
* Visualmente atractivo.
* Coherente entre páginas.
* Orientado a toma de decisiones.

## 6. Inspiración visual

La pantalla principal debe inspirarse en una landing page moderna con:

* Fondo de video a pantalla completa.
* Encabezado tipo glassmorphism.
* Contenido hero ubicado en la parte inferior izquierda.
* Mensaje principal claro.
* Accesos rápidos a módulos.
* Tarjetas visuales.
* Estética gastronómica y empresarial.

## 7. Estilo visual propuesto

### Paleta de colores

* Rojo vino: identidad gastronómica y fuerza visual.
* Negro carbón: elegancia y contraste.
* Crema claro: calidez y legibilidad.
* Blanco: limpieza visual.
* Dorado suave: detalle premium.
* Verde: estados correctos o confirmados.
* Amarillo: advertencias.
* Rojo: alertas críticas.

### Estilo general

El diseño debe combinar una estética gastronómica con una presentación empresarial. Debe parecer un sistema real para gestión alimentaria, no una maqueta universitaria.

## 8. Estructura de navegación

El sistema tendrá navegación multipágina mediante sidebar.

Páginas principales:

1. Inicio
2. Clientes
3. Productos e insumos
4. Pedidos
5. Producción
6. Despachos
7. Costos
8. Reportes inteligentes
9. Configuración

## 9. Jerarquía visual

Cada página deberá tener:

1. Título claro.
2. Subtítulo explicativo.
3. Métricas principales.
4. Filtros si corresponde.
5. Área de registro o edición.
6. Tabla de datos.
7. Alertas o recomendaciones.
8. Pie visual o nota de estado.

## 10. Componentes visuales requeridos

Se deberán crear componentes reutilizables en `core/ui.py`:

* Encabezado visual.
* Hero section.
* Tarjeta KPI.
* Tarjeta de módulo.
* Tarjeta de alerta.
* Badge de estado.
* Separador de sección.
* Tabla estilizada.
* Mensaje de éxito.
* Mensaje de advertencia.
* Mensaje de error.
* Footer.

## 11. Recursos visuales necesarios

Se necesitarán los siguientes recursos:

* Logo de Gourmet Señor de Locumba.
* Video de fondo para la portada.
* Imagen fallback para cuando el video no cargue.
* Imágenes de productos.
* Iconos para módulos.
* Fondos secundarios.
* Posibles mockups para documentación y defensa.

## 12. Restricciones técnicas

El sistema está desarrollado en Streamlit, por lo tanto:

* No se implementará React real dentro del sistema.
* Se imitará la estética moderna mediante CSS, HTML embebido y componentes de Streamlit.
* El video debe estar optimizado para no volver lenta la app.
* La navegación debe seguir siendo compatible con `pages/`.
* No se debe romper la lógica de negocio existente.
* Las rutas visuales deben centralizarse en `config.py`.

## 13. Principios UX

El rediseño debe cumplir estos principios:

1. Claridad antes que decoración.
2. Menos pasos para llegar a cada módulo.
3. Mensajes entendibles para usuarios no técnicos.
4. Tablas limpias y fáciles de leer.
5. Estados visuales claros.
6. Alertas visibles pero no invasivas.
7. Diseño consistente en todas las páginas.
8. Portada impactante, módulos internos funcionales.

## 14. Flujo principal del sistema

El flujo integrado que debe poder demostrarse es:

```text
Cliente → Pedido → Producción → Despacho → Reporte
```

Este flujo será usado como prueba principal del Rol 1.

## 15. Evidencias de esta fase

Se deberán guardar evidencias de:

* Documento Design Brief.
* Carpeta de diseño creada.
* Referencias visuales seleccionadas.
* Primer moodboard.
* Flujo de navegación.
* Registro de decisiones UX/UI.

## 16. Resultado esperado

Al finalizar esta fase, el proyecto contará con una guía clara para rediseñar la experiencia visual y de navegación de SIGO-PRO FoodOps sin improvisar y sin romper los módulos existentes.
