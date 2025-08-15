import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, date
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from excel.excel_manager import ExcelManager
from gui.themes.corporate_colors import CorporateColors
from utils.helpers import (
    get_default_machines, get_lines_list, get_machines_by_line,
    validate_observation, validate_machine,
    get_today_date, format_date_for_display, get_current_user,
    get_filter_options, calculate_date_range, filter_dates_in_range, get_date_range_description
)
from version import get_full_version_string, get_version_string

# -*- coding: utf-8 -*-
"""
Ventana principal del sistema COPY VALLS
Versión 0.1.4.0 - Integración con sistema de login corporativo
"""

class MainWindow:
    """Ventana principal del sistema con soporte para usuarios y roles"""
    
    def __init__(self, user_name=None, user_role=None):
        self.user_name = user_name or "Usuario"
        self.user_role = user_role or "operador"
        self.colors = CorporateColors()
        self.root = None
        self.logout_callback = None
        
        # ✅ Agregar variables faltantes
        self.excel_manager = ExcelManager()
        self.lines = get_lines_list()
        self.machines = get_default_machines()
        
        # ✅ Definir permisos por rol
        self.user_permissions = {
            'admin': {'can_add': True, 'can_edit': True, 'can_delete': True, 'can_edit_datetime': True},  # ✅ Agregado
            'administrador': {'can_add': True, 'can_edit': True, 'can_delete': True, 'can_edit_datetime': True},
            'supervisor': {'can_add': True, 'can_edit': True, 'can_delete': False, 'can_edit_datetime': True},
            'operador': {'can_add': True, 'can_edit': False, 'can_delete': False, 'can_edit_datetime': False},
            'operator': {'can_add': True, 'can_edit': False, 'can_delete': False, 'can_edit_datetime': False},  # ✅ Agregado
            'tecnico': {'can_add': True, 'can_edit': True, 'can_delete': False, 'can_edit_datetime': False},
            'invitado': {'can_add': False, 'can_edit': False, 'can_delete': False, 'can_edit_datetime': False}
        }
    
    def set_logout_callback(self, callback):
        """Establece el callback para logout"""
        self.logout_callback = callback
    
    def show(self):
        """Muestra la ventana principal"""
        print("🚀 [DEBUG] Iniciando MainWindow.show()")
        print(f"🚀 [DEBUG] Usuario: {self.user_name}, Rol: {self.user_role}")
        
        self.root = tk.Tk()
        self.root.title(f"COPY VALLS - Sistema de Mantenimiento - {self.user_name}")
        
        # Configuración de ventana
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors.BACKGROUND_SECONDARY)
        self.root.state('zoomed')  # Maximizada en Windows
        
        print("🚀 [DEBUG] Ventana configurada, creando interfaz...")
        
        # Crear interfaz
        self.create_interface()
        
        print("🚀 [DEBUG] Interfaz creada, mostrando mensaje de bienvenida...")
        
        # Mostrar mensaje de bienvenida
        self.show_welcome_message()
        
        print("🚀 [DEBUG] Iniciando mainloop...")
        self.root.mainloop()
    
    def create_interface(self):
        """Crea la interfaz principal"""
        print("🔧 [DEBUG] Creando header...")
        # Header corporativo
        self.create_header()
        
        print("🔧 [DEBUG] Creando barra de usuario...")
        # Barra de usuario
        self.create_user_bar()
        
        print("🔧 [DEBUG] Creando contenido principal...")
        # Contenido principal (placeholder por ahora)
        self.create_main_content()
        
        print("🔧 [DEBUG] Creando footer...")
        # Footer
        self.create_footer()
        
        # ✅ AGREGAR ESTA LÍNEA:
        print("🔧 [DEBUG] Creando menú...")
        # Crear menú de la aplicación
        self.setup_menu()
        
        print("🔧 [DEBUG] Interfaz completamente creada")
    
    def create_header(self):
        """Crea el header corporativo"""
        header_frame = tk.Frame(
            self.root,
            bg=self.colors.CORPORATE_GOLD,
            height=80
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header_frame, bg=self.colors.CORPORATE_GOLD)
        title_frame.pack(expand=True, fill="both")
        
        company_label = tk.Label(
            title_frame,
            text="COPY VALLS - MANTENIMIENTO DE MÁQUINAS",
            font=("Arial", 20, "bold"),
            fg=self.colors.TEXT_ON_GOLD,
            bg=self.colors.CORPORATE_GOLD
        )
        company_label.pack(expand=True)
    
    def create_user_bar(self):
        """Crea la barra de información del usuario"""
        user_frame = tk.Frame(
            self.root,
            bg=self.colors.BACKGROUND_PRIMARY,
            height=50
        )
        user_frame.pack(fill="x")
        user_frame.pack_propagate(False)
        
        # Información del usuario (izquierda)
        user_info_frame = tk.Frame(user_frame, bg=self.colors.BACKGROUND_PRIMARY)
        user_info_frame.pack(side="left", padx=20, pady=10)
        
        user_label = tk.Label(
            user_info_frame,
            text=f"👤 {self.user_name} ({self.user_role.title()})",
            font=("Arial", 12, "bold"),
            fg=self.colors.TEXT_ON_GOLD,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        user_label.pack(side="left")
        
        # Botones de acción (derecha)
        actions_frame = tk.Frame(user_frame, bg=self.colors.BACKGROUND_PRIMARY)
        actions_frame.pack(side="right", padx=20, pady=10)
        
        # Configurar estilos
        style = ttk.Style()
        style.configure(
            "UserBar.TButton",
            background=self.colors.BUTTON_SECONDARY,
            foreground=self.colors.TEXT_ON_GOLD,
            font=("Arial", 9),
            padding=(10, 5)
        )
        
        # Botón de configuración (solo para admin/supervisor)
        if self.user_role in ["administrador", "supervisor"]:
            config_button = ttk.Button(
                actions_frame,
                text="⚙️ Config",
                style="UserBar.TButton",
                command=self.show_config
            )
            config_button.pack(side="right", padx=(0, 10))
        
        # Botón de logout
        logout_button = ttk.Button(
            actions_frame,
            text="🚪 Salir",
            style="UserBar.TButton",
            command=self.handle_logout
        )
        logout_button.pack(side="right")
    
    def create_main_content(self):
        """Crea el contenido principal con mejor visibilidad"""
        print("📋 [DEBUG] Iniciando create_main_content()")
        
        # Frame principal con fondo más visible
        main_frame = tk.Frame(
            self.root,
            bg="white",  # ✅ Fondo blanco para mejor contraste
            relief="raised",
            bd=2
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        print("📋 [DEBUG] main_frame creado y empaquetado")
        
        # Panel de control superior
        control_panel = tk.Frame(main_frame, bg="white")
        control_panel.pack(fill="x", pady=(10, 20))
        
        # Título principal más visible
        title_label = tk.Label(
            control_panel,
            text=f"🏭 SISTEMA DE OBSERVACIÓN DE MÁQUINAS",
            font=("Arial", 18, "bold"),
            fg="#1a365d",  # Azul oscuro
            bg="white"
        )
        title_label.pack(pady=(0, 10))
        
        # Información del usuario
        user_info_label = tk.Label(
            control_panel,
            text=f"👤 Usuario: {self.user_name} | 🔑 Rol: {self.user_role.title()}",
            font=("Arial", 12, "bold"),
            fg="#2d3748",  # Gris oscuro
            bg="white"
        )
        user_info_label.pack(pady=(0, 20))
        
        # Botones de acción con colores visibles
        buttons_frame = tk.Frame(control_panel, bg="white")
        buttons_frame.pack(fill="x", pady=(0, 20))
        
        if self.user_permissions[self.user_role]['can_add']:
            new_obs_btn = tk.Button(
                buttons_frame,
                text="➕ Nueva Observación",
                command=self.show_new_incident_dialog,
                bg="#48bb78",  # Verde
                fg="white",
                font=("Arial", 11, "bold"),
                padx=20, pady=10,
                relief="raised",
                bd=2
            )
            new_obs_btn.pack(side="left", padx=(0, 15))
        
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Actualizar Observaciones",
            command=self.load_today_observations,
            bg="#4299e1",  # Azul
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20, pady=10,
            relief="raised",
            bd=2
        )
        refresh_btn.pack(side="left", padx=(0, 15))
        
        config_btn = tk.Button(
            buttons_frame,
            text="⚙️ Configuración",
            command=self.show_config,
            bg="#ed8936",  # Naranja
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20, pady=10,
            relief="raised",
            bd=2
        )
        config_btn.pack(side="left")
        
        # Área de observaciones con marco visible
        obs_frame = tk.LabelFrame(
            main_frame,
            text="📋 Observaciones de Hoy",
            bg="white",
            fg="#1a365d",
            font=("Arial", 14, "bold"),
            relief="groove",
            bd=3
        )
        obs_frame.pack(fill="both", expand=True, pady=(10, 20))
        
        # Lista de observaciones
        list_frame = tk.Frame(obs_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.observations_listbox = tk.Listbox(
            list_frame,
            bg="#f7fafc",  # Gris muy claro
            fg="#2d3748",  # Gris oscuro
            font=("Arial", 10),
            selectmode=tk.SINGLE,
            relief="sunken",
            bd=2,
            selectbackground="#4299e1",
            selectforeground="white"
        )
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.config(command=self.observations_listbox.yview)
        self.observations_listbox.config(yscrollcommand=scrollbar.set)
        
        self.observations_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar observaciones
        self.load_today_observations()
        
        # Panel de estado
        status_frame = tk.Frame(main_frame, bg="#edf2f7", relief="sunken", bd=1)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Sistema listo - Interfaz cargada correctamente",
            font=("Arial", 10),
            fg="#2d3748",
            bg="#edf2f7"
        )
        self.status_label.pack(pady=8)
        
        print("📋 [DEBUG] create_main_content() COMPLETADO con interfaz visible")
    
    def create_footer(self):
        """Crea el footer con información de versión"""
        footer_frame = tk.Frame(
            self.root,
            bg=self.colors.SURFACE_DARK,
            height=30
        )
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        version_label = tk.Label(
            footer_frame,
            text=f"COPY VALLS v{get_version_string()} - Sistema de Mantenimiento de Máquinas",
            font=("Arial", 9),
            fg=self.colors.TEXT_ON_GOLD,
            bg=self.colors.SURFACE_DARK
        )
        version_label.pack(expand=True)
    
    def get_role_info(self):
        """Obtiene información específica del rol del usuario"""
        role_descriptions = {
            "administrador": "Como Administrador, tienes acceso completo al sistema. Puedes gestionar usuarios, configurar el sistema y acceder a todas las funcionalidades.",
            "supervisor": "Como Supervisor, puedes supervisar las operaciones, generar reportes y gestionar el mantenimiento de máquinas.",
            "operador": "Como Operador, puedes registrar observaciones, consultar el estado de las máquinas y generar reportes básicos.",
            "tecnico": "Como Técnico, puedes acceder a la información técnica de las máquinas y registrar actividades de mantenimiento.",
            "invitado": "Como Invitado, tienes acceso limitado de solo lectura al sistema."
        }
        
        return role_descriptions.get(self.user_role, "Usuario del sistema de mantenimiento.")
    
    def show_welcome_message(self):
        """Muestra mensaje de bienvenida"""
        messagebox.showinfo(
            "¡Bienvenido!",
            f"Bienvenido al sistema COPY VALLS, {self.user_name}.\n\n"
            f"Rol: {self.user_role.title()}\n"
            f"Versión: {get_version_string()}\n\n"
            "El sistema está listo para usar."
        )
    
    def show_config(self):
        """Muestra ventana de configuración (placeholder)"""
        messagebox.showinfo(
            "Configuración",
            "Panel de configuración - Próximamente disponible"
        )
    
    def handle_logout(self):
        """Maneja el logout del usuario con confirmación"""
        result = messagebox.askyesno(
            "Confirmar Salida", 
            "¿Confirmas que quieres salir del usuario actual?\n\nEsto te devolverá a la ventana de login."
        )
        if result:
            if self.logout_callback:
                self.logout_callback()
            else:
                self.on_window_close()

    def logout(self):
        """Cierra sesión y vuelve al login"""
        result = messagebox.askyesno(
            "Cerrar Sesión", 
            "¿Confirmas que quieres salir del usuario actual?\n\nEsto te devolverá a la ventana de login."
        )
        if result:
            if self.logout_callback:
                self.logout_callback()
            else:
                # Cerrar ventana actual y volver al login
                self.root.destroy()
            
            # Crear nueva instancia para mostrar login
            new_app = MainWindow()
            if new_app.current_user:
                new_app.run()
    
    def on_window_close(self):
        """Maneja el cierre de la ventana con confirmación mejorada"""
        result = messagebox.askyesno(
            "Confirmar Salida",
            "¿Confirmas que quieres salir del programa?\n\nEsto cerrará completamente la aplicación."
        )
        if result:
            self.close()
    
    def close(self):
        """Cierra la ventana principal"""
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None

    def show_new_incident_dialog(self):
        """Muestra diálogo moderno para nueva incidencia"""
        # ✅ Cambiar self.current_user_role por self.user_role
        if not self.user_permissions[self.user_role]['can_add']:
            messagebox.showwarning("Sin permisos", "No tienes permisos para añadir incidencias")
            return
        
        dialog = tk.Toplevel(self.root)
        # ✅ Cambiar self.current_user por self.user_name
        dialog.title(f"Nueva Incidencia - {self.user_name} ({self.user_role})")
        dialog.geometry("550x650")
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 🎨 Aplicar tema moderno al diálogo
        dialog.configure(bg=self.colors.BACKGROUND_SECONDARY)
        
        # Centrar ventana
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 150, self.root.winfo_rooty() + 100))
        
        # Variables
        selected_date = tk.StringVar(value=get_today_date())
        selected_time = tk.StringVar(value=datetime.now().strftime("%H:%M:%S"))
        selected_line = tk.StringVar()
        selected_machine = tk.StringVar()
        
        # 🎨 Frame principal con estilo moderno
        main_frame = tk.Frame(dialog, bg=self.colors.SURFACE_LIGHT, padx=25, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 🎨 Título con estilo moderno
        title_text = f"➕ Nueva Incidencia - {self.user_name} ({self.user_role})"
        title_label = tk.Label(main_frame, text=title_text, 
                              font=("Arial", 16, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.SURFACE_LIGHT)
        title_label.pack(pady=(0, 25))
        
        # 🎨 Crear campos de formulario
        # Fecha
        tk.Label(main_frame, text="📅 Fecha:", 
                font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(15, 5))
        
        if self.user_permissions[self.user_role]['can_edit_datetime']:
            date_entry = DateEntry(main_frame, textvariable=selected_date, date_pattern='dd/mm/yyyy')
        else:
            date_entry = tk.Entry(main_frame, textvariable=selected_date, state='readonly')
        date_entry.pack(pady=(5, 10), fill=tk.X)
        
        # Hora
        tk.Label(main_frame, text="🕐 Hora:", 
                font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 5))
        
        if self.user_permissions[self.user_role]['can_edit_datetime']:
            time_entry = tk.Entry(main_frame, textvariable=selected_time)
        else:
            time_entry = tk.Entry(main_frame, textvariable=selected_time, state='readonly')
        time_entry.pack(pady=(5, 10), fill=tk.X)
        
        # Línea
        tk.Label(main_frame, text="🏭 Línea:", 
                font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 5))
        
        line_combo = ttk.Combobox(main_frame, textvariable=selected_line, 
                                 values=self.lines, state='readonly')
        line_combo.pack(pady=(5, 10), fill=tk.X)
        
        # Máquina
        tk.Label(main_frame, text="⚙️ Máquina:", 
                font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 5))
        
        machine_combo = ttk.Combobox(main_frame, textvariable=selected_machine, 
                                    values=self.machines, state='readonly')
        machine_combo.pack(pady=(5, 10), fill=tk.X)
        
        # 🎨 Campo de observación
        tk.Label(main_frame, text="📝 Observación:", 
                font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(15, 5))
        
        observation_text = scrolledtext.ScrolledText(main_frame, height=8, width=50,
                                                   font=('Arial', 10))
        observation_text.pack(pady=(5, 20), fill=tk.BOTH, expand=True)
        
        def save_incident():
            try:
                # Validar campos
                if not selected_line.get() or not selected_machine.get():
                    messagebox.showerror("Error", "Debe seleccionar línea y máquina")
                    return
                
                observation = observation_text.get(1.0, tk.END).strip()
                if not observation:
                    messagebox.showerror("Error", "Debe introducir una observación")
                    return
                
                # Guardar observación
                success = self.excel_manager.save_observation(
                    selected_date.get(),
                    selected_time.get(),
                    selected_line.get(),
                    selected_machine.get(),
                    observation,
                    self.user_name  # ✅ Cambiar self.current_user por self.user_name
                )
                
                if success:
                    messagebox.showinfo("Éxito", "✅ Incidencia guardada correctamente")
                    dialog.destroy()
                    self.load_today_observations()
                else:
                    messagebox.showerror("Error", "❌ Error al guardar la incidencia")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        # 🎨 Botones
        button_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        button_frame.pack(fill=tk.X, pady=(20, 10))
        
        save_button = tk.Button(button_frame, text="💾 Guardar", command=save_incident,
                               bg=self.colors.BUTTON_PRIMARY, fg=self.colors.TEXT_ON_GOLD,
                               font=("Arial", 10, "bold"), padx=20, pady=5)
        save_button.pack(side=tk.LEFT, padx=(0, 15))
        
        cancel_button = tk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy,
                                 bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                                 font=("Arial", 10, "bold"), padx=20, pady=5)
        cancel_button.pack(side=tk.LEFT)

    def create_modern_form_field(self, parent, label_text, variable, widget_class, widget_options):
        """Crea un campo de formulario con estilo moderno"""
        ttk.Label(parent, text=label_text, style="Modern.TLabel").pack(anchor=tk.W, pady=(10, 5))
        
        if widget_class == DateEntry:
            widget = widget_class(parent, textvariable=variable, **widget_options)
        else:
            widget = widget_class(parent, textvariable=variable, **widget_options)
        
        widget.pack(pady=(5, 10), fill=tk.X)
        return widget

    def load_available_users(self):
        """Carga lista de nombres de usuario disponibles"""
        try:
            users_with_passwords = self.load_users_with_passwords()
            user_names = [user_data[1] for user_data in users_with_passwords if len(user_data) > 1]
            return user_names
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios disponibles: {str(e)}")
            return ["usuario", "mecanico", "admin"]

    def setup_menu(self):
        """Configura la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo (izquierda)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.clear_fields)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.handle_logout)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Actualizar", command=self.load_today_observations)
        
        # 🎯 Menú Admin - MOVIDO A LA DERECHA Y MEJORADO
        admin_menu = tk.Menu(menubar, tearoff=0)
        
        if self.user_role == 'admin':
            # Menú admin completo con salir de cuenta
            menubar.add_cascade(label="👑 Admin ▼", menu=admin_menu)
            admin_menu.add_command(label="📊 Consola de Logs", command=self.show_admin_console)
            admin_menu.add_command(label="👥 Gestión de Usuarios", command=self.show_user_management)
            admin_menu.add_command(label="⚙️ Configuración Avanzada", command=self.show_advanced_config)
            admin_menu.add_separator()
            admin_menu.add_command(label="🔧 Herramientas de Sistema", command=self.show_system_tools)
            admin_menu.add_separator()
            admin_menu.add_command(label="🚪 Salir de Cuenta Admin", command=self.logout_from_admin)
        else:
            # Opción de login para admin
            menubar.add_cascade(label="👑 Admin", menu=admin_menu)
            admin_menu.add_command(label="🔐 Acceder como Admin", command=self.show_admin_login)

    def setup_context_menu(self):
        """Configura menú contextual"""
        pass

    def show_context_menu(self, event):
        """Muestra menú contextual"""
        pass

    def open_full_list_window(self):
        """Abre ventana con lista completa"""
        messagebox.showinfo("Lista Completa", "Funcionalidad en desarrollo...")

    def update_status(self, message):
        """Actualiza mensaje de la barra de estado con iconos"""
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=message)

    def run(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error en la aplicación: {str(e)}")

    def get_user_icon(self, role):
        """Obtiene icono según el rol del usuario"""
        icons = {
            'admin': '👑',
            'mecanico': '🔧',
            'usuario': '👤'
        }
        return icons.get(role, '👤')

    def get_role_display_name(self, role):
        """Obtiene nombre de visualización del rol"""
        names = {
            'admin': 'Administrador',
            'mecanico': 'Mecánico',
            'usuario': 'Usuario'
        }
        return names.get(role, 'Usuario')

    def logout_from_admin(self):
        """Cierra sesión de admin y vuelve al login"""
        result = messagebox.askyesno(
            "Salir de Cuenta Admin", 
            f"¿Confirmas que quieres salir de la cuenta de {self.user_name}?\n\nEsto te devolverá a la ventana de login inicial."
        )
        if result:
            if self.logout_callback:
                self.logout_callback()
            else:
                self.root.destroy()
    
    def load_today_observations(self):
        """Carga y muestra las observaciones del día actual"""
        print("📊 [DEBUG] Iniciando load_today_observations()")
        try:
            today = get_today_date()
            print(f"📊 [DEBUG] Fecha de hoy: {today}")
            
            observations = self.excel_manager.get_observations_by_date(today)
            print(f"📊 [DEBUG] Observaciones encontradas: {len(observations)}")
            
            # Limpiar y actualizar lista
            if hasattr(self, 'observations_listbox'):
                self.observations_listbox.delete(0, tk.END)
                
                if observations:
                    for i, obs in enumerate(observations, 1):
                        # ✅ Corregir: obs es una tupla, no un diccionario
                        # Formato de tupla: (fecha, hora, línea, máquina, observación, usuario)
                        fecha = obs[0] if len(obs) > 0 else 'N/A'
                        hora = obs[1] if len(obs) > 1 else 'N/A'
                        linea = obs[2] if len(obs) > 2 else 'N/A'
                        maquina = obs[3] if len(obs) > 3 else 'N/A'
                        observacion = obs[4] if len(obs) > 4 else 'N/A'
                        usuario = obs[5] if len(obs) > 5 else 'N/A'
                        
                        display_text = f"{i:2d}. {hora} - {maquina}: {observacion} ({usuario})"
                        self.observations_listbox.insert(tk.END, display_text)
                else:
                    self.observations_listbox.insert(tk.END, "📝 No hay observaciones registradas para hoy")
                    self.observations_listbox.insert(tk.END, "💡 Usa el botón 'Nueva Observación' para agregar una")
            
            # Actualizar estado
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"✅ Cargadas {len(observations)} observaciones de {today}")
            
            print(f"📊 [DEBUG] Lista actualizada con {len(observations)} observaciones")
            
        except Exception as e:
            error_msg = f"❌ Error al cargar observaciones: {str(e)}"
            print(f"📊 [DEBUG] {error_msg}")
            
            if hasattr(self, 'observations_listbox'):
                self.observations_listbox.delete(0, tk.END)
                self.observations_listbox.insert(tk.END, "❌ Error al cargar observaciones")
                self.observations_listbox.insert(tk.END, f"Detalles: {str(e)}")
            
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"❌ Error: {str(e)}")
    
    def show_admin_login(self):
        """Muestra diálogo de login para acceder como admin"""
        # Crear ventana de diálogo
        login_dialog = tk.Toplevel(self.root)
        login_dialog.title("🔐 Acceso de Administrador")
        login_dialog.geometry("400x250")
        login_dialog.configure(bg=self.colors.BACKGROUND_PRIMARY)
        login_dialog.resizable(False, False)
        login_dialog.transient(self.root)
        login_dialog.grab_set()
        
        # Centrar diálogo
        login_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Frame principal
        main_frame = tk.Frame(login_dialog, bg=self.colors.BACKGROUND_PRIMARY, padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="👑 Acceso de Administrador",
            font=("Arial", 16, "bold"),
            fg=self.colors.CORPORATE_GOLD,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # Campo usuario
        tk.Label(main_frame, text="Usuario:", font=("Arial", 10), 
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.BACKGROUND_PRIMARY).pack(anchor="w")
        username_var = tk.StringVar()
        username_entry = tk.Entry(main_frame, textvariable=username_var, font=("Arial", 11), width=25)
        username_entry.pack(pady=(5, 10), fill="x")
        
        # Campo contraseña
        tk.Label(main_frame, text="Contraseña:", font=("Arial", 10),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.BACKGROUND_PRIMARY).pack(anchor="w")
        password_var = tk.StringVar()
        password_entry = tk.Entry(main_frame, textvariable=password_var, show="*", font=("Arial", 11), width=25)
        password_entry.pack(pady=(5, 20), fill="x")
        
        # Función de validación
        def validate_admin_login():
            username = username_var.get().strip()
            password = password_var.get().strip()
            
            # Validación simple (misma que en login_window.py)
            valid_admins = {
                "admin": "admin123",
                "administrador": "admin123",
                "supervisor": "sup123"
            }
            
            if username in valid_admins and valid_admins[username] == password:
                # ✅ Login exitoso - cambiar rol a admin
                self.user_role = 'admin'
                self.user_name = username
                
                # Actualizar título de ventana
                self.root.title(f"COPY VALLS - Sistema de Mantenimiento - {self.user_name} (Admin)")
                
                # Recrear menú con permisos de admin
                self.setup_menu()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("✅ Acceso Concedido", f"Bienvenido, {username}!\nAhora tienes permisos de administrador.")
                
                login_dialog.destroy()
            else:
                messagebox.showerror("❌ Error de Acceso", "Usuario o contraseña incorrectos.")
                password_var.set("")  # Limpiar contraseña
                password_entry.focus_set()
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=self.colors.BACKGROUND_PRIMARY)
        button_frame.pack(fill="x", pady=(10, 0))
        
        login_btn = tk.Button(
            button_frame,
            text="🔐 Acceder",
            command=validate_admin_login,
            bg=self.colors.BUTTON_PRIMARY,
            fg=self.colors.TEXT_ON_GOLD,
            font=("Arial", 10, "bold"),
            padx=20, pady=5
        )
        login_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancelar",
            command=login_dialog.destroy,
            bg=self.colors.BUTTON_SECONDARY,
            fg=self.colors.TEXT_PRIMARY,
            font=("Arial", 10),
            padx=20, pady=5
        )
        cancel_btn.pack(side="left")
        
        # Configurar eventos
        username_entry.bind("<Return>", lambda e: password_entry.focus_set())
        password_entry.bind("<Return>", lambda e: validate_admin_login())
        username_entry.focus_set()
    
    def show_admin_console(self):
        """Muestra la consola de logs para admin"""
        messagebox.showinfo("📊 Consola de Logs", "Funcionalidad en desarrollo...\n¡Próximamente!")
    
    def show_user_management(self):
        """Muestra gestión de usuarios"""
        messagebox.showinfo("👥 Gestión de Usuarios", "Funcionalidad en desarrollo...\n¡Próximamente!")
    
    def show_advanced_config(self):
        """Muestra configuración avanzada"""
        messagebox.showinfo("⚙️ Configuración Avanzada", "Funcionalidad en desarrollo...\n¡Próximamente!")
    
    def show_system_tools(self):
        """Muestra herramientas de sistema"""
        messagebox.showinfo("🔧 Herramientas de Sistema", "Funcionalidad en desarrollo...\n¡Próximamente!")
    
    def clear_fields(self):
        """Limpia los campos del formulario"""
        pass
    
    def create_modern_form_field(self, parent, label_text, variable, widget_class, widget_options):
        """Crea un campo de formulario con estilo moderno"""
        ttk.Label(parent, text=label_text, style="Modern.TLabel").pack(anchor=tk.W, pady=(10, 5))
        
        if widget_class == DateEntry:
            widget = widget_class(parent, textvariable=variable, **widget_options)
        else:
            widget = widget_class(parent, textvariable=variable, **widget_options)
        
        widget.pack(pady=(5, 10), fill=tk.X)
        return widget