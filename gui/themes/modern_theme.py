# -*- coding: utf-8 -*-
"""
Tema Moderno Profesional
Versión 1.3.8.2 - Sistema de Temas Completo
"""

import tkinter as tk
from tkinter import ttk
from .colors import ColorPalette

class ModernTheme:
    """Tema moderno y profesional para la aplicación"""
    
    def __init__(self, style):
        self.style = style
        self.colors = ColorPalette()
        self.setup_theme()
    
    def setup_theme(self):
        """Configura todos los estilos del tema moderno"""
        self.configure_window_styles()
        self.configure_button_styles()
        self.configure_entry_styles()
        self.configure_frame_styles()
        self.configure_label_styles()
        self.configure_treeview_styles()
        self.configure_combobox_styles()
        self.configure_scrollbar_styles()
    
    def configure_window_styles(self):
        """Configura estilos para ventanas principales"""
        # Configuración base del tema
        self.style.theme_use('clam')
        
        # Configurar colores base
        self.style.configure('.',
            background=self.colors.BACKGROUND,
            foreground=self.colors.TEXT_PRIMARY,
            selectbackground=self.colors.SECONDARY,
            selectforeground=self.colors.TEXT_ON_PRIMARY
        )
    
    def configure_button_styles(self):
        """Configura estilos modernos para botones"""
        
        # 🔵 Botón Primario
        self.style.configure("Modern.Primary.TButton",
            background=self.colors.PRIMARY,
            foreground=self.colors.TEXT_ON_PRIMARY,
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 10),
            relief="flat",
            borderwidth=0
        )
        
        self.style.map("Modern.Primary.TButton",
            background=[('active', self.colors.PRIMARY_LIGHT),
                       ('pressed', self.colors.PRIMARY_DARK)],
            relief=[('pressed', 'sunken'),
                   ('!pressed', 'flat')]
        )
        
        # 🔵 Botón Secundario
        self.style.configure("Modern.Secondary.TButton",
            background=self.colors.SECONDARY,
            foreground=self.colors.TEXT_ON_PRIMARY,
            font=('Segoe UI', 10),
            padding=(15, 8),
            relief="flat",
            borderwidth=0
        )
        
        self.style.map("Modern.Secondary.TButton",
            background=[('active', self.colors.SECONDARY_LIGHT),
                       ('pressed', self.colors.SECONDARY_DARK)]
        )
        
        # ✅ Botón de Éxito
        self.style.configure("Modern.Success.TButton",
            background=self.colors.SUCCESS,
            foreground=self.colors.TEXT_ON_PRIMARY,
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 8),
            relief="flat"
        )
        
        self.style.map("Modern.Success.TButton",
            background=[('active', self.colors.SUCCESS_LIGHT)]
        )
        
        # ⚠️ Botón de Advertencia
        self.style.configure("Modern.Warning.TButton",
            background=self.colors.WARNING,
            foreground=self.colors.TEXT_ON_PRIMARY,
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 8),
            relief="flat"
        )
        
        # ❌ Botón de Error
        self.style.configure("Modern.Error.TButton",
            background=self.colors.ERROR,
            foreground=self.colors.TEXT_ON_PRIMARY,
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 8),
            relief="flat"
        )
        
        # 🎨 Estilo para botón de perfil (MOVIDO AQUÍ)
        self.style.configure('Modern.Profile.TButton',
                        background=self.colors.SECONDARY,
                        foreground=self.colors.TEXT_PRIMARY,
                        borderwidth=1,
                        relief='flat',
                        padding=(15, 8),
                        font=('Segoe UI', 10, 'bold'))
        
        self.style.map('Modern.Profile.TButton',
                  background=[('active', self.colors.PRIMARY_LIGHT),
                             ('pressed', self.colors.PRIMARY_DARK)],
                  foreground=[('active', self.colors.TEXT_PRIMARY)],
                  relief=[('pressed', 'sunken')])
    
    def configure_entry_styles(self):
        """Configura estilos modernos para campos de entrada"""
        
        self.style.configure("Modern.TEntry",
            fieldbackground=self.colors.SURFACE,
            background=self.colors.SURFACE,
            foreground=self.colors.TEXT_PRIMARY,
            borderwidth=2,
            relief="solid",
            insertcolor=self.colors.PRIMARY,
            font=('Segoe UI', 10),
            padding=(10, 8)
        )
        
        self.style.map("Modern.TEntry",
            bordercolor=[('focus', self.colors.BORDER_FOCUS),
                        ('!focus', self.colors.BORDER)],
            lightcolor=[('focus', self.colors.BORDER_FOCUS)],
            darkcolor=[('focus', self.colors.BORDER_FOCUS)]
        )
    
    def configure_frame_styles(self):
        """Configura estilos para frames y contenedores"""
        
        # Frame principal
        self.style.configure("Modern.TFrame",
            background=self.colors.BACKGROUND,
            relief="flat",
            borderwidth=0
        )
        
        # Frame de superficie (cards)
        self.style.configure("Modern.Card.TFrame",
            background=self.colors.SURFACE,
            relief="solid",
            borderwidth=1,
            bordercolor=self.colors.BORDER_LIGHT
        )
        
        # LabelFrame moderno
        self.style.configure("Modern.TLabelframe",
            background=self.colors.SURFACE,
            foreground=self.colors.TEXT_PRIMARY,
            borderwidth=2,
            relief="solid",
            bordercolor=self.colors.BORDER,
            font=('Segoe UI', 11, 'bold')
        )
        
        self.style.configure("Modern.TLabelframe.Label",
            background=self.colors.SURFACE,
            foreground=self.colors.PRIMARY,
            font=('Segoe UI', 11, 'bold')
        )
    
    def configure_label_styles(self):
        """Configura estilos para etiquetas"""
        
        # Etiqueta principal
        self.style.configure("Modern.TLabel",
            background=self.colors.BACKGROUND,
            foreground=self.colors.TEXT_PRIMARY,
            font=('Segoe UI', 10)
        )
        
        # Etiqueta de título
        self.style.configure("Modern.Title.TLabel",
            background=self.colors.BACKGROUND,
            foreground=self.colors.PRIMARY,
            font=('Segoe UI', 14, 'bold')
        )
        
        # Etiqueta de subtítulo
        self.style.configure("Modern.Subtitle.TLabel",
            background=self.colors.BACKGROUND,
            foreground=self.colors.TEXT_SECONDARY,
            font=('Segoe UI', 11)
        )
    
    def configure_treeview_styles(self):
        """Configura estilos para Treeview (ya implementado en v1.3.8.1)"""
        # Los estilos de Treeview ya están implementados en la versión anterior
        pass
    
    def configure_combobox_styles(self):
        """Configura estilos para Combobox"""
        
        self.style.configure("Modern.TCombobox",
            fieldbackground=self.colors.SURFACE,
            background=self.colors.SURFACE,
            foreground=self.colors.TEXT_PRIMARY,
            borderwidth=2,
            relief="solid",
            font=('Segoe UI', 10),
            padding=(10, 8)
        )
        
        self.style.map("Modern.TCombobox",
            bordercolor=[('focus', self.colors.BORDER_FOCUS),
                        ('!focus', self.colors.BORDER)]
        )
    
    def configure_scrollbar_styles(self):
        """Configura estilos para scrollbars"""
        
        self.style.configure("Modern.Vertical.TScrollbar",
            background=self.colors.BACKGROUND_DARK,
            troughcolor=self.colors.BACKGROUND,
            borderwidth=0,
            arrowcolor=self.colors.TEXT_SECONDARY,
            darkcolor=self.colors.BACKGROUND_DARK,
            lightcolor=self.colors.BACKGROUND_DARK
        )
        
        self.style.map("Modern.Vertical.TScrollbar",
            background=[('active', self.colors.SECONDARY_LIGHT)]
        )

    def configure_enterprise_styles(self):
        """Configura estilos empresariales para login"""
        
        # Header empresarial
        self.style.configure('Enterprise.Header.TFrame',
                        background=self.colors.PRIMARY_ENTERPRISE,
                        relief='flat')
        
        # Logo empresarial
        self.style.configure('Enterprise.Logo.TLabel',
                        background=self.colors.PRIMARY_ENTERPRISE,
                        foreground='white',
                        font=('Segoe UI', 16, 'bold'))
        
        # Botón principal empresarial
        self.style.configure('Enterprise.Primary.TButton',
                        background=self.colors.PRIMARY_ENTERPRISE,
                        foreground='white',
                        font=('Segoe UI', 11, 'bold'),
                        relief='flat',
                        borderwidth=0)
        
        self.style.map('Enterprise.Primary.TButton',
                      background=[('active', self.colors.PRIMARY_ENTERPRISE_LIGHT),
                                 ('pressed', self.colors.PRIMARY_ENTERPRISE_DARK)])