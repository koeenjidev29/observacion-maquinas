# Cambios en Versión 1.3.3 - Menú Contextual y Archivo de Versión

**Fecha de lanzamiento:** 19 de diciembre de 2024

## Nuevas Funcionalidades

### 1. Archivo de Versión (version.txt)

**Descripción:**
Se ha agregado un archivo `version.txt` en la raíz del proyecto que contiene la versión actual del programa.

**Características:**
- ✅ Archivo `version.txt` que muestra la versión actual (1.3.3)
- ✅ Script automático `update_version_txt.py` para sincronizar la versión
- ✅ Archivo batch `actualizar_version.bat` para ejecutar fácilmente la actualización

**Ubicación de archivos:**
- `version.txt` - Archivo con la versión actual
- `scripts/update_version_txt.py` - Script para actualizar automáticamente
- `scripts/actualizar_version.bat` - Ejecutable para actualizar la versión

### 2. Menú Contextual en Tabla de Observaciones

**Descripción:**
Se ha implementado un menú contextual (click derecho) en la tabla de observaciones que permite editar y eliminar observaciones directamente desde la tabla.

**Funcionalidades del menú contextual:**
- ✅ **Editar Observación**: Permite modificar una observación seleccionada
- ✅ **Eliminar Observación**: Permite eliminar una observación seleccionada
- ✅ **Protección por contraseña**: Ambas opciones requieren la misma contraseña que el menú de herramientas
- ✅ **Confirmación de eliminación**: Muestra un diálogo de confirmación antes de eliminar

**Cómo usar el menú contextual:**
1. Hacer click derecho sobre cualquier observación en la tabla
2. Seleccionar "Editar Observación" o "Eliminar Observación"
3. Ingresar la contraseña de administrador (misma que en el menú Herramientas)
4. Confirmar la acción

## Archivos Modificados

### Nuevos archivos creados:
- ✅ `version.txt` - Archivo con la versión actual
- ✅ `scripts/update_version_txt.py` - Script de actualización automática
- ✅ `scripts/actualizar_version.bat` - Ejecutable para actualizar versión
- ✅ `docs/CAMBIOS_v1.3.3.md` - Documentación de cambios

### Archivos modificados:
- ✅ `gui/main_window.py`:
  - Agregada función `setup_context_menu()` para configurar el menú contextual
  - Agregada función `show_context_menu()` para mostrar el menú en la posición correcta
  - Agregada función `context_edit_observation()` para editar desde el menú contextual
  - Agregada función `context_delete_observation()` para eliminar desde el menú contextual
  - Modificada función `setup_observations_table()` para incluir el menú contextual

- ✅ `version.py`:
  - Actualizada versión a 1.3.3
  - Actualizado nombre de versión a "Menú Contextual y Archivo de Versión"

## Funcionalidad Verificada

- ✅ Menú contextual aparece al hacer click derecho en observaciones
- ✅ Edición de observaciones desde menú contextual con protección por contraseña
- ✅ Eliminación de observaciones desde menú contextual con confirmación
- ✅ Archivo version.txt actualizado con la versión correcta
- ✅ Scripts de actualización de versión funcionando
- ✅ Compatibilidad con funcionalidades existentes

## Mejoras de Usabilidad

1. **Acceso rápido**: El menú contextual proporciona acceso directo a las funciones de edición y eliminación sin necesidad de usar el menú superior.

2. **Consistencia**: Las mismas protecciones de seguridad (contraseña) se aplican tanto en el menú de herramientas como en el menú contextual.

3. **Confirmación visual**: Los diálogos de confirmación ayudan a prevenir eliminaciones accidentales.

4. **Gestión de versión**: El archivo version.txt facilita la identificación rápida de la versión del programa.

## Notas Técnicas

- El menú contextual se activa con el evento `<Button-3>` (click derecho)
- La selección automática del item bajo el cursor mejora la experiencia de usuario
- El script `update_version_txt.py` lee directamente del módulo `version.py` para mantener sincronización
- Todas las funciones mantienen la misma lógica de validación y manejo de errores que las versiones del menú principal