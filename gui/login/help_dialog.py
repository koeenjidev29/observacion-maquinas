# -*- coding: utf-8 -*-
"""
Ventana de ayuda para el sistema COPY VALLS
Versión 0.1.4.0 - Información de contacto y soporte
"""

import tkinter as tk
from tkinter import ttk
from gui.themes.corporate_colors import CorporateColors

class HelpDialog:
    """Ventana de ayuda con información de contacto"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.colors = CorporateColors()
        self.dialog = None
    
    def show(self):
        """Muestra la ventana de ayuda"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("COPY VALLS - Ayuda y Soporte")
        
        # Configuración de ventana
        window_width = 450
        window_height = 350
        
        if self.parent:
            parent_x = self.parent.winfo_rootx()
            parent_y = self.parent.winfo_rooty()
            parent_width = self.parent.winfo_width()
            parent_height = self.parent.winfo_height()
            
            x = parent_x + (parent_width - window_width) // 2
            y = parent_y + (parent_height - window_height) // 2
        else:
            screen_width = self.dialog.winfo_screenwidth()
            screen_height = self.dialog.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
        
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.dialog.configure(bg=self.colors.BACKGROUND_SECONDARY)
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(
            self.dialog,
            bg=self.colors.BACKGROUND_SECONDARY,
            relief="raised",
            bd=2
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Información de contacto
        self.create_contact_info(main_frame)
        
        # Botón cerrar
        self.create_close_button(main_frame)
        
        # Centrar y mostrar
        self.dialog.focus_set()
    
    def create_header(self, parent):
        """Crea el header de la ventana de ayuda"""
        header_frame = tk.Frame(parent, bg=self.colors.BACKGROUND_SECONDARY)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="🛠️ SOPORTE TÉCNICO",
            font=("Arial", 18, "bold"),
            fg=self.colors.CORPORATE_GOLD,
            bg=self.colors.BACKGROUND_SECONDARY
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="COPY VALLS - Mantenimiento de Máquinas",
            font=("Arial", 11),
            fg=self.colors.TEXT_SECONDARY,
            bg=self.colors.BACKGROUND_SECONDARY
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_contact_info(self, parent):
        """Crea la sección de información de contacto"""
        # Frame de contacto con borde
        contact_frame = tk.Frame(
            parent,
            bg=self.colors.SURFACE_LIGHT,
            relief="sunken",
            bd=2
        )
        contact_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título de contacto
        contact_title = tk.Label(
            contact_frame,
            text="Para soporte técnico, contacte con:",
            font=("Arial", 12, "bold"),
            fg=self.colors.TEXT_PRIMARY,
            bg=self.colors.SURFACE_LIGHT
        )
        contact_title.pack(pady=(15, 20))
        
        # Información de contacto
        contact_info = [
            ("📞 Teléfono:", "+34 XXX XXX XXX"),
            ("📧 Email:", "soporte@copyvalls.com"),
            ("🌐 Web:", "www.copyvalls.com"),
            ("⏰ Horario:", "Lunes a Viernes: 8:00 - 18:00")
        ]
        
        for label, value in contact_info:
            info_frame = tk.Frame(contact_frame, bg=self.colors.SURFACE_LIGHT)
            info_frame.pack(fill="x", padx=30, pady=5)
            
            # Etiqueta
            tk.Label(
                info_frame,
                text=label,
                font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_SECONDARY,
                bg=self.colors.SURFACE_LIGHT,
                width=12,
                anchor="w"
            ).pack(side="left")
            
            # Valor
            tk.Label(
                info_frame,
                text=value,
                font=("Arial", 10),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT,
                anchor="w"
            ).pack(side="left", padx=(10, 0))
        
        # Nota adicional
        note_label = tk.Label(
            contact_frame,
            text="💡 Tip: Presione F1 en cualquier momento para acceder a esta ayuda",
            font=("Arial", 9, "italic"),
            fg=self.colors.TEXT_MUTED,
            bg=self.colors.SURFACE_LIGHT,
            wraplength=350
        )
        note_label.pack(pady=(20, 15))
    
    def create_close_button(self, parent):
        """Crea el botón de cerrar"""
        button_frame = tk.Frame(parent, bg=self.colors.BACKGROUND_SECONDARY)
        button_frame.pack(fill="x")
        
        # Configurar estilo del botón
        style = ttk.Style()
        style.configure(
            "Help.Close.TButton",
            background=self.colors.BUTTON_SECONDARY,
            foreground=self.colors.TEXT_ON_GOLD,
            font=("Arial", 10),
            padding=(20, 8)
        )
        
        close_button = ttk.Button(
            button_frame,
            text="Cerrar",
            style="Help.Close.TButton",
            command=self.close_dialog
        )
        close_button.pack()
        
        # Configurar eventos
        self.dialog.bind('<Escape>', lambda e: self.close_dialog())
        self.dialog.bind('<Return>', lambda e: self.close_dialog())
    
    def close_dialog(self):
        """Cierra la ventana de ayuda"""
        if self.dialog:
            self.dialog.destroy()