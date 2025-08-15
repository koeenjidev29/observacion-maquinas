# -*- coding: utf-8 -*-
"""
Ventana de Login corporativa para COPY VALLS
Versión 0.1.4.0 - Sistema de autenticación
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.themes.corporate_colors import CorporateColors
from gui.login.help_dialog import HelpDialog
from version import get_version_string

class LoginWindow:
    """Ventana de login corporativa con validación de usuarios"""
    
    def __init__(self, on_login_success=None, on_exit=None):
        self.on_login_success = on_login_success
        self.on_exit = on_exit
        self.colors = CorporateColors()
        self.root = None
        self.username_var = None
        self.password_var = None
        
    def show(self):
        """Muestra la ventana de login"""
        self.root = tk.Tk()
        self.root.title("COPY VALLS - Acceso al Sistema")
        
        # Configuración de ventana
        window_width = 500
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=self.colors.BACKGROUND_PRIMARY)
        self.root.resizable(False, False)
        
        # Configurar estilos
        self.setup_styles()
        
        # Frame principal con borde
        main_frame = tk.Frame(
            self.root,
            bg=self.colors.BACKGROUND_PRIMARY,
            relief="raised",
            bd=3
        )
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header con branding
        self.create_header(main_frame)
        
        # Formulario de login
        self.create_login_form(main_frame)
        
        # Botones de acción
        self.create_action_buttons(main_frame)
        
        # Footer con versión
        self.create_footer(main_frame)
        
        # Configurar eventos
        self.setup_events()
        
        self.root.mainloop()
    
    def setup_styles(self):
        """Configura los estilos TTK corporativos"""
        style = ttk.Style()
        
        # Estilo para Entry
        style.configure(
            "Corporate.TEntry",
            fieldbackground=self.colors.SURFACE_LIGHT,
            borderwidth=2,
            relief="solid",
            bordercolor=self.colors.BORDER_MEDIUM,
            focuscolor=self.colors.CORPORATE_GOLD,
            font=("Arial", 11)
        )
        
        # Estilo para botón principal (Entrar)
        style.configure(
            "Corporate.Primary.TButton",
            background=self.colors.BUTTON_PRIMARY,
            foreground=self.colors.TEXT_ON_GOLD,
            borderwidth=2,
            relief="raised",
            font=("Arial", 11, "bold"),
            padding=(20, 8)
        )
        
        style.map(
            "Corporate.Primary.TButton",
            background=[("active", self.colors.BUTTON_PRIMARY_HOVER),
                       ("pressed", self.colors.CORPORATE_DARK_GOLD)]
        )
        
        # Estilo para botón secundario (Salir)
        style.configure(
            "Corporate.Secondary.TButton",
            background=self.colors.BUTTON_SECONDARY,
            foreground=self.colors.TEXT_ON_GOLD,
            borderwidth=2,
            relief="raised",
            font=("Arial", 10),
            padding=(15, 6)
        )
        
        style.map(
            "Corporate.Secondary.TButton",
            background=[("active", self.colors.BUTTON_SECONDARY_HOVER),
                       ("pressed", self.colors.SURFACE_DARK)]
        )
        
        # Estilo para botón de ayuda (destacado)
        style.configure(
            "Corporate.Help.TButton",
            background=self.colors.BUTTON_HELP,
            foreground=self.colors.TEXT_PRIMARY,
            borderwidth=3,
            relief="raised",
            font=("Arial", 10, "bold"),
            padding=(15, 6)
        )
        
        style.map(
            "Corporate.Help.TButton",
            background=[("active", self.colors.BUTTON_HELP_HOVER),
                       ("pressed", self.colors.CORPORATE_GOLD)]
        )
    
    def create_header(self, parent):
        """Crea el header con branding"""
        header_frame = tk.Frame(parent, bg=self.colors.BACKGROUND_PRIMARY)
        header_frame.pack(fill="x", pady=(0, 30))
        
        # COPY VALLS
        company_label = tk.Label(
            header_frame,
            text="COPY VALLS",
            font=("Arial", 24, "bold"),
            fg=self.colors.TEXT_ON_GOLD,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        company_label.pack()
        
        # MANTENIMIENTO DE MÁQUINAS
        subtitle_label = tk.Label(
            header_frame,
            text="MANTENIMIENTO DE MÁQUINAS",
            font=("Arial", 12),
            fg=self.colors.TEXT_SECONDARY,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_login_form(self, parent):
        """Crea el formulario de login"""
        # Frame del formulario con fondo diferenciado
        form_frame = tk.Frame(
            parent,
            bg=self.colors.BACKGROUND_SECONDARY,
            relief="sunken",
            bd=2
        )
        form_frame.pack(fill="x", pady=(0, 20), padx=20, ipady=20)
        
        # Título del formulario
        login_title = tk.Label(
            form_frame,
            text="login",
            font=("Arial", 14, "bold"),
            fg=self.colors.TEXT_PRIMARY,
            bg=self.colors.BACKGROUND_SECONDARY
        )
        login_title.pack(pady=(0, 15))
        
        # Campo Usuario
        tk.Label(
            form_frame,
            text="usuario",
            font=("Arial", 11),
            fg=self.colors.TEXT_PRIMARY,
            bg=self.colors.BACKGROUND_SECONDARY
        ).pack(anchor="w", padx=40, pady=(0, 5))
        
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            form_frame,
            textvariable=self.username_var,
            style="Corporate.TEntry",
            width=30
        )
        self.username_entry.pack(padx=40, pady=(0, 15))
        
        # Campo Contraseña
        tk.Label(
            form_frame,
            text="contraseña",
            font=("Arial", 11),
            fg=self.colors.TEXT_PRIMARY,
            bg=self.colors.BACKGROUND_SECONDARY
        ).pack(anchor="w", padx=40, pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            form_frame,
            textvariable=self.password_var,
            style="Corporate.TEntry",
            show="*",
            width=30
        )
        self.password_entry.pack(padx=40, pady=(0, 10))
    
    def create_action_buttons(self, parent):
        """Crea los botones de acción"""
        buttons_frame = tk.Frame(parent, bg=self.colors.BACKGROUND_PRIMARY)
        buttons_frame.pack(fill="x", pady=(0, 20))
        
        # Frame para botones principales
        main_buttons_frame = tk.Frame(buttons_frame, bg=self.colors.BACKGROUND_PRIMARY)
        main_buttons_frame.pack()
        
        # Botón Entrar
        self.login_button = ttk.Button(
            main_buttons_frame,
            text="entrar",
            style="Corporate.Primary.TButton",
            command=self.handle_login
        )
        self.login_button.pack(side="left", padx=(0, 15))
        
        # Botón Salir
        self.exit_button = ttk.Button(
            main_buttons_frame,
            text="salir",
            style="Corporate.Secondary.TButton",
            command=self.handle_exit
        )
        self.exit_button.pack(side="left", padx=(15, 0))
        
        # Botón Ayuda (destacado y separado)
        help_frame = tk.Frame(buttons_frame, bg=self.colors.BACKGROUND_PRIMARY)
        help_frame.pack(pady=(15, 0))
        
        self.help_button = ttk.Button(
            help_frame,
            text="ayuda",
            style="Corporate.Help.TButton",
            command=self.show_help
        )
        self.help_button.pack()
    
    def create_footer(self, parent):
        """Crea el footer con información de versión"""
        footer_frame = tk.Frame(parent, bg=self.colors.BACKGROUND_PRIMARY)
        footer_frame.pack(side="bottom", fill="x")
        
        version_label = tk.Label(
            footer_frame,
            text=f"versión {get_version_string()}",
            font=("Arial", 9),
            fg=self.colors.TEXT_MUTED,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        version_label.pack(side="right")
    
    def setup_events(self):
        """Configura eventos de teclado"""
        # Enter para hacer login
        self.root.bind('<Return>', lambda e: self.handle_login())
        # Escape para salir
        self.root.bind('<Escape>', lambda e: self.handle_exit())
        # F1 para ayuda
        self.root.bind('<F1>', lambda e: self.show_help())
        
        # Focus inicial en username
        self.username_entry.focus_set()
    
    def handle_login(self):
        """Maneja el proceso de login"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning(
                "Campos Requeridos",
                "Por favor, ingrese usuario y contraseña."
            )
            return
        
        # Aquí iría la validación real de usuarios
        # Por ahora, validación simple
        if self.validate_user(username, password):
            if self.on_login_success:
                self.root.destroy()
                self.on_login_success(username)
        else:
            messagebox.showerror(
                "Error de Acceso",
                "Usuario o contraseña incorrectos."
            )
            self.password_var.set("")  # Limpiar contraseña
            self.password_entry.focus_set()
    
    def validate_user(self, username, password):
        """Valida las credenciales del usuario"""
        # Validación temporal - aquí se conectaría con la base de datos
        valid_users = {
            "admin": "admin123",
            "operador": "op123",
            "supervisor": "sup123"
        }
        
        return username in valid_users and valid_users[username] == password
    
    def handle_exit(self):
        """Maneja la salida de la aplicación"""
        if messagebox.askyesno(
            "Confirmar Salida",
            "¿Está seguro que desea salir del sistema?"
        ):
            if self.on_exit:
                self.on_exit()
            else:
                self.root.quit()
    
    def show_help(self):
        """Muestra la ventana de ayuda"""
        help_dialog = HelpDialog(self.root)
        help_dialog.show()