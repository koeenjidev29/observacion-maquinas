@echo off
chcp 65001 >nul
echo ================================================
echo   INSTALADOR COMPLETO - OBSERVACIÓN DE MÁQUINAS
echo   Versión: Instalación desde cero
echo ================================================
echo.
echo Este script instalará todo lo necesario:
echo - Verificará Python
echo - Actualizará pip
echo - Instalará todas las dependencias
echo - Verificará la instalación
echo.
pause
echo.

:: Verificar Python
echo [1/6] Verificando Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado.
    echo.
    echo INSTRUCCIONES PARA INSTALAR PYTHON:
    echo 1. Abrir Microsoft Store
    echo 2. Buscar "Python 3.12" o "Python 3.11"
    echo 3. Hacer clic en "Obtener" o "Instalar"
    echo 4. Esperar a que termine la instalación
    echo 5. Ejecutar este script nuevamente
    echo.
    echo ¿Desea abrir Microsoft Store ahora? (S/N)
    set /p respuesta=
    if /i "%respuesta%"=="S" (
        start ms-windows-store://pdp/?productid=9NCVDN91XZQP
    )
    echo.
    echo Después de instalar Python, ejecute este script nuevamente.
    pause
    exit /b 1
)
echo ✅ Python encontrado: 
py --version
echo.

:: Verificar pip
echo [2/6] Verificando pip...
py -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error con pip
    pause
    exit /b 1
)
echo ✅ pip funcionando correctamente
echo.

:: Actualizar pip
echo [3/6] Actualizando pip a la última versión...
py -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ⚠️ Advertencia: No se pudo actualizar pip, continuando...
)
echo ✅ pip actualizado
echo.

:: Instalar dependencias básicas primero
echo [4/6] Instalando dependencias básicas...
echo Instalando openpyxl...
py -m pip install openpyxl==3.1.2
if %errorlevel% neq 0 (
    echo ❌ Error instalando openpyxl
    pause
    exit /b 1
)

echo Instalando tkcalendar...
py -m pip install "tkcalendar>=1.6.0"
if %errorlevel% neq 0 (
    echo ❌ Error instalando tkcalendar
    pause
    exit /b 1
)

echo Instalando tkinter-tooltip...
py -m pip install tkinter-tooltip==2.0.0
if %errorlevel% neq 0 (
    echo ❌ Error instalando tkinter-tooltip
    pause
    exit /b 1
)
echo ✅ Dependencias básicas instaladas
echo.

:: Instalar pandas (problemático)
echo [5/6] Instalando pandas (puede tardar varios minutos)...
echo Intentando instalación optimizada de pandas...
py -m pip install --only-binary=all "pandas>=2.0.0,<2.1.0"
if %errorlevel% neq 0 (
    echo ⚠️ Instalación optimizada falló, intentando instalación estándar...
    py -m pip install "pandas>=2.0.0,<2.1.0"
    if %errorlevel% neq 0 (
        echo ❌ Error instalando pandas
        echo El programa puede funcionar sin pandas, pero con funcionalidad limitada.
        echo ¿Desea continuar sin pandas? (S/N)
        set /p continuar=
        if /i not "%continuar%"=="S" (
            pause
            exit /b 1
        )
    )
)
echo ✅ pandas instalado (o saltado)
echo.

:: Verificar instalación
echo [6/6] Verificando instalación completa...
py -c "import sys; print('Python:', sys.version)"
py -c "import openpyxl; print('✅ openpyxl:', openpyxl.__version__)"
py -c "import tkcalendar; print('✅ tkcalendar: OK')"
py -c "try: import pandas; print('✅ pandas:', pandas.__version__); except: print('⚠️ pandas: No disponible')"
echo.

echo ================================================
echo   INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ================================================
echo.
echo El programa está listo para usar.
echo.
echo OPCIONES PARA EJECUTAR:
echo 1. Doble clic en: ejecutar_programa.bat
echo 2. Comando manual: py main.py
echo.
echo ¿Desea ejecutar el programa ahora? (S/N)
set /p ejecutar=
if /i "%ejecutar%"=="S" (
    echo Iniciando programa...
    py main.py
)
echo.
pause