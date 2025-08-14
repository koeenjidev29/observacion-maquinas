# Programa de Observación de Máquinas - Versión 1.2

## Cambios Implementados

### Nueva Funcionalidad: Selección por Líneas de Producción

La versión 1.2 introduce un sistema jerárquico de selección que permite organizar las máquinas por líneas de producción.

#### Características Principales:

1. **Selección de Línea**: 
   - Se agregó un nuevo campo "Línea" en la interfaz
   - El usuario debe seleccionar primero la línea de producción
   - Disponibles 5 líneas de producción (LÍNEA 1 a LÍNEA 5)

2. **Filtrado Dinámico de Máquinas**:
   - Las máquinas se filtran automáticamente según la línea seleccionada
   - Solo se muestran las máquinas correspondientes a la línea elegida
   - El campo de máquina se limpia automáticamente al cambiar de línea

3. **Estructura de Máquinas por Línea**:
   - **LÍNEA 1**: MÁQUINA 30 T8, MÁQUINA 31 T12, MÁQUINA 32 T23, MÁQUINA 33 T16
   - **LÍNEA 2**: MÁQUINA 29 T8, MÁQUINA 28 T12, MÁQUINA 27 T15, MÁQUINA 26 T20, MÁQUINA 25 T18
   - **LÍNEA 3**: MÁQUINA 24 T10, MÁQUINA 23 T14, MÁQUINA 22 T16, MÁQUINA 21 T22
   - **LÍNEA 4**: MÁQUINA 20 T12, MÁQUINA 19 T18, MÁQUINA 18 T25, MÁQUINA 17 T30
   - **LÍNEA 5**: MÁQUINA 16 T8, MÁQUINA 15 T12, MÁQUINA 14 T16, MÁQUINA 13 T20, MÁQUINA 12 T24

#### Validaciones Mejoradas:

- Se agregó validación obligatoria para la selección de línea
- El usuario debe seleccionar tanto línea como máquina antes de guardar
- Mensajes informativos en la barra de estado sobre líneas y máquinas disponibles

#### Archivos Modificados:

1. **`utils/helpers.py`**:
   - Agregada función `get_production_lines()`: Retorna la estructura completa de líneas y máquinas
   - Agregada función `get_lines_list()`: Retorna solo la lista de líneas disponibles
   - Agregada función `get_machines_by_line()`: Retorna las máquinas de una línea específica
   - Modificada función `get_default_machines()`: Mantiene compatibilidad retornando todas las máquinas

2. **`gui/main_window.py`**:
   - Agregado campo de selección de línea en la interfaz
   - Implementado método `on_line_selected()` para filtrado dinámico
   - Actualizado método `clear_fields()` para incluir limpieza de línea
   - Mejorado método `save_observation()` con validación de línea
   - Reorganizada la interfaz para acomodar el nuevo campo

#### Flujo de Uso:

1. El usuario selecciona una fecha
2. El usuario selecciona una línea de producción
3. Automáticamente se cargan las máquinas de esa línea
4. El usuario selecciona una máquina específica
5. El usuario ingresa la observación
6. Se guarda la observación con toda la información

#### Compatibilidad:

- La versión 1.2 mantiene compatibilidad con archivos Excel existentes
- Los datos anteriores siguen siendo accesibles
- Las funciones antiguas se mantienen para compatibilidad hacia atrás

## Instalación y Ejecución

Para ejecutar la versión 1.2:

```bash
# Ejecutar el programa
.\ejecutar_programa.bat

# Ejecutar las pruebas
.\ejecutar_pruebas.bat
```

## Notas Técnicas

- Se mantiene la estructura de archivos Excel existente
- Las observaciones se siguen guardando con el mismo formato
- La interfaz es más intuitiva y organizada
- Mejor experiencia de usuario con filtrado automático

---

**Versión**: 1.2  
**Fecha**: $(Get-Date -Format "yyyy-MM-dd")  
**Estado**: Funcional y probado