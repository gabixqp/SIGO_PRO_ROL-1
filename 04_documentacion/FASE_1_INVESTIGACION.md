# FASE 1 — Investigación del Rol 1 Integrador

## 1. Proyecto

**Nombre del sistema:** SIGO-PRO FoodOps
**Empresa piloto:** Gourmet Señor de Locumba S.A.C.
**RUC:** 20612215546
**Ubicación:** Tiabaya, Arequipa
**Curso:** Computación Aplicada
**Carrera:** Ingeniería Industrial

## 2. Rol asignado

El rol asignado es el **Rol 1 — Integrador del sistema**.

Este rol se enfoca en la arquitectura general del proyecto, configuración central, almacenamiento, navegación multipágina, identidad visual, experiencia de usuario, documentación y evidencias de integración.

## 3. Alcance del Rol 1

El Rol 1 no se encarga de rehacer toda la lógica de negocio del sistema. Su función principal es lograr que el software se vea, funcione y se presente como un producto integrado.

El alcance incluye:

* Revisar la arquitectura general del proyecto.
* Ordenar la estructura de carpetas.
* Centralizar configuración en `config.py`.
* Mejorar la interfaz visual mediante `core/ui.py`.
* Mejorar la portada e inicio del sistema en `app.py`.
* Asegurar navegación clara entre módulos.
* Revisar almacenamiento básico en `core/storage.py`.
* Mejorar validaciones compartidas en `core/validaciones.py` y `core/limpieza.py`.
* Preparar evidencias de integración.
* Documentar el proceso de mejora.
* Registrar el uso de IA mediante bitácora.

## 4. Estructura actual detectada

La estructura base del sistema contiene:

```text
SIGO_PRO/
├── app.py
├── config.py
├── README.md
├── requirements.txt
├── analytics/
├── core/
├── data/
├── modules/
├── output/
└── pages/
```

## 5. Diagnóstico general

El sistema ya cuenta con una estructura modular clara. Existen carpetas separadas para la lógica del negocio, analítica, datos, páginas, salida de reportes y utilidades compartidas.

Sin embargo, todavía falta fortalecer la parte visual, la documentación del rol, las evidencias, los respaldos, los registros de cambios y la experiencia de usuario final.

## 6. Archivos prioritarios para el Rol 1

Los archivos prioritarios son:

* `app.py`
* `config.py`
* `core/ui.py`
* `core/storage.py`
* `core/validaciones.py`
* `core/limpieza.py`
* `pages/1_Inicio.py`
* `pages/9_Configuracion.py`
* `pages/8_Reportes_Inteligentes.py`
* `README.md`
* `requirements.txt`

## 7. Archivos que no se modificarán inicialmente

No se modificarán inicialmente los archivos de lógica de negocio:

* `modules/clientes.py`
* `modules/pedidos.py`
* `modules/productos.py`
* `modules/insumos.py`
* `modules/recetas.py`
* `modules/produccion.py`
* `modules/despachos.py`
* `modules/costos.py`
* `modules/recomendaciones.py`

Tampoco se modificarán inicialmente los archivos internos de analítica:

* `analytics/indicadores.py`
* `analytics/reportes.py`
* `analytics/graficos.py`
* `analytics/optimizacion.py`

## 8. Riesgos detectados

1. Romper la lógica de otros roles al modificar módulos internos.
2. Duplicar estilos visuales en distintas páginas.
3. Romper rutas al agregar recursos visuales.
4. Sobrescribir archivos CSV sin respaldo.
5. Crear una visual demasiado pesada con videos grandes.
6. Priorizar estética sobre usabilidad.
7. No generar evidencias suficientes para la defensa.

## 9. Decisión de trabajo

Se trabajará primero en diagnóstico, diseño UX/UI y documentación. Luego se implementarán mejoras controladas en `config.py`, `core/ui.py` y `app.py`.

La lógica de negocio de otros roles solo se tocará si es estrictamente necesario para integración visual o compatibilidad.

## 10. Evidencias requeridas

Se deberán generar las siguientes evidencias:

* Capturas del sistema antes de la mejora.
* Capturas del sistema después de la mejora.
* Árbol de carpetas inicial y final.
* Registro de cambios.
* Bitácora de uso de IA.
* Prueba de navegación.
* Prueba de integración del flujo cliente → pedido → producción → despacho → reporte.
* Manual básico de instalación y ejecución.
* Informe final del Rol 1.

## 11. Resultado de la fase

La Fase 1 permite dejar claro qué existe, qué se debe mejorar y qué archivos forman parte del alcance del Rol 1 Integrador.
