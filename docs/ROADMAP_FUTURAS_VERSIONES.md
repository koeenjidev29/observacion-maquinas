# 🗺️ ROADMAP - PROGRAMA DE OBSERVACIÓN DE MÁQUINAS

## 📊 Estado Actual: Versión 1.3.6
- ✅ Sistema básico de observaciones
- ✅ Gestión de fechas y máquinas
- ✅ Integración con Excel
- ✅ Sistema de filtrado
- ✅ Interfaz gráfica funcional

---

## 🎨 VERSIÓN 1.3.7 - REORGANIZACIÓN DE INTERFAZ (PRIORIDAD MÁXIMA)

### 🏠 **Nueva Estructura de Pantalla Principal**
**Objetivo**: Reorganizar la interfaz para una experiencia más intuitiva y centrada en las incidencias del día actual.

#### 📋 **Vista Principal Rediseñada**:
- **Vista por defecto**: Mostrar automáticamente todas las incidencias del día actual
- **Actualización automática**: Si cambia la fecha (día siguiente), se actualiza automáticamente a la nueva hoja
- **Enfoque diario**: El usuario siempre ve primero lo relevante del día

#### 🔄 **Nueva Organización de Controles**:
1. **Área principal**: Lista de incidencias del día actual (siempre visible)
2. **Botón "Nueva Incidencia"**: Movido a una posición más prominente
3. **Botón "Ver Lista Completa"**: Para acceder al historial completo (ya existente)
4. **Filtros avanzados**: Disponibles solo en "Ver Lista Completa"

#### 👤 **Permisos Diferenciados en "Nueva Incidencia"**:

**🔹 Usuario Normal**:
- ❌ No puede introducir incidencias
- ✅ Solo visualización

**🔧 Mecánico/Encargado**:
- ✅ Puede introducir nueva incidencia
- ✅ Campos editables: Máquina y Observación
- ❌ Fecha y hora: Automáticas (no modificables)
- 📅 Fecha/hora se asignan automáticamente al momento de creación

**👑 Administrador**:
- ✅ Puede introducir nueva incidencia
- ✅ Campos editables: Máquina, Observación, Fecha y Hora
- 📅 Fecha/hora por defecto: Momento actual (pero modificable)
- 🎛️ Control total sobre todos los campos

#### 🔄 **Flujo de Trabajo Mejorado**:
1. **Inicio del programa** → Vista automática de incidencias del día
2. **¿Nueva incidencia?** → Botón "Nueva Incidencia" (permisos según usuario)
3. **¿Ver historial?** → Botón "Ver Lista Completa"
4. **¿Filtrar historial?** → Filtros disponibles en "Ver Lista Completa"

#### 🎯 **Beneficios**:
- ✅ Interfaz más intuitiva y centrada en el día actual
- ✅ Menos clics para las acciones más comunes
- ✅ Separación clara entre vista diaria y historial
- ✅ Permisos diferenciados según tipo de usuario
- ✅ Actualización automática de fecha

---

## 🎯 VERSIÓN 1.4.0 - INTERFAZ RESPONSIVA (PRIORIDAD ALTA)

### 📱 **Diseño Adaptativo Automático**
**Objetivo**: Hacer que el programa se adapte automáticamente a cualquier resolución de pantalla.

#### Funcionalidades:
- **Auto-detección de resolución**
  - Detectar resolución actual del monitor al iniciar
  - Calcular factor de escalado automático
  - Ajustar todos los elementos proporcionalmente

- **Escalado inteligente**
  - Fuentes: Escalado proporcional según resolución
  - Botones: Tamaño adaptativo manteniendo usabilidad
  - Ventanas: Proporción óptima para cada pantalla
  - Espaciado: Ajuste automático de márgenes y padding

#### 🖥️ **Control de Ventana Inteligente**
- **Tamaños controlados**
  - Mínimo: 800x600 (funcionalidad básica)
  - Máximo: 90% de la pantalla disponible (con bordes del sistema)
  - Centrado automático en pantalla

- **Comportamiento de ventana**
  - ✅ Permitir minimizar
  - ✅ Permitir maximizar (pero controlado al 90% de pantalla)
  - ❌ Bloquear redimensionado manual por el usuario
  - ✅ Permitir mover la ventana

#### 📐 **Ejemplos de Resoluciones**
- **1920x1080 (Full HD)**: Ventana 1728x972 (90%)
- **2560x1440 (2K)**: Ventana 2304x1296 (90%)
- **3840x2160 (4K)**: Ventana 3456x1944 (90%)
- **Resoluciones custom**: Cálculo automático

#### 🔧 **Implementación Técnica**
- Módulo de detección de pantalla
- Sistema de escalado de fuentes
- Gestor de geometría de ventana
- Configuración automática de tkinter

---

## 🔐 VERSIÓN 1.5.0 - SISTEMA DE AUTENTICACIÓN

### 👤 **Sistema de Login**
**Objetivo**: Implementar control de acceso con diferentes niveles de permisos.

#### Pantalla de Login:
- **Ventana independiente** que aparece antes del programa principal
- **Campos**: Usuario y Contraseña
- **Validación**: Verificación contra usuarios predefinidos
- **Cierre automático** al login exitoso

#### 👥 **Usuarios Predefinidos**: