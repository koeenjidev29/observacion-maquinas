# 📚 Guía para Subir el Proyecto a GitHub

## 🎯 Pasos para Subir tu Proyecto

### ⚠️ IMPORTANTE: Instalar Git Primero

**Si ves el error "git no se reconoce"**, necesitas instalar Git:
- 📖 Ver guía completa: `INSTALAR_GIT.md`
- 🔗 Descarga directa: https://git-scm.com/download/win
- ⚡ Instalación rápida: Ejecutar instalador con configuración por defecto
- 🔄 **Reiniciar PowerShell** después de instalar

### 1. Preparar el Repositorio Local

```bash
# Navegar a la carpeta del proyecto
cd "C:\Users\Produccion1\Documents\Programa observación"

# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Versión inicial 1.3.0 - Sistema de Filtrado por Períodos"
```

### 2. Crear Repositorio en GitHub

1. **Ir a GitHub**: https://github.com
2. **Hacer clic en "New repository"** (botón verde)
3. **Configurar el repositorio**:
   - **Repository name**: `programa-observacion-maquinas`
   - **Description**: `Sistema completo para el registro y filtrado de observaciones de máquinas industriales`
   - **Visibility**: `Public` (para que sea accesible desde casa)
   - **NO marcar** "Add a README file" (ya tenemos uno)
   - **NO marcar** "Add .gitignore" (ya tenemos uno)
   - **Seleccionar** "MIT License" o dejar sin licencia (ya tenemos una)
4. **Hacer clic en "Create repository"**

### 3. Conectar y Subir

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/koeenjidev29/observacion-maquinas.git

# Cambiar a la rama main (GitHub usa 'main' por defecto)
git branch -M main

# Subir el código
git push -u origin main
```

## 🏠 Trabajar desde Casa

### Clonar el Proyecto en Casa

```bash
# Clonar el repositorio
git clone https://github.com/koeenjidev29/observacion-maquinas.git

# Entrar a la carpeta
cd observacion-maquinas

# Instalar y ejecutar
scripts\instalar_y_ejecutar.bat
```

### Sincronizar Cambios

**Desde el Trabajo (subir cambios):**
```bash
# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios realizados"

# Subir cambios
git push
```

**Desde Casa (descargar cambios):**
```bash
# Descargar últimos cambios
git pull

# Ejecutar el programa actualizado
ejecutar.bat
```

## 📋 Comandos Git Útiles

### Comandos Básicos
```bash
# Ver estado de archivos
git status

# Ver historial de commits
git log --oneline

# Ver diferencias
git diff

# Agregar archivos específicos
git add archivo.py

# Commit con mensaje
git commit -m "Mensaje descriptivo"
```

### Manejo de Ramas
```bash
# Crear nueva rama para una funcionalidad
git checkout -b nueva-funcionalidad

# Cambiar de rama
git checkout main

# Fusionar rama
git merge nueva-funcionalidad

# Eliminar rama
git branch -d nueva-funcionalidad
```

## 🔒 Configuración Inicial de Git

**Primera vez usando Git:**
```bash
# Configurar nombre y email
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

# Verificar configuración
git config --list
```

## 📁 Archivos Importantes para GitHub

### ✅ Ya Incluidos en el Proyecto
- `README_GITHUB.md` - Documentación principal para GitHub
- `.gitignore` - Archivos a ignorar
- `LICENSE` - Licencia MIT
- `requirements.txt` - Dependencias Python

### 📝 Recomendaciones

1. **README Principal**: Renombrar `README_GITHUB.md` a `README.md` antes de subir
2. **Documentación**: La carpeta `docs/` contiene toda la documentación técnica
3. **Releases**: Crear releases para cada versión importante
4. **Issues**: Usar GitHub Issues para reportar problemas
5. **Wiki**: Considerar usar GitHub Wiki para documentación extendida

## 🚀 Flujo de Trabajo Recomendado

### En el Trabajo
1. Hacer cambios al código
2. Probar con `pruebas.bat`
3. Commit y push a GitHub
4. Documentar cambios importantes

### En Casa
1. `git pull` para obtener últimos cambios
2. Trabajar en nuevas funcionalidades
3. Crear rama para cambios grandes
4. Commit y push cuando esté listo

## 🔧 Solución de Problemas

### Error: "Repository not found"
- Verificar que el nombre del repositorio sea correcto
- Verificar que tengas permisos de acceso

### Error: "Authentication failed"
- Usar token de acceso personal en lugar de contraseña
- Configurar SSH keys para autenticación automática

### Conflictos de Merge
```bash
# Ver archivos en conflicto
git status

# Editar archivos manualmente para resolver conflictos
# Buscar marcadores: <<<<<<< ======= >>>>>>>

# Agregar archivos resueltos
git add archivo-resuelto.py

# Completar el merge
git commit
```

## 📞 Recursos Adicionales

- **GitHub Docs**: https://docs.github.com
- **Git Tutorial**: https://git-scm.com/docs/gittutorial
- **GitHub Desktop**: Interfaz gráfica para Git
- **VS Code**: Editor con integración Git excelente

---

**¡Listo!** Con estos pasos podrás trabajar en tu proyecto tanto desde el trabajo como desde casa, manteniendo todo sincronizado a través de GitHub.