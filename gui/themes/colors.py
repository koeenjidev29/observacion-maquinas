# -*- coding: utf-8 -*-
"""
Paleta de Colores Corporativa
Versión 1.3.8.2 - Sistema de Temas Profesional
"""

class ColorPalette:
    """Paleta de colores corporativa para el tema moderno"""
    
    # 🎨 Colores Primarios
    PRIMARY = "#2c3e50"          # Azul oscuro profesional
    PRIMARY_LIGHT = "#34495e"    # Azul oscuro claro
    PRIMARY_DARK = "#1a252f"     # Azul muy oscuro
    
    # 🎨 Colores Secundarios
    SECONDARY = "#3498db"        # Azul claro
    SECONDARY_LIGHT = "#5dade2"  # Azul claro suave
    SECONDARY_DARK = "#2980b9"   # Azul medio
    
    # 🎨 Colores de Estado
    SUCCESS = "#27ae60"          # Verde éxito
    SUCCESS_LIGHT = "#58d68d"    # Verde claro
    WARNING = "#f39c12"          # Naranja advertencia
    WARNING_LIGHT = "#f8c471"    # Naranja claro
    ERROR = "#e74c3c"            # Rojo error
    ERROR_LIGHT = "#ec7063"      # Rojo claro
    INFO = "#17a2b8"             # Azul información
    
    # 🎨 Colores de Fondo
    BACKGROUND = "#ecf0f1"       # Gris muy claro
    BACKGROUND_DARK = "#bdc3c7"  # Gris medio
    SURFACE = "#ffffff"          # Blanco
    SURFACE_VARIANT = "#f8f9fa"  # Gris casi blanco
    
    # 🎨 Colores de Texto
    TEXT_PRIMARY = "#2c3e50"     # Texto principal
    TEXT_SECONDARY = "#7f8c8d"   # Texto secundario
    TEXT_DISABLED = "#95a5a6"    # Texto deshabilitado
    TEXT_ON_PRIMARY = "#ffffff"  # Texto sobre primario
    
    # 🎨 Colores de Bordes
    BORDER = "#dee2e6"           # Borde normal
    BORDER_LIGHT = "#e9ecef"     # Borde claro
    BORDER_FOCUS = "#3498db"     # Borde con foco
    
    # 🎨 Colores de Sombra
    SHADOW_LIGHT = "rgba(44, 62, 80, 0.1)"   # Sombra suave
    SHADOW_MEDIUM = "rgba(44, 62, 80, 0.2)"  # Sombra media
    SHADOW_STRONG = "rgba(44, 62, 80, 0.3)"  # Sombra fuerte
    
    # 🎨 Colores por Rol de Usuario
    ROLE_ADMIN = "#fff3cd"       # Amarillo suave admin
    ROLE_ADMIN_BORDER = "#ffeaa7" # Borde admin
    ROLE_MECANICO = "#d1ecf1"    # Azul suave mecánico
    ROLE_MECANICO_BORDER = "#bee5eb" # Borde mecánico
    ROLE_USUARIO = "#d4edda"     # Verde suave usuario
    ROLE_USUARIO_BORDER = "#c3e6cb" # Borde usuario
    
    # 🎨 Gradientes
    GRADIENT_PRIMARY = "linear-gradient(135deg, #2c3e50 0%, #34495e 100%)"
    GRADIENT_SECONDARY = "linear-gradient(135deg, #3498db 0%, #5dade2 100%)"
    GRADIENT_SUCCESS = "linear-gradient(135deg, #27ae60 0%, #58d68d 100%)"
    
    @classmethod
    def get_role_colors(cls, role):
        """Obtiene colores específicos para un rol de usuario"""
        role_colors = {
            'admin': {
                'background': cls.ROLE_ADMIN,
                'border': cls.ROLE_ADMIN_BORDER,
                'text': '#856404',
                'icon': '👑'
            },
            'mecanico': {
                'background': cls.ROLE_MECANICO,
                'border': cls.ROLE_MECANICO_BORDER,
                'text': '#0c5460',
                'icon': '🔧'
            },
            'usuario': {
                'background': cls.ROLE_USUARIO,
                'border': cls.ROLE_USUARIO_BORDER,
                'text': '#155724',
                'icon': '👤'
            }
        }
        return role_colors.get(role, role_colors['usuario'])


# 🏢 Colores empresariales (menos mate, más profesional)
BACKGROUND_ENTERPRISE = '#f8f9fa'  # Gris muy claro
PRIMARY_ENTERPRISE = '#0d47a1'     # Azul corporativo
PRIMARY_ENTERPRISE_LIGHT = '#1565c0'
PRIMARY_ENTERPRISE_DARK = '#01579b'
SECONDARY_ENTERPRISE = '#37474f'   # Gris azulado
ACCENT_ENTERPRISE = '#ff6f00'      # Naranja corporativo
SUCCESS_ENTERPRISE = '#2e7d32'     # Verde corporativo
WARNING_ENTERPRISE = '#f57c00'     # Ámbar corporativo
ERROR_ENTERPRISE = '#c62828'       # Rojo corporativo
TEXT_ENTERPRISE = '#212121'        # Texto principal
TEXT_ENTERPRISE_SECONDARY = '#757575'  # Texto secundario
BORDER_ENTERPRISE = '#e0e0e0'      # Bordes suaves
SHADOW_ENTERPRISE = 'rgba(0,0,0,0.1)'  # Sombras suaves