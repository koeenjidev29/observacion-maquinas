@echo off
echo Actualizando archivo version.txt...
cd /d "%~dp0.."
python scripts\update_version_txt.py
echo.
echo Presiona cualquier tecla para continuar...
pause >nul