# Programa de Observación de Máquinas

## 🚀 Inicio Rápido

### Ejecutar el Programa
```bash
# Opción 1: Usar el acceso directo
ejecutar.bat

# Opción 2: Desde la carpeta scripts
scripts\ejecutar_programa.bat
```

### Ejecutar Pruebas
```bash
# Opción 1: Usar el acceso directo
pruebas.bat

# Opción 2: Desde la carpeta scripts
scripts\ejecutar_pruebas.bat
```

## 📁 Estructura del Proyecto

```
Programa observación/
├── 📄 ejecutar.bat          # Acceso rápido al programa
├── 📄 pruebas.bat           # Acceso rápido a las pruebas
├── 📄 main.py               # Archivo principal
├── 📄 version.py            # Control de versiones
├── 📄 requirements.txt      # Dependencias Python
├── 📄 test_programa.py      # Pruebas principales
├── 📄 test_simple.py        # Pruebas básicas
│
├── 📂 docs/                 # 📚 Documentación completa
│   ├── README.md            # Documentación principal
│   ├── INSTALACION.md       # Guía de instalación
│   ├── INICIO_RAPIDO.md     # Guía de inicio rápido
│   ├── SISTEMA_VERSIONES.md # Sistema de versiones
│   ├── CAMBIOS_VERSION_1.2.md
│   ├── CAMBIOS_VERSION_1.3.md
│   └── ...
│
├── 📂 scripts/              # 🔧 Scripts de ejecución
│   ├── ejecutar_programa.bat
│   ├── ejecutar_pruebas.bat
│   └── instalar_y_ejecutar.bat
│
├── 📂 gui/                  # 🖥️ Interfaz gráfica
│   ├── __init__.py
│   └── main_window.py
│
├── 📂 excel/                # 📊 Manejo de Excel
│   ├── __init__.py
│   └── excel_manager.py
│
├── 📂 utils/                # 🛠️ Utilidades
│   ├── __init__.py
│   └── helpers.py
│
└── 📂 data/                 # 💾 Datos y plantillas
    ├── observaciones.xlsx
    ├── test_observaciones.xlsx
    └── crear_plantilla.py
```

## 📚 Documentación

Toda la documentación está organizada en la carpeta `docs/`:

- **[README.md](docs/README.md)** - Documentación completa del programa
- **[INSTALACION.md](docs/INSTALACION.md)** - Guía de instalación paso a paso
- **[INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)** - Cómo empezar rápidamente
- **[SISTEMA_VERSIONES.md](docs/SISTEMA_VERSIONES.md)** - Control de versiones centralizado
- **[CAMBIOS_VERSION_1.3.md](docs/CAMBIOS_VERSION_1.3.md)** - Últimas funcionalidades

## ⚡ Versión Actual

**Versión 1.3.8** - [Nombre de la versión]
**Desarrollador**: koeenji dev  
**Fecha**: 2024-12-20

### Nuevas Funcionalidades v1.3
- ✅ Filtrado por períodos (día, semana, 15 días, mes)
- ✅ Filtros personalizados con rangos de fechas
- ✅ Tabla expandida con columnas Fecha y Línea
- ✅ Interfaz mejorada con información contextual

## 🔧 Desarrollo

### Estructura de Código
- **Modular**: Cada componente en su carpeta específica
- **Documentado**: Documentación completa en `docs/`
- **Versionado**: Sistema centralizado en `version.py`
- **Probado**: Scripts de prueba automatizados

### Scripts Disponibles
- `ejecutar.bat` - Ejecuta el programa principal
- `pruebas.bat` - Ejecuta todas las pruebas
- `scripts/instalar_y_ejecutar.bat` - Instalación completa

---

**¿Necesitas ayuda?** Consulta la documentación completa en la carpeta `docs/`