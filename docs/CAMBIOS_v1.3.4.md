# Cambios en la Versión 1.3.4

**Fecha de lanzamiento:** 2024-12-19  
**Nombre de la versión:** Consola de Depuración y Gestión de Usuarios

## 🆕 Nuevas Funcionalidades

### 1. Consola de Depuración
- **Acceso protegido:** Se accede mediante contraseña (1111) desde el menú Herramientas
- **Información del sistema:** Muestra versión, fecha, archivo Excel y estado general
- **Verificación de archivos:** Comprueba la existencia y tamaño del archivo Excel
- **Logs de hojas:** Lista las hojas disponibles en el archivo Excel
- **Funciones de control:**
  - Limpiar consola
  - Actualizar logs
  - Exportar logs a archivo de texto
- **Propósito:** Ayuda a diagnosticar errores como "no se puede eliminar esta línea"

### 2. Sistema de Gestión de Usuarios
- **Acceso protegido:** Se accede mediante contraseña (1111) desde el menú Herramientas o botón "Usuarios"
- **Botón de acceso rápido:** Nuevo botón "Usuarios" ubicado junto al campo de máquinas
- **Funcionalidades completas:**
  - Añadir nuevos usuarios
  - Modificar usuarios existentes
  - Eliminar usuarios
  - Actualizar lista de usuarios
- **Roles disponibles:** Operador, Técnico, Supervisor, Admin
- **Almacenamiento:** Los usuarios se guardan en `data/usuarios.txt`
- **Usuarios por defecto:**
  - Produccion1 (Operador)
  - Supervisor (Supervisor)
  - Mantenimiento (Técnico)
  - Administrador (Admin)

## 🔧 Mejoras en la Interfaz

### Menú de Herramientas Ampliado
- Añadida opción "Consola de Depuración"
- Añadida opción "Gestión de Usuarios"
- Ambas opciones requieren autenticación con contraseña

### Botón de Acceso Rápido
- Nuevo botón "Usuarios" en la sección de entrada de datos
- Ubicado estratégicamente junto al campo de máquinas
- Proporciona acceso directo a la gestión de usuarios

## 📁 Archivos Modificados

### `gui/main_window.py`
- Añadidas funciones para consola de depuración:
  - `open_debug_console()`
  - `clear_debug_console()`
  - `refresh_debug_logs()`
  - `export_debug_logs()`
- Añadidas funciones para gestión de usuarios:
  - `open_user_management()`
  - `refresh_users()`
  - `load_users_from_file()`
  - `save_users_to_file()`
  - `add_user()`, `modify_user()`, `delete_user()`
  - `show_user_dialog()`
  - `save_current_users()`
- Actualizado menú de herramientas
- Añadido botón "Usuarios" en la interfaz principal

### `version.py`
- Actualizado `VERSION_PATCH` a 4
- Actualizado `VERSION_NAME` a "Consola de Depuración y Gestión de Usuarios"

### `version.txt`
- Actualizado a versión 1.3.4

## 🎯 Beneficios de esta Versión

1. **Mejor diagnóstico de errores:** La consola de depuración permite identificar y resolver problemas como errores de eliminación de líneas

2. **Gestión centralizada de usuarios:** Sistema completo para administrar usuarios del sistema

3. **Acceso rápido:** El botón "Usuarios" facilita el acceso a la gestión sin navegar por menús

4. **Seguridad mantenida:** Ambas funcionalidades requieren autenticación con contraseña

5. **Información detallada:** La consola proporciona información técnica útil para el mantenimiento del sistema

## 🔒 Seguridad

- Todas las nuevas funcionalidades están protegidas con contraseña (1111)
- Los usuarios se almacenan de forma segura en archivos de texto
- Las funciones de depuración no exponen información sensible

---

**Nota:** Esta versión mejora significativamente las capacidades de diagnóstico y administración del sistema, proporcionando herramientas esenciales para el mantenimiento y gestión de usuarios.