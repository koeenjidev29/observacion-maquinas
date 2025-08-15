import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, date
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from excel.excel_manager import ExcelManager
from utils.helpers import (
    get_default_machines, get_lines_list, get_machines_by_line,
    validate_observation, validate_machine,
    get_today_date, format_date_for_display, get_current_user,
    get_filter_options, calculate_date_range, filter_dates_in_range, get_date_range_description
)
from version import get_full_version_string, get_version_string

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(get_full_version_string())
        self.root.geometry("900x700")  # 🆕 Tamaño aumentado para mejor diseño
        self.root.resizable(True, True)
        
        # 🎨 NUEVO: Configurar tema moderno completo
        self.style = ttk.Style()
        from .themes import ModernTheme, ColorPalette
        self.theme = ModernTheme(self.style)
        self.colors = ColorPalette()
        
        # 🎨 Aplicar fondo moderno a la ventana principal
        self.root.configure(bg=self.colors.BACKGROUND)
        
        self.style.theme_use('clam')
        
        # 🎨 NUEVO: Configurar estilos personalizados para tablas
        self.configure_modern_table_styles()
        
        # Inicializar gestor de Excel
        self.excel_manager = ExcelManager()
        
        # Variables de usuario y permisos
        self.current_user = None
        self.current_user_role = None
        self.user_permissions = {
            'usuario': {'can_add': False, 'can_edit_datetime': False, 'can_edit_all': False},
            'mecanico': {'can_add': True, 'can_edit_datetime': False, 'can_edit_all': False},
            'admin': {'can_add': True, 'can_edit_datetime': True, 'can_edit_all': True}
        }
        
        # Mostrar login primero
        if not self.show_login():
            self.root.destroy()
            return
            
        # Variables de la interfaz
        self.selected_date = tk.StringVar(value=get_today_date())
        self.selected_line = tk.StringVar()
        self.selected_machine = tk.StringVar()
        self.selected_user = tk.StringVar()
        self.observation_text = tk.StringVar()
        
        # Listas de líneas, máquinas y usuarios
        self.lines = get_lines_list()
        self.machines = get_default_machines()
        self.users = self.load_available_users()
        
        # Configurar interfaz
        self.setup_menu()
        self.setup_ui()
        self.setup_context_menu()
        
        # Cargar observaciones del día actual automáticamente
        self.load_today_observations()
        
        # Actualizar estado
        self.update_status(f"Conectado como: {self.current_user} ({self.current_user_role})")

    def show_login(self):
        """Muestra ventana de login empresarial moderna"""
        login_window = tk.Toplevel()
        login_window.title("Sistema de Gestión Industrial - Acceso")
        login_window.geometry("450x550")  # 🆕 Tamaño más grande y profesional
        login_window.resizable(False, False)
        login_window.transient(self.root)
        login_window.grab_set()
        
        # 🎨 Fondo empresarial con gradiente
        login_window.configure(bg=self.colors.BACKGROUND_ENTERPRISE)
        
        # 🆕 Header empresarial con logo
        header_frame = ttk.Frame(login_window, style="Enterprise.Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # 🏢 Logo y título empresarial
        company_label = ttk.Label(header_frame, 
                                 text="🏭 SISTEMA DE GESTIÓN\nINDUSTRIAL", 
                                 style="Enterprise.Logo.TLabel",
                                 justify='center')
        company_label.pack(pady=20)
        
        # 🆕 Subtítulo profesional
        subtitle_label = ttk.Label(header_frame,
                                  text="Control y Monitoreo de Máquinas",
                                  style="Enterprise.Subtitle.TLabel")
        subtitle_label.pack()
        
        # 🎨 Frame principal con sombra y bordes redondeados
        main_frame = ttk.Frame(login_window, padding="40", style="Enterprise.Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # 🔐 Título de acceso
        access_label = ttk.Label(main_frame, text="🔐 Acceso al Sistema", 
                                style="Enterprise.Title.TLabel")
        access_label.pack(pady=(0, 30))
        
        # 🆕 Campos con iconos y mejor diseño
        # Campo Usuario
        user_frame = ttk.Frame(main_frame, style="Enterprise.Field.TFrame")
        user_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(user_frame, text="👤 USUARIO", 
                 style="Enterprise.FieldLabel.TLabel").pack(anchor=tk.W, pady=(0, 8))
        username_entry = ttk.Entry(user_frame, textvariable=username_var,
                                  font=('Segoe UI', 12), 
                                  style="Enterprise.TEntry")
        username_entry.pack(fill=tk.X, ipady=8)
        
        # Campo Contraseña
        pass_frame = ttk.Frame(main_frame, style="Enterprise.Field.TFrame")
        pass_frame.pack(fill=tk.X, pady=(0, 30))
        
        ttk.Label(pass_frame, text="🔑 CONTRASEÑA", 
                 style="Enterprise.FieldLabel.TLabel").pack(anchor=tk.W, pady=(0, 8))
        password_entry = ttk.Entry(pass_frame, textvariable=password_var,
                                  show="●", font=('Segoe UI', 12),
                                  style="Enterprise.TEntry")
        password_entry.pack(fill=tk.X, ipady=8)
        
        # 🆕 Botones empresariales mejorados
        button_frame = ttk.Frame(main_frame, style="Enterprise.TFrame")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón Conectar (principal)
        connect_btn = ttk.Button(button_frame, text="🔗 CONECTAR",
                                command=validate_login,
                                style="Enterprise.Primary.TButton")
        connect_btn.pack(fill=tk.X, pady=(0, 15), ipady=12)
        
        # Frame para botones secundarios
        secondary_frame = ttk.Frame(button_frame, style="Enterprise.TFrame")
        secondary_frame.pack(fill=tk.X)
        
        # Botón Salir
        exit_btn = ttk.Button(secondary_frame, text="🚪 SALIR",
                             command=self.exit_application,
                             style="Enterprise.Exit.TButton")
        exit_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
        
        # Botón Ayuda
        help_btn = ttk.Button(secondary_frame, text="❓ AYUDA",
                             command=self.show_login_help,
                             style="Enterprise.Help.TButton")
        help_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0), ipady=8)
        
        # 🆕 Footer con información
        footer_frame = ttk.Frame(login_window, style="Enterprise.Footer.TFrame")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        version_label = ttk.Label(footer_frame, 
                                 text=f"Versión {get_version_string()} | © 2024 Sistema Industrial",
                                 style="Enterprise.Footer.TLabel")
        version_label.pack(pady=10)
        
        # 🆕 Eventos mejorados
        username_entry.focus()
        password_entry.bind('<Return>', lambda e: validate_login())
        username_entry.bind('<Return>', lambda e: password_entry.focus())
        
        # 🆕 Métodos adicionales
        def exit_application():
            result = messagebox.askyesno("Salir", "¿Desea salir del sistema?")
            if result:
                self.root.quit()
        
        def show_login_help():
            messagebox.showinfo("Ayuda", 
                               "Contacte al administrador del sistema\n" +
                               "para obtener credenciales de acceso.\n\n" +
                               "Usuarios por defecto:\n" +
                               "• admin / admin123\n" +
                               "• mecanico / mec123\n" +
                               "• usuario / user123")

    def show_login(self):
        """Muestra ventana de login y valida credenciales"""
        login_window = tk.Toplevel()
        login_window.title("Iniciar Sesión")
        login_window.geometry("350x250")  # 🎨 Tamaño aumentado
        login_window.resizable(False, False)
        login_window.transient(self.root)
        login_window.grab_set()
        
        # 🎨 Aplicar tema moderno a la ventana de login
        login_window.configure(bg=self.colors.BACKGROUND)
        
        # Centrar ventana
        login_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 250, self.root.winfo_rooty() + 200))
        
        # Variables
        username_var = tk.StringVar()
        password_var = tk.StringVar()
        login_successful = [False]
        
        # 🎨 Frame principal con estilo moderno
        main_frame = ttk.Frame(login_window, padding="25", style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 🎨 Título con estilo moderno
        title_label = ttk.Label(main_frame, text="🔐 Iniciar Sesión", 
                               style="Modern.Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # 🎨 Campo Usuario con estilo moderno
        ttk.Label(main_frame, text="👤 Usuario:", style="Modern.TLabel").pack(anchor=tk.W, pady=(0, 5))
        username_entry = ttk.Entry(main_frame, textvariable=username_var, 
                                  font=('Segoe UI', 11), style="Modern.TEntry")
        username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # 🎨 Campo Contraseña con estilo moderno
        ttk.Label(main_frame, text="🔑 Contraseña:", style="Modern.TLabel").pack(anchor=tk.W, pady=(0, 5))
        password_entry = ttk.Entry(main_frame, textvariable=password_var, 
                                  show="*", font=('Segoe UI', 11), style="Modern.TEntry")
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        def validate_login():
            username = username_var.get().strip()
            password = password_var.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Por favor, complete todos los campos")
                return
            
            # Cargar usuarios y validar
            users = self.load_users_with_passwords()
            for user_data in users:
                if len(user_data) >= 4 and user_data[1] == username and user_data[2] == password:
                    self.current_user = username
                    self.current_user_role = user_data[3] if len(user_data) > 3 else 'usuario'
                    login_successful[0] = True
                    login_window.destroy()
                    return
            
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        # 🎨 Botones con estilos modernos
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        login_btn = ttk.Button(button_frame, text="✅ Iniciar Sesión", 
                              command=validate_login, style="Modern.Primary.TButton")
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancelar", 
                               command=login_window.destroy, style="Modern.Secondary.TButton")
        cancel_btn.pack(side=tk.LEFT)
        
        # Focus y eventos
        username_entry.focus()
        password_entry.bind('<Return>', lambda e: validate_login())
        
        # Esperar a que se cierre la ventana
        login_window.wait_window()
        return login_successful[0]

    def load_users_with_passwords(self):
        """Carga usuarios con contraseñas desde archivo"""
        try:
            users_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'usuarios.txt')
            users = []
            
            if os.path.exists(users_file):
                with open(users_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split(',')
                            if len(parts) >= 4:
                                users.append([p.strip() for p in parts])
            
            # Si no hay usuarios, crear usuarios por defecto
            if not users:
                default_users = [
                    ['1', 'admin', 'admin123', 'admin'],
                    ['2', 'mecanico', 'mec123', 'mecanico'],
                    ['3', 'usuario', 'user123', 'usuario']
                ]
                self.save_users_with_passwords(default_users)
                return default_users
            
            return users
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")
            return [['1', 'admin', 'admin123', 'admin']]

    def save_users_with_passwords(self, users):
        """Guarda usuarios con contraseñas en archivo"""
        try:
            users_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'usuarios.txt')
            with open(users_file, 'w', encoding='utf-8') as f:
                f.write("# Formato: id,usuario,contraseña,rol\n")
                for user in users:
                    f.write(','.join(map(str, user)) + '\n')
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar usuarios: {str(e)}")

    def setup_ui(self):
        """Configura la interfaz de usuario con tema moderno completo"""
        # 🎨 NUEVA: Barra de usuario superior con estilo moderno
        self.setup_modern_user_bar()
        
        # 🎨 Frame principal con estilo moderno
        main_frame = ttk.Frame(self.root, padding="15", style="Modern.TFrame")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 🎨 Título con estilo moderno
        title_text = f"📊 Registro de Observaciones de Máquinas\n{get_version_string()}"
        title_label = ttk.Label(main_frame, text=title_text, 
                               style="Modern.Title.TLabel", justify='center')
        title_label.grid(row=0, column=0, pady=(0, 25))
        
        # 🎨 NUEVA ESTRUCTURA: Vista principal con LabelFrame moderno
        today_frame = ttk.LabelFrame(main_frame, 
                                   text=f"📅 Incidencias de Hoy - {get_today_date()}", 
                                   padding="15", style="Modern.TLabelframe")
        today_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        today_frame.columnconfigure(0, weight=1)
        today_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 🎨 Botones de acción con estilos modernos
        self.setup_modern_action_buttons(today_frame)
        
        # 🎨 Tabla de observaciones con estilo moderno
        self.setup_today_observations_table(today_frame)
        
        # 🎨 Barra de estado con estilo moderno
        self.setup_modern_status_bar(main_frame)

    def setup_modern_user_bar(self):
        """Configura barra de usuario superior con tema moderno"""
        user_frame = ttk.Frame(self.root, style="Modern.Card.TFrame", padding="10")
        user_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # 🎨 NUEVO: Perfil clicable con menú desplegable
        profile_frame = ttk.Frame(user_frame, style="Modern.TFrame")
        profile_frame.pack(side=tk.LEFT)
        
        # Información del usuario con iconos - AHORA CLICABLE
        role_icon = self.get_user_icon(self.current_user_role)
        user_info = f"{role_icon} {self.current_user} ({self.get_role_display_name(self.current_user_role)})"
        
        # 🎨 Botón de perfil clicable con estilo moderno
        self.profile_btn = ttk.Button(profile_frame, text=user_info, 
                                     command=self.show_user_profile_menu,
                                     style="Modern.Profile.TButton")
        self.profile_btn.pack(side=tk.LEFT)
        
        # Botón de logout con estilo moderno
        logout_btn = ttk.Button(user_frame, text="🚪 Cerrar Sesión", 
                               command=self.logout, style="Modern.Secondary.TButton")
        logout_btn.pack(side=tk.RIGHT)

    def show_user_profile_menu(self):
        """Muestra menú desplegable del perfil de usuario"""
        # Crear menú contextual
        profile_menu = tk.Menu(self.root, tearoff=0)
        
        # 👤 Información del usuario
        profile_menu.add_command(label=f"👤 Usuario: {self.current_user}", state="disabled")
        profile_menu.add_command(label=f"🎭 Rol: {self.get_role_display_name(self.current_user_role)}", state="disabled")
        profile_menu.add_separator()
        
        # 🔧 Opciones según el rol
        if self.current_user_role == 'admin':
            profile_menu.add_command(label="👑 Panel de Administración", command=self.show_admin_panel)
            profile_menu.add_command(label="👥 Gestionar Usuarios", command=self.show_user_management)
            profile_menu.add_separator()
        
        # 📊 Opciones generales
        profile_menu.add_command(label="📊 Mis Estadísticas", command=self.show_user_stats)
        profile_menu.add_command(label="⚙️ Configuración", command=self.show_user_settings)
        profile_menu.add_separator()
        
        # 🚪 Cerrar sesión
        profile_menu.add_command(label="🚪 Cerrar Sesión", command=self.logout)
        
        # Mostrar menú en la posición del botón
        try:
            x = self.profile_btn.winfo_rootx()
            y = self.profile_btn.winfo_rooty() + self.profile_btn.winfo_height()
            profile_menu.post(x, y)
        except:
            # Si hay error, mostrar en posición del mouse
            profile_menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def show_admin_panel(self):
        """Muestra panel de administración (solo para admins)"""
        if self.current_user_role != 'admin':
            messagebox.showwarning("Sin permisos", "Solo los administradores pueden acceder a esta función")
            return
        messagebox.showinfo("Panel de Admin", "Funcionalidad en desarrollo...")

    def show_user_management(self):
        """Muestra gestión de usuarios (solo para admins)"""
        if self.current_user_role != 'admin':
            messagebox.showwarning("Sin permisos", "Solo los administradores pueden acceder a esta función")
            return
        messagebox.showinfo("Gestión de Usuarios", "Funcionalidad en desarrollo...")

    def show_user_stats(self):
        """Muestra estadísticas del usuario"""
        messagebox.showinfo("Mis Estadísticas", "Funcionalidad en desarrollo...")

    def show_user_settings(self):
        """Muestra configuración del usuario"""
        messagebox.showinfo("Configuración", "Funcionalidad en desarrollo...")

    def setup_modern_action_buttons(self, parent):
        """Configura botones de acción con estilos modernos"""
        action_frame = ttk.Frame(parent, style="Modern.TFrame")
        action_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # 🎨 Botón Nueva Incidencia con estilo primario
        if self.user_permissions[self.current_user_role]['can_add']:
            new_incident_btn = ttk.Button(action_frame, text="➕ Nueva Incidencia", 
                                        command=self.show_new_incident_dialog, 
                                        style='Modern.Primary.TButton')
            new_incident_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 🎨 Botón Ver Lista Completa con estilo secundario
        full_list_btn = ttk.Button(action_frame, text="📋 Ver Lista Completa", 
                                  command=self.open_full_list_window,
                                  style='Modern.Secondary.TButton')
        full_list_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 🎨 Botón Actualizar con estilo secundario
        refresh_btn = ttk.Button(action_frame, text="🔄 Actualizar", 
                               command=self.load_today_observations,
                               style='Modern.Secondary.TButton')
        refresh_btn.pack(side=tk.LEFT)

    def setup_modern_status_bar(self, parent):
        """Configura barra de estado con estilo moderno"""
        self.status_bar = ttk.Label(parent, text="✅ Listo", 
                                   relief=tk.SUNKEN, anchor=tk.W,
                                   style="Modern.TLabel")
        self.status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))

    def configure_modern_table_styles(self):
        """Configura estilos modernos y profesionales para las tablas"""
        
        # 🎨 Estilo para encabezados de tabla
        self.style.configure("Modern.Treeview.Heading",
            background=self.colors.PRIMARY,
            foreground=self.colors.TEXT_ON_PRIMARY,
            font=('Segoe UI', 10, 'bold'),
            relief="flat",
            borderwidth=1
        )
        
        # 🎨 Estilo para el cuerpo de la tabla
        self.style.configure("Modern.Treeview",
            background=self.colors.SURFACE,
            foreground=self.colors.TEXT_PRIMARY,
            font=('Segoe UI', 9),
            fieldbackground=self.colors.SURFACE,
            borderwidth=1,
            relief="solid",
            rowheight=28  # 🎨 Altura de fila mejorada
        )
        
        # 🎨 Colores para selección y hover
        self.style.map("Modern.Treeview",
            background=[('selected', self.colors.SECONDARY),
                       ('active', self.colors.SURFACE_VARIANT)],
            foreground=[('selected', self.colors.TEXT_ON_PRIMARY)]
        )

    def setup_today_observations_table(self, parent):
        """Configura la tabla de observaciones con diseño moderno completo"""
        # 🎨 Frame para la tabla con estilo moderno
        table_frame = ttk.Frame(parent, style="Modern.TFrame")
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # 🎨 Crear Treeview con estilo moderno
        columns = ('Hora', 'Línea', 'Máquina', 'Usuario', 'Rol', 'Observación')
        self.today_tree = ttk.Treeview(table_frame, 
                                      columns=columns, 
                                      show='headings', 
                                      height=15,
                                      style="Modern.Treeview")
        
        # 🎨 Configurar tags para filas con colores por rol
        self.today_tree.tag_configure('oddrow', background=self.colors.SURFACE_VARIANT)
        self.today_tree.tag_configure('evenrow', background=self.colors.SURFACE)
        
        # 🎨 Tags por rol de usuario
        admin_colors = self.colors.get_role_colors('admin')
        mecanico_colors = self.colors.get_role_colors('mecanico')
        usuario_colors = self.colors.get_role_colors('usuario')
        
        self.today_tree.tag_configure('admin_row', 
                                     background=admin_colors['background'], 
                                     foreground=admin_colors['text'])
        self.today_tree.tag_configure('mecanico_row', 
                                     background=mecanico_colors['background'], 
                                     foreground=mecanico_colors['text'])
        self.today_tree.tag_configure('usuario_row', 
                                     background=usuario_colors['background'], 
                                     foreground=usuario_colors['text'])
        
        # 🎨 Configurar encabezados con iconos mejorados
        headers_config = {
            'Hora': {'text': '🕐 Hora', 'width': 100},
            'Línea': {'text': '🏭 Línea', 'width': 120},
            'Máquina': {'text': '⚙️ Máquina', 'width': 140},
            'Usuario': {'text': '👤 Usuario', 'width': 120},
            'Rol': {'text': '🎭 Rol', 'width': 100},
            'Observación': {'text': '📝 Observación', 'width': 350}
        }
        
        # Configurar columnas
        for col, config in headers_config.items():
            self.today_tree.heading(col, text=config['text'])
            self.today_tree.column(col, 
                                  width=config['width'], 
                                  minwidth=config['width']-30,
                                  anchor='center' if col != 'Observación' else 'w')
        
        # 🎨 Scrollbars con estilo moderno
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                   command=self.today_tree.yview,
                                   style="Modern.Vertical.TScrollbar")
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, 
                                   command=self.today_tree.xview)
        self.today_tree.configure(yscrollcommand=v_scrollbar.set, 
                                 xscrollcommand=h_scrollbar.set)
        
        # Grid con mejor espaciado
        self.today_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 🎨 Efectos de hover mejorados
        self.today_tree.bind('<Motion>', self.on_table_hover)
        self.today_tree.bind('<Leave>', self.on_table_leave)
        
        # Menú contextual
        self.today_tree.bind("<Button-3>", self.show_context_menu)
    
    def on_table_hover(self, event):
        """Efecto hover mejorado para la tabla"""
        item = self.today_tree.identify_row(event.y)
        if item:
            self.today_tree.configure(cursor="hand2")
    
    def on_table_leave(self, event):
        """Restaurar cursor normal al salir de la tabla"""
        self.today_tree.configure(cursor="")

    def load_today_observations(self):
        """Carga observaciones del día con estilos modernos mejorados"""
        try:
            today = get_today_date()
            observations = self.excel_manager.get_observations_by_date(today)
            
            # Limpiar tabla
            for item in self.today_tree.get_children():
                self.today_tree.delete(item)
            
            # 🎨 Cargar observaciones con estilos por rol
            for i, obs in enumerate(observations):
                user_role = self.get_user_role(obs[5]) if len(obs) > 5 else 'usuario'
                
                # 🎨 Determinar tags para la fila
                tags = []
                
                # Tag para fila alternada
                if i % 2 == 0:
                    tags.append('evenrow')
                else:
                    tags.append('oddrow')
                
                # Tag según el rol del usuario
                if user_role == 'admin':
                    tags.append('admin_row')
                elif user_role == 'mecanico':
                    tags.append('mecanico_row')
                else:
                    tags.append('usuario_row')
                
                # 🎨 Formatear datos con iconos según el rol
                role_colors = self.colors.get_role_colors(user_role)
                formatted_role = f"{role_colors['icon']} {user_role.title()}"
                
                # Insertar en tabla con estilos
                self.today_tree.insert('', 'end', 
                                      values=(
                                          obs[1],  # Hora
                                          obs[2],  # Línea
                                          obs[3],  # Máquina
                                          obs[5] if len(obs) > 5 else 'N/A',  # Usuario
                                          formatted_role,  # Rol con icono
                                          obs[4]   # Observación
                                      ),
                                      tags=tags)
            
            count = len(observations)
            self.update_status(f"✅ Cargadas {count} observaciones del día {today}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar observaciones del día: {str(e)}")
            self.update_status("❌ Error al cargar observaciones")

    def get_user_role(self, username):
        """Obtiene el rol de un usuario"""
        users = self.load_users_with_passwords()
        for user_data in users:
            if len(user_data) >= 4 and user_data[1] == username:
                return user_data[3] if len(user_data) > 3 else 'usuario'
        return 'usuario'

    def show_new_incident_dialog(self):
        """Muestra diálogo moderno para nueva incidencia"""
        if not self.user_permissions[self.current_user_role]['can_add']:
            messagebox.showwarning("Sin permisos", "No tienes permisos para añadir incidencias")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Nueva Incidencia - {self.current_user} ({self.current_user_role})")
        dialog.geometry("550x650")
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 🎨 Aplicar tema moderno al diálogo
        dialog.configure(bg=self.colors.BACKGROUND)
        
        # Centrar ventana
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 150, self.root.winfo_rooty() + 100))
        
        # Variables
        selected_date = tk.StringVar(value=get_today_date())
        selected_time = tk.StringVar(value=datetime.now().strftime("%H:%M:%S"))
        selected_line = tk.StringVar()
        selected_machine = tk.StringVar()
        
        # 🎨 Frame principal con estilo moderno
        main_frame = ttk.Frame(dialog, padding="25", style="Modern.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 🎨 Título con estilo moderno
        title_text = f"➕ Nueva Incidencia - {self.current_user} ({self.current_user_role})"
        ttk.Label(main_frame, text=title_text, style="Modern.Title.TLabel").pack(pady=(0, 25))
        
        # 🎨 Crear campos de formulario modernos
        self.create_modern_form_field(main_frame, "📅 Fecha:", selected_date, 
                                     DateEntry if self.user_permissions[self.current_user_role]['can_edit_datetime'] else ttk.Entry,
                                     {'date_pattern': 'dd/mm/yyyy'} if self.user_permissions[self.current_user_role]['can_edit_datetime'] else {'state': 'readonly', 'style': 'Modern.TEntry'})
        
        self.create_modern_form_field(main_frame, "🕐 Hora:", selected_time, ttk.Entry,
                                     {} if self.user_permissions[self.current_user_role]['can_edit_datetime'] else {'state': 'readonly', 'style': 'Modern.TEntry'})
        
        self.create_modern_form_field(main_frame, "🏭 Línea:", selected_line, ttk.Combobox,
                                     {'values': self.lines, 'state': 'readonly', 'style': 'Modern.TCombobox'})
        
        self.create_modern_form_field(main_frame, "⚙️ Máquina:", selected_machine, ttk.Combobox,
                                     {'values': self.machines, 'state': 'readonly', 'style': 'Modern.TCombobox'})
        
        # 🎨 Campo de observación con estilo moderno
        ttk.Label(main_frame, text="📝 Observación:", style="Modern.TLabel").pack(anchor=tk.W, pady=(15, 5))
        observation_text = scrolledtext.ScrolledText(main_frame, height=8, width=50,
                                                   font=('Segoe UI', 10))
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
                    self.current_user
                )
                
                if success:
                    messagebox.showinfo("Éxito", "✅ Incidencia guardada correctamente")
                    dialog.destroy()
                    self.load_today_observations()
                else:
                    messagebox.showerror("Error", "❌ Error al guardar la incidencia")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        # 🎨 Botones con estilos modernos
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(fill=tk.X, pady=(20, 10))
        
        ttk.Button(button_frame, text="💾 Guardar", command=save_incident,
                  style="Modern.Success.TButton").pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy,
                  style="Modern.Secondary.TButton").pack(side=tk.LEFT)

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
        """Configura el menú de la aplicación"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Actualizar", command=self.load_today_observations)

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

    def logout(self):
        """Cierra sesión y vuelve al login"""
        result = messagebox.askyesno("Cerrar Sesión", 
                                   "¿Estás seguro de que quieres cerrar sesión?")
        if result:
            self.root.destroy()
            
            # Crear nueva instancia para mostrar login
            new_app = MainWindow()
            if new_app.current_user:
                new_app.run()