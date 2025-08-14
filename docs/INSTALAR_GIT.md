# 🔧 Instalación de Git para Windows

## ❌ Problema Detectado

El error `git : El término 'git' no se reconoce` indica que **Git no está instalado** en tu sistema Windows.

## ✅ Solución: Instalar Git

### Opción 1: Descarga Oficial (Recomendada)

1. **Ir a la página oficial:**
   ```
   https://git-scm.com/download/win
   ```

2. **Descargar automáticamente:**
   - Se descargará automáticamente la versión más reciente
   - Archivo: `Git-X.XX.X-64-bit.exe`

3. **Instalar con configuración recomendada:**
   - ✅ Ejecutar el instalador como administrador
   - ✅ Usar configuración por defecto
   - ✅ Seleccionar "Git from the command line and also from 3rd-party software"
   - ✅ Usar OpenSSL library
   - ✅ Checkout Windows-style, commit Unix-style line endings

### Opción 2: Winget (Windows 11/10)

```powershell
# Ejecutar como administrador
winget install --id Git.Git -e --source winget
```

### Opción 3: Chocolatey

```powershell
# Instalar Chocolatey primero (si no lo tienes)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Git
choco install git
```

## 🔄 Verificar Instalación

**Reiniciar PowerShell** y ejecutar:

```powershell
git --version
```

**Resultado esperado:**
```
git version 2.XX.X.windows.X
```

## ⚙️ Configuración Inicial

```powershell
# Configurar nombre y email
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

# Verificar configuración
git config --list
```

## 🚀 Continuar con GitHub

**Una vez instalado Git, ejecutar:**

```powershell
cd "C:\Users\Produccion1\Documents\Programa observación"
git init
git add .
git commit -m "Versión inicial 1.3.0 - Sistema de Filtrado por Períodos"
git remote add origin https://github.com/koeenjidev29/observacion-maquinas.git
git branch -M main
git push -u origin main
```

## 🆘 Solución de Problemas

### Error: "git no se reconoce"
- ✅ Reiniciar PowerShell/CMD
- ✅ Reiniciar el sistema
- ✅ Verificar que Git esté en PATH

### Error: "Permission denied"
- ✅ Ejecutar PowerShell como administrador
- ✅ Configurar SSH keys para GitHub

### Error: "Repository not found"
- ✅ Crear primero el repositorio en GitHub
- ✅ Verificar que el nombre sea exacto: `observacion-maquinas`

## 📱 Alternativas Gráficas

Si prefieres una interfaz gráfica:

- **GitHub Desktop**: https://desktop.github.com/
- **GitKraken**: https://www.gitkraken.com/
- **SourceTree**: https://www.sourcetreeapp.com/

---

**¡Una vez instalado Git, podrás subir tu proyecto a GitHub sin problemas!**