@echo off
chcp 65001 >nul
echo ================================================
echo   Programa de Observación de Máquinas
echo   Instalador y Ejecutor Automático
echo ================================================
echo.

:: Verificar si Python está instalado
echo [1/4] Verificando instalación de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    echo.
    echo ================================================
    echo   PYTHON NO ENCONTRADO - ACCIÓN REQUERIDA
    echo ================================================
    echo.
    echo 1. Instale Python desde Microsoft Store:
    echo    - Abrir Microsoft Store
    echo    - Buscar "Python 3.12" o "Python 3.11"
    echo    - Hacer clic en "Obtener" o "Instalar"
    echo.
    echo 2. O desde el sitio oficial:
    echo    - Ir a https://www.python.org/downloads/
    echo    - Descargar Python 3.11 o superior
    echo    - IMPORTANTE: Marcar "Add Python to PATH"
    echo.
    echo 3. Después de instalar:
    echo    - Reiniciar el sistema
    echo    - Ejecutar este archivo nuevamente
    echo.
    echo Consulte INSTALAR_PYTHON_PRIMERO.md para más detalles
    echo.
    pause
    exit /b 1
)
echo ✅ Python encontrado
python --version
echo.

:: Instalar dependencias
echo [2/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error al instalar dependencias
    echo Intentando con pip3...
    pip3 install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar dependencias con pip3
        pause
        exit /b 1
    )
)
echo ✅ Dependencias instaladas correctamente
echo.

:: Crear directorio de datos
echo [3/4] Preparando directorios...
if not exist "data" mkdir data
echo ✅ Directorios preparados
echo.

:: Ejecutar programa
echo [4/4] Iniciando programa...
echo.
echo ================================================
echo   Iniciando Programa de Observación de Máquinas
echo ================================================
echo.
python main.py

:: Si hay error, mostrar mensaje
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error al ejecutar el programa
    echo.
    echo Posibles soluciones:
    echo 1. Verificar que Python esté correctamente instalado
    echo 2. Ejecutar como administrador
    echo 3. Verificar permisos de escritura en la carpeta
    echo.
    pause
)

echo.
echo Programa finalizado.
pause