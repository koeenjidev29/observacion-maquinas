# Cambios en la Versión 1.3.5

**Fecha de lanzamiento:** 2024-12-19  
**Nombre de la versión:** Campo de Selección de Usuario

## 🆕 Nueva Funcionalidad

### Campo de Selección de Usuario
- **Ubicación:** Agregado debajo del campo de máquinas en la sección "Nueva Observación"
- **Propósito:** Permite seleccionar qué usuario está introduciendo la observación
- **Funcionalidad:** Lista desplegable con todos los usuarios registrados en el sistema
- **Integración:** Se conecta automáticamente con el sistema de gestión de usuarios

## 🔧 Mejoras en la Interfaz

### Formulario de Nueva Observación
- **Nuevo campo:** "Usuario" entre "Máquina" y "Observación"
- **Validación:** El campo de usuario es obligatorio para guardar observaciones
- **Persistencia:** El usuario seleccionado se mantiene después de limpiar campos para facilitar el uso continuo
- **Actualización automática:** La lista se actualiza cuando se modifican usuarios desde la gestión

### Experiencia de Usuario Mejorada
- **Usuario por defecto:** Se selecciona automáticamente el primer usuario disponible
- **Validación mejorada:** Mensaje de error claro si no se selecciona usuario
- **Flujo optimizado:** El usuario permanece seleccionado al limpiar otros campos

## 📁 Archivos Modificados

### `gui/main_window.py`
- **Variables añadidas:**
  - `self.selected_user`: Variable para el usuario seleccionado
  - `self.users`: Lista de usuarios disponibles
  - `self.user_combo`: Combo box para selección de usuario

- **Funciones modificadas:**
  - `__init__()`: Inicialización de variables de usuario
  - `setup_ui()`: Agregado campo de usuario en la interfaz
  - `save_observation()`: Validación y uso del usuario seleccionado
  - `clear_fields()`: Mantiene usuario seleccionado
  - `save_current_users()`: Actualiza lista de usuarios en combo

- **Funciones añadidas:**
  - `load_available_users()`: Carga usuarios desde archivo para el combo

### `version.py`
- Actualizado `VERSION_PATCH` a 5
- Actualizado `VERSION_NAME` a "Campo de Selección de Usuario"

### `version.txt`
- Actualizado a versión 1.3.5

## 🎯 Beneficios de esta Versión

1. **Trazabilidad mejorada:** Cada observación queda registrada con el usuario específico que la introdujo

2. **Flexibilidad de usuarios:** Cualquier usuario registrado puede ser seleccionado para una observación

3. **Integración completa:** Se conecta seamlessly con el sistema de gestión de usuarios existente

4. **Usabilidad optimizada:** El usuario seleccionado se mantiene para facilitar múltiples entradas consecutivas

5. **Validación robusta:** Previene observaciones sin usuario asignado

## 🔄 Flujo de Trabajo Actualizado

1. **Seleccionar fecha** (como antes)
2. **Seleccionar línea** (como antes)
3. **Seleccionar máquina** (como antes)
4. **🆕 Seleccionar usuario** (nuevo paso)
5. **Escribir observación** (como antes)
6. **Guardar** (con validación de usuario)

## 📋 Usuarios por Defecto

La aplicación incluye usuarios predeterminados:
- Produccion1 (Operador)
- Supervisor (Supervisor)
- Mantenimiento (Técnico)
- Administrador (Admin)

## 🔧 Notas Técnicas

- Los usuarios se cargan dinámicamente desde `data/usuarios.txt`
- La lista se actualiza automáticamente cuando se modifican usuarios
- El campo mantiene el estado entre operaciones para mejorar la eficiencia
- Manejo robusto de errores si el archivo de usuarios no existe

---

**Nota:** Esta versión completa la funcionalidad de gestión de usuarios, permitiendo ahora una trazabilidad completa de quién introduce cada observación en el sistema.