import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
from tkcalendar import DateEntry
from datetime import datetime, date
import sys
import os

# Agregar el directorio raíz al path para importaciones
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

class MainWindow:
    """Ventana principal de la aplicación de observaciones de máquinas"""
    
    def __init__(self, user_name=None, user_role=None):
        self.root = tk.Tk()
        self.user_name = user_name or "Usuario"
        self.user_role = user_role or "operador"
        self.colors = CorporateColors()
        self.excel_manager = ExcelManager()
        self.logout_callback = None
        
        # Definir permisos por rol
        self.user_permissions = {
            'admin': {'can_delete': True, 'can_edit': True, 'can_configure': True, 'can_view_all': True},
            'administrador': {'can_delete': True, 'can_edit': True, 'can_configure': True, 'can_view_all': True},
            'supervisor': {'can_delete': False, 'can_edit': True, 'can_configure': True, 'can_view_all': True},
            'operador': {'can_delete': False, 'can_edit': False, 'can_configure': False, 'can_view_all': False},
            'tecnico': {'can_delete': False, 'can_edit': True, 'can_configure': False, 'can_view_all': True},
            'invitado': {'can_delete': False, 'can_edit': False, 'can_configure': False, 'can_view_all': False}
        }
    
    def set_logout_callback(self, callback):
        """Establece el callback para logout"""
        self.logout_callback = callback
        
    def show(self):
        """Muestra la ventana principal"""
        # Configurar ventana
        self.root.title(f"📊 Observaciones de Máquinas - {get_full_version_string()} - Usuario: {self.user_name} ({self.get_role_display_name(self.user_role)})")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configurar el cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Configurar colores de fondo
        self.root.configure(bg=self.colors.BACKGROUND_PRIMARY)  # ✅ Cambiado de BACKGROUND a BACKGROUND_PRIMARY
        
        # Crear interfaz
        self.create_interface()
        
        # Configurar menú
        self.setup_menu()
        
        # Cargar observaciones del día
        self.load_today_observations()
        
        # Mostrar mensaje de bienvenida
        self.root.after(500, self.show_welcome_message)
        
        # Iniciar loop principal
        self.root.mainloop()
    
    def create_interface(self):
        """Crea la interfaz principal"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors.BACKGROUND_PRIMARY)  # ✅ Cambiado de BACKGROUND a BACKGROUND_PRIMARY
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear secciones
        self.create_header(main_frame)
        self.create_user_bar(main_frame)
        self.create_main_content(main_frame)
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Crea el encabezado de la aplicación"""
        header_frame = tk.Frame(parent, bg=self.colors.CORPORATE_GOLD, height=80)  # ✅ Cambiado de self.root a parent
        header_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        header_frame.pack_propagate(False)
        
        # Contenido del header
        content_frame = tk.Frame(header_frame, bg=self.colors.CORPORATE_GOLD)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Título principal
        title_label = tk.Label(content_frame, 
                              text="🏭 Sistema de Observaciones de Máquinas",
                              font=("Arial", 18, "bold"),
                              fg=self.colors.TEXT_ON_GOLD,
                              bg=self.colors.CORPORATE_GOLD)
        title_label.pack(side=tk.LEFT)
        
        # Información de versión
        version_label = tk.Label(content_frame,
                                text=get_full_version_string(),
                                font=("Arial", 10),
                                fg=self.colors.TEXT_ON_GOLD,
                                bg=self.colors.CORPORATE_GOLD)
        version_label.pack(side=tk.RIGHT, anchor=tk.E)
    
    def create_user_bar(self, parent):
        """Crea la barra de usuario"""
        user_frame = tk.Frame(parent, bg=self.colors.SURFACE_LIGHT, height=40)
        user_frame.pack(fill=tk.X, pady=(5, 0))
        user_frame.pack_propagate(False)
        
        # Contenido de la barra de usuario
        content_frame = tk.Frame(user_frame, bg=self.colors.SURFACE_LIGHT)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=5)
        
        # Información del usuario (clickeable)
        user_info = f"{self.get_user_icon(self.user_role)} {self.user_name} ({self.get_role_display_name(self.user_role)})"
        user_button = tk.Button(content_frame, text=user_info,
                               font=("Arial", 11, "bold"),
                               fg=self.colors.TEXT_PRIMARY,
                               bg=self.colors.SURFACE_LIGHT,
                               relief=tk.FLAT,
                               cursor="hand2",
                               command=self.show_user_profile)
        user_button.pack(side=tk.LEFT)
        
        # Fecha actual
        today_label = tk.Label(content_frame,
                              text=f"📅 {format_date_for_display(get_today_date())}",
                              font=("Arial", 11),
                              fg=self.colors.TEXT_PRIMARY,
                              bg=self.colors.SURFACE_LIGHT)
        today_label.pack(side=tk.RIGHT)
    
    def create_main_content(self, parent):
        """Crea el contenido principal"""
        content_frame = tk.Frame(parent, bg=self.colors.BACKGROUND_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        
        # Frame de botones
        button_frame = tk.Frame(content_frame, bg=self.colors.BACKGROUND_PRIMARY)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botón Nueva Observación
        new_button = tk.Button(button_frame, text="➕ Nueva Observación",
                              command=self.show_new_incident_dialog,
                              bg=self.colors.BUTTON_PRIMARY,
                              fg=self.colors.TEXT_ON_GOLD,
                              font=("Arial", 11, "bold"),
                              padx=20, pady=8)
        new_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Actualizar
        refresh_button = tk.Button(button_frame, text="🔄 Actualizar Observaciones",
                                  command=self.load_today_observations,
                                  bg=self.colors.BUTTON_SECONDARY,
                                  fg=self.colors.TEXT_ON_GOLD,
                                  font=("Arial", 11, "bold"),
                                  padx=20, pady=8)
        refresh_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Ver Lista Completa
        list_button = tk.Button(button_frame, text="📋 Ver Lista Completa",
                               command=self.show_complete_list,
                               bg="#4299e1",
                               fg="white",
                               font=("Arial", 11, "bold"),
                               padx=20, pady=8)
        list_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Configuración (solo para roles con permisos)
        if self.user_permissions[self.user_role]['can_configure']:
            config_button = tk.Button(button_frame, text="⚙️ Configuración",
                                     command=self.show_config,
                                     bg="#805ad5",
                                     fg="white",
                                     font=("Arial", 11, "bold"),
                                     padx=20, pady=8)
            config_button.pack(side=tk.LEFT)
        
        # Frame para la tabla
        table_frame = tk.Frame(content_frame, bg=self.colors.BACKGROUND_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview para mostrar observaciones
        columns = ('ID', 'Fecha', 'Hora', 'Línea', 'Máquina', 'Subcategoría', 'Observaciones', 'Usuario', 'Rol')
        self.observations_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        column_widths = {
            'ID': 50,
            'Fecha': 100,
            'Hora': 80,
            'Línea': 80,
            'Máquina': 100,
            'Subcategoría': 120,
            'Observaciones': 300,
            'Usuario': 100,
            'Rol': 100
        }
        
        for col in columns:
            self.observations_tree.heading(col, text=col)
            self.observations_tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.observations_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.observations_tree.xview)
        self.observations_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar tabla y scrollbars
        self.observations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configurar estilos alternados para las filas
        self.observations_tree.tag_configure('oddrow', background='#f0f0f0')
        self.observations_tree.tag_configure('evenrow', background='white')
    
    def create_footer(self, parent):
        """Crea el pie de página"""
        footer_frame = tk.Frame(parent, bg=self.colors.SURFACE_LIGHT, height=30)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        # Barra de estado
        self.status_label = tk.Label(footer_frame,
                                    text="✅ Sistema listo",
                                    font=("Arial", 9),
                                    fg=self.colors.TEXT_PRIMARY,
                                    bg=self.colors.SURFACE_LIGHT)
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
    
    def get_role_info(self):
        """Obtiene información detallada del rol"""
        role_info = {
            'admin': "Administrador del sistema con acceso completo a todas las funciones.",
            'administrador': "Administrador del sistema con acceso completo a todas las funciones.",
            'supervisor': "Supervisor con permisos de edición y configuración.",
            'operador': "Operador con permisos básicos de visualización y creación.",
            'tecnico': "Técnico con permisos de edición y visualización amplia.",
            'invitado': "Usuario invitado con permisos limitados de solo lectura."
        }
        return role_info.get(self.user_role, "Rol no definido")
    
    def show_welcome_message(self):
        """Muestra mensaje de bienvenida"""
        welcome_msg = f"¡Bienvenido/a {self.user_name}!\n\nSistema de Observaciones de Máquinas\n{get_full_version_string()}"
        messagebox.showinfo("Bienvenido", welcome_msg)
    
    def show_config(self):
        """Muestra ventana de configuración"""
        messagebox.showinfo("Configuración", "Ventana de configuración - Próximamente disponible")
    
    def handle_logout(self):
        """Maneja el cierre de sesión"""
        result = messagebox.askyesno(
            "Cerrar Sesión",
            f"¿Deseas cerrar la sesión de {self.user_name}?"
        )
        if result:
            self.logout()
    
    def logout(self):
        """Cierra la sesión actual"""
        try:
            self.excel_manager.close_workbook()
        except:
            pass
        
        if self.logout_callback:
            self.logout_callback()
        else:
            self.root.destroy()
    
    def on_window_close(self):
        """Maneja el cierre de la ventana"""
        result = messagebox.askyesno(
            "Salir",
            "¿Deseas salir del programa?"
        )
        if result:
            self.close()
    
    def close(self):
        """Cierra la aplicación"""
        try:
            self.excel_manager.close_workbook()
        except:
            pass
        self.root.destroy()
    
    def show_new_incident_dialog(self):
        """Muestra diálogo para nueva incidencia"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Observación")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 50))
        
        # Frame principal con padding
        main_frame = tk.Frame(dialog, bg=self.colors.SURFACE_LIGHT, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="📝 Nueva Observación", 
                              font=("Arial", 14, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.SURFACE_LIGHT)
        title_label.pack(pady=(0, 20))
        
        # ID automático (solo lectura)
        auto_id = tk.StringVar(value=str(self.excel_manager.get_next_id()))
        tk.Label(main_frame, text="ID:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(0, 2))
        id_entry = tk.Entry(main_frame, textvariable=auto_id, state='readonly', width=10, font=("Arial", 9))
        id_entry.pack(anchor=tk.W, pady=(2, 10))
        
        # Frame para campos en grid
        fields_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        fields_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Fecha y Hora
        tk.Label(fields_frame, text="Fecha:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=0, sticky="w", pady=2)
        selected_date = tk.StringVar(value=get_today_date())
        date_entry = DateEntry(fields_frame, textvariable=selected_date, width=12, 
                              background='darkblue', foreground='white', borderwidth=2, font=("Arial", 9))
        date_entry.grid(row=0, column=1, sticky="ew", padx=(5, 15), pady=2)
        
        tk.Label(fields_frame, text="Hora:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=2, sticky="w", pady=2)
        selected_time = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        time_entry = tk.Entry(fields_frame, textvariable=selected_time, width=8, font=("Arial", 9))
        time_entry.grid(row=0, column=3, sticky="ew", padx=(5, 0), pady=2)
        
        # Línea y Máquina
        tk.Label(fields_frame, text="Línea:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=1, column=0, sticky="w", pady=2)
        selected_line = tk.StringVar()
        line_combo = ttk.Combobox(fields_frame, textvariable=selected_line, values=get_lines_list(),
                                 state='readonly', width=12, font=("Arial", 9))
        line_combo.grid(row=1, column=1, sticky="ew", padx=(5, 15), pady=2)
        
        tk.Label(fields_frame, text="Máquina:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=1, column=2, sticky="w", pady=2)
        selected_machine = tk.StringVar()
        machine_combo = ttk.Combobox(fields_frame, textvariable=selected_machine,
                                    state='readonly', width=12, font=("Arial", 9))
        machine_combo.grid(row=1, column=3, sticky="ew", padx=(5, 0), pady=2)
        
        def update_machines(*args):
            """Actualiza las máquinas según la línea seleccionada"""
            line = selected_line.get()
            if line:
                machines = get_machines_by_line(line)
                machine_combo['values'] = machines
                selected_machine.set('')  # Limpiar selección anterior
        
        selected_line.trace('w', update_machines)
        
        # Categoría
        tk.Label(fields_frame, text="Categoría:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=2, column=0, sticky="w", pady=2)
        selected_category = tk.StringVar(value="General")
        categories = ["General", "Mantenimiento", "Calidad", "Seguridad", "Producción", "Limpieza"]
        category_combo = ttk.Combobox(fields_frame, textvariable=selected_category, values=categories,
                                     state='readonly', width=12, font=("Arial", 9))
        category_combo.grid(row=2, column=3, sticky="ew", padx=(5, 0), pady=2)
        
        # Usuario (solo lectura)
        tk.Label(fields_frame, text="Usuario:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=3, column=0, sticky="w", pady=2)
        user_var = tk.StringVar(value=self.user_name)  # Crear variable para el usuario
        user_entry = tk.Entry(fields_frame, textvariable=user_var, state='readonly', width=15, font=("Arial", 9))
        user_entry.grid(row=3, column=1, sticky="ew", padx=(5, 15), pady=2)
        
        # Configurar grid
        fields_frame.grid_columnconfigure(1, weight=1)
        fields_frame.grid_columnconfigure(3, weight=1)
        
        # Campo de observación compacto
        tk.Label(main_frame, text="Observaciones:", 
                font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY,
                bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 2))
        
        observation_text = scrolledtext.ScrolledText(main_frame, height=6, width=50,
                                                   font=('Arial', 9))
        observation_text.pack(pady=(2, 15), fill=tk.BOTH, expand=True)
        
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
                    f"[{selected_category.get()}] {observation}",  # Incluir categoría
                    self.user_name
                )
                
                if success:
                    messagebox.showinfo("Éxito", f"✅ Incidencia #{auto_id.get()} guardada correctamente")
                    dialog.destroy()
                    self.load_today_observations()
                else:
                    messagebox.showerror("Error", "❌ Error al guardar la incidencia")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        # Botones compactos
        button_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        save_button = tk.Button(button_frame, text="💾 Guardar", command=save_incident,
                               bg=self.colors.BUTTON_PRIMARY, fg=self.colors.TEXT_ON_GOLD,
                               font=("Arial", 9, "bold"), padx=12, pady=3)
        save_button.pack(side=tk.LEFT, padx=(0, 8))
        
        cancel_button = tk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy,
                                 bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                                 font=("Arial", 9, "bold"), padx=12, pady=3)
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
            print(f"Error al cargar usuarios: {str(e)}")
            return []

    def setup_menu(self):
        """Configura el menú de la aplicación"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva Observación", command=self.show_new_incident_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_window_close)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Actualizar", command=self.load_today_observations)
        view_menu.add_command(label="Lista Completa", command=self.show_complete_list)
        
        # Menú Herramientas (solo para admin)
        if self.user_permissions[self.user_role]['can_configure']:
            tools_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Herramientas", menu=tools_menu)
            tools_menu.add_command(label="Configuración", command=self.show_config)
            
            if self.user_role in ['admin', 'administrador']:
                tools_menu.add_separator()
                tools_menu.add_command(label="Panel de Administración", command=self.show_admin_login)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_welcome_message)

    def setup_context_menu(self):
        """Configura menú contextual para la tabla"""
        pass

    def show_context_menu(self, event):
        """Muestra menú contextual"""
        pass

    def show_complete_list(self):
        """Muestra ventana con lista completa de observaciones con filtros"""
        list_window = tk.Toplevel(self.root)
        list_window.title("Lista Completa de Observaciones")
        list_window.geometry("1400x800")
        list_window.transient(self.root)
        list_window.grab_set()
        
        # Centrar ventana
        list_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Frame principal
        main_frame = tk.Frame(list_window, bg=self.colors.BACKGROUND, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="📋 Lista Completa de Observaciones", 
                              font=("Arial", 16, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.BACKGROUND)
        title_label.pack(pady=(0, 20))
        
        # Frame de filtros
        filter_frame = tk.LabelFrame(main_frame, text="🔍 Filtros", font=("Arial", 12, "bold"),
                                    bg=self.colors.SURFACE_LIGHT, fg=self.colors.TEXT_PRIMARY)
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Filtros en grid
        filters_grid = tk.Frame(filter_frame, bg=self.colors.SURFACE_LIGHT)
        filters_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Filtro por ID
        tk.Label(filters_grid, text="ID:", font=("Arial", 10, "bold"),
                bg=self.colors.SURFACE_LIGHT).grid(row=0, column=0, sticky="w", padx=(0, 5))
        filter_id = tk.StringVar()
        id_entry = tk.Entry(filters_grid, textvariable=filter_id, width=10)
        id_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Filtro por Usuario
        tk.Label(filters_grid, text="Usuario:", font=("Arial", 10, "bold"),
                bg=self.colors.SURFACE_LIGHT).grid(row=0, column=2, sticky="w", padx=(0, 5))
        filter_user = tk.StringVar()
        user_combo = ttk.Combobox(filters_grid, textvariable=filter_user, width=15)
        user_combo.grid(row=0, column=3, padx=(0, 20))
        
        # Filtro por Máquina
        tk.Label(filters_grid, text="Máquina:", font=("Arial", 10, "bold"),
                bg=self.colors.SURFACE_LIGHT).grid(row=0, column=4, sticky="w", padx=(0, 5))
        filter_machine = tk.StringVar()
        machine_filter_combo = ttk.Combobox(filters_grid, textvariable=filter_machine, width=15)
        machine_filter_combo.grid(row=0, column=5, padx=(0, 20))
        
        # Filtros de fecha
        tk.Label(filters_grid, text="Desde:", font=("Arial", 10, "bold"),
                bg=self.colors.SURFACE_LIGHT).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(10, 0))
        filter_date_from = tk.StringVar()
        date_from_entry = DateEntry(filters_grid, textvariable=filter_date_from, width=12)
        date_from_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        tk.Label(filters_grid, text="Hasta:", font=("Arial", 10, "bold"),
                bg=self.colors.SURFACE_LIGHT).grid(row=1, column=2, sticky="w", padx=(0, 5), pady=(10, 0))
        filter_date_to = tk.StringVar()
        date_to_entry = DateEntry(filters_grid, textvariable=filter_date_to, width=12)
        date_to_entry.grid(row=1, column=3, padx=(0, 20), pady=(10, 0))
        
        # Botones de filtro
        button_filter_frame = tk.Frame(filters_grid, bg=self.colors.SURFACE_LIGHT)
        button_filter_frame.grid(row=1, column=4, columnspan=2, pady=(10, 0), sticky="w")
        
        def apply_filters():
            """Aplica los filtros a la tabla"""
            try:
                # Obtener todas las observaciones
                all_observations = self.excel_manager.get_all_observations_with_id()
                filtered_observations = []
                
                for obs in all_observations:
                    # obs formato: (id, fecha, hora, linea, maquina, observacion, usuario)
                    include = True
                    
                    # Filtro por ID
                    if filter_id.get() and str(obs[0]) != filter_id.get():
                        include = False
                    
                    # Filtro por Usuario
                    if filter_user.get() and obs[6] != filter_user.get():
                        include = False
                    
                    # Filtro por Máquina
                    if filter_machine.get() and obs[4] != filter_machine.get():
                        include = False
                    
                    # Filtros de fecha
                    if filter_date_from.get():
                        try:
                            obs_date = datetime.strptime(obs[1], "%Y-%m-%d").date()
                            from_date = datetime.strptime(filter_date_from.get(), "%m/%d/%y").date()
                            if obs_date < from_date:
                                include = False
                        except:
                            pass
                    
                    if filter_date_to.get():
                        try:
                            obs_date = datetime.strptime(obs[1], "%Y-%m-%d").date()
                            to_date = datetime.strptime(filter_date_to.get(), "%m/%d/%y").date()
                            if obs_date > to_date:
                                include = False
                        except:
                            pass
                    
                    if include:
                        filtered_observations.append(obs)
                
                # Actualizar tabla
                update_table(filtered_observations)
                status_label.config(text=f"✅ Mostrando {len(filtered_observations)} observaciones filtradas")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al aplicar filtros: {str(e)}")
        
        def clear_filters():
            """Limpia todos los filtros"""
            filter_id.set("")
            filter_user.set("")
            filter_machine.set("")
            filter_date_from.set("")
            filter_date_to.set("")
            load_all_observations()
        
        apply_button = tk.Button(button_filter_frame, text="🔍 Aplicar Filtros", command=apply_filters,
                               bg=self.colors.BUTTON_PRIMARY, fg=self.colors.TEXT_ON_GOLD,
                               font=("Arial", 10, "bold"), padx=15, pady=5)
        apply_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(button_filter_frame, text="🗑️ Limpiar Filtros", command=clear_filters,
                               bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                               font=("Arial", 10, "bold"), padx=15, pady=5)
        clear_button.pack(side=tk.LEFT)
        
        # Frame para la tabla
        table_frame = tk.Frame(main_frame, bg=self.colors.BACKGROUND)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        columns = ('ID', 'Fecha', 'Hora', 'Línea', 'Máquina', 'Subcategoría', 'Observaciones', 'Usuario')
        list_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        column_widths = {
            'ID': 60,
            'Fecha': 100,
            'Hora': 80,
            'Línea': 80,
            'Máquina': 120,
            'Subcategoría': 120,
            'Observaciones': 400,
            'Usuario': 100
        }
        
        for col in columns:
            list_tree.heading(col, text=col)
            list_tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=list_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=list_tree.xview)
        list_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar tabla y scrollbars
        list_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def update_table(observations):
            """Actualiza la tabla con las observaciones"""
            # Limpiar tabla
            for item in list_tree.get_children():
                list_tree.delete(item)
            
            # Agregar observaciones
            for i, obs in enumerate(observations):
                # obs formato: (id, fecha, hora, linea, maquina, observacion, usuario)
                observacion = obs[5] if len(obs) > 5 else 'N/A'
                subcategoria = 'General'
                
                # Extraer subcategoría si existe
                if observacion.startswith('[') and ']' in observacion:
                    end_bracket = observacion.find(']')
                    subcategoria = observacion[1:end_bracket]
                    observacion = observacion[end_bracket+2:]  # +2 para saltar '] '
                
                # Insertar fila
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                list_tree.insert('', 'end', values=(
                    obs[0],  # ID
                    obs[1],  # Fecha
                    obs[2],  # Hora
                    obs[3],  # Línea
                    obs[4],  # Máquina
                    subcategoria,
                    observacion,
                    obs[6] if len(obs) > 6 else 'N/A'  # Usuario
                ), tags=(tag,))
        
        def load_all_observations():
            """Carga todas las observaciones"""
            try:
                all_observations = self.excel_manager.get_all_observations_with_id()
                update_table(all_observations)
                
                # Cargar opciones de filtros
                users = list(set([obs[6] for obs in all_observations if len(obs) > 6]))
                machines = list(set([obs[4] for obs in all_observations if len(obs) > 4]))
                
                user_combo['values'] = [''] + sorted(users)
                machine_filter_combo['values'] = [''] + sorted(machines)
                
                status_label.config(text=f"✅ Cargadas {len(all_observations)} observaciones")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar observaciones: {str(e)}")
                status_label.config(text=f"❌ Error: {str(e)}")
        
        # Configurar estilos alternados
        list_tree.tag_configure('oddrow', background='#f0f0f0')
        list_tree.tag_configure('evenrow', background='white')
        
        # Barra de estado
        status_label = tk.Label(main_frame, text="Cargando...", font=("Arial", 10),
                               fg=self.colors.TEXT_PRIMARY, bg=self.colors.BACKGROUND)
        status_label.pack(pady=(10, 0))
        
        # Cargar datos iniciales
        list_window.after(100, load_all_observations)

    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)

    def run(self):
        """Ejecuta la aplicación"""
        self.show()

    def get_user_icon(self, role):
        """Obtiene el icono correspondiente al rol del usuario"""
        icons = {
            'admin': '👑',
            'administrador': '👑',
            'supervisor': '👨‍💼',
            'operador': '👷',
            'tecnico': '🔧',
            'invitado': '👤'
        }
        return icons.get(role, '👤')

    def get_role_display_name(self, role):
        """Obtiene el nombre de visualización del rol"""
        display_names = {
            'admin': 'Administrador',
            'administrador': 'Administrador',
            'supervisor': 'Supervisor',
            'operador': 'Operador',
            'tecnico': 'Técnico',
            'invitado': 'Invitado'
        }
        return display_names.get(role, role.title())

    def logout_from_admin(self):
        """Cierra sesión desde el panel de administración"""
        result = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Deseas cerrar la sesión actual?"
        )
        if result:
            if self.logout_callback:
                self.logout_callback()
            else:
                self.root.destroy()

    def load_today_observations(self):
        """Loads and displays today's observations in the table"""
        print("📊 [DEBUG] Iniciando load_today_observations()")
        try:
            today = get_today_date()
            print(f"📊 [DEBUG] Fecha de hoy: {today}")
            
            observations = self.excel_manager.get_observations_by_date(today)
            print(f"📊 [DEBUG] Observaciones encontradas: {len(observations)}")
            
            # Limpiar tabla
            if hasattr(self, 'observations_tree'):
                for item in self.observations_tree.get_children():
                    self.observations_tree.delete(item)
                
                if observations:
                    # Generar IDs automáticos
                    for i, obs in enumerate(observations, 1):
                        # Formato de tupla: (fecha, hora, línea, máquina, observación, usuario)
                        fecha = obs[0] if len(obs) > 0 else 'N/A'
                        hora = obs[1] if len(obs) > 1 else 'N/A'
                        linea = obs[2] if len(obs) > 2 else 'N/A'
                        maquina = obs[3] if len(obs) > 3 else 'N/A'
                        observacion = obs[4] if len(obs) > 4 else 'N/A'
                        usuario = obs[5] if len(obs) > 5 else 'N/A'
                        
                        subcategoria = 'General'
                        if observacion.startswith('[') and ']' in observacion:
                            end_bracket = observacion.find(']')
                            subcategoria = observacion[1:end_bracket]
                            observacion = observacion[end_bracket+2:]  # +2 para saltar '] '
                        
                        # Por ahora, rol lo dejamos como 'N/A' hasta que esté disponible en los datos
                        rol = 'N/A'
                        
                        # Insertar fila en la tabla
                        self.observations_tree.insert('', 'end', values=(
                            i,  # ID
                            fecha,
                            hora,
                            linea,
                            maquina,
                            subcategoria,
                            observacion,
                            usuario,
                            rol
                        ))
                else:
                    # Insertar mensaje cuando no hay observaciones
                    self.observations_tree.insert('', 'end', values=(
                          '-', '-', '-', '-', '-', '-', 
                        '📝 No hay observaciones registradas para hoy', '-', '-'
                    ))
            
            # Actualizar estado
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"✅ Cargadas {len(observations)} observaciones de {today}")
            
            print(f"📊 [DEBUG] Tabla actualizada con {len(observations)} observaciones")
            
        except Exception as e:
            error_msg = f"❌ Error al cargar observaciones: {str(e)}"
            print(f"📊 [DEBUG] {error_msg}")
            
            if hasattr(self, 'observations_tree'):
                for item in self.observations_tree.get_children():
                    self.observations_tree.delete(item)
                self.observations_tree.insert('', 'end', values=(
                    '-', '-', '-', '-', '-', '-', 
                    f'❌ Error al cargar: {str(e)}', '-', '-'
                ))
            
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"❌ Error: {str(e)}")
    
    def show_admin_login(self):
        """Muestra diálogo de login para administrador"""
        admin_dialog = tk.Toplevel(self.root)
        admin_dialog.title("Acceso de Administrador")
        admin_dialog.geometry("400x300")
        admin_dialog.resizable(False, False)
        admin_dialog.transient(self.root)
        admin_dialog.grab_set()
        
        # Centrar ventana
        admin_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 200, self.root.winfo_rooty() + 150))
        
        # Frame principal
        main_frame = tk.Frame(admin_dialog, bg=self.colors.SURFACE_LIGHT, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="🔐 Acceso de Administrador", 
                              font=("Arial", 14, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.SURFACE_LIGHT)
        title_label.pack(pady=(0, 20))
        
        # Usuario
        tk.Label(main_frame, text="Usuario:", font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 5))
        
        username_var = tk.StringVar()
        username_entry = tk.Entry(main_frame, textvariable=username_var, font=("Arial", 10))
        username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Contraseña
        tk.Label(main_frame, text="Contraseña:", font=("Arial", 10, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 5))
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(main_frame, textvariable=password_var, show="*", font=("Arial", 10))
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        def validate_admin():
            # Aquí iría la validación real del administrador
            username = username_var.get()
            password = password_var.get()
            
            # Validación simple (en producción usar hash y base de datos)
            valid_admins = {
                "admin": "admin123",
                "administrador": "copy2024"
            }
            
            if username in valid_admins and valid_admins[username] == password:
                admin_dialog.destroy()
                self.show_admin_console()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
                password_entry.delete(0, tk.END)
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        login_button = tk.Button(button_frame, text="🔓 Acceder", command=validate_admin,
                               bg=self.colors.BUTTON_PRIMARY, fg=self.colors.TEXT_ON_GOLD,
                               font=("Arial", 10, "bold"), padx=15, pady=5)
        login_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(button_frame, text="❌ Cancelar", command=admin_dialog.destroy,
                                 bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                                 font=("Arial", 10, "bold"), padx=15, pady=5)
        cancel_button.pack(side=tk.LEFT)
        
        # Focus en el campo de usuario
        username_entry.focus()
        
        # Bind Enter para login
        admin_dialog.bind('<Return>', lambda e: validate_admin())

    def show_admin_console(self):
        """Muestra consola de administración"""
        admin_console = tk.Toplevel(self.root)
        admin_console.title("Panel de Administración")
        admin_console.geometry("500x500")
        admin_console.resizable(False, False)
        admin_console.transient(self.root)
        admin_console.grab_set()
        
        # Centrar ventana
        admin_console.geometry("+%d+%d" % (self.root.winfo_rootx() + 150, self.root.winfo_rooty() + 100))
        
        # Frame principal
        main_frame = tk.Frame(admin_console, bg=self.colors.SURFACE_LIGHT, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="🛠️ Panel de Administración", 
                              font=("Arial", 16, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.SURFACE_LIGHT)
        title_label.pack(pady=(0, 30))
        
        # Información del sistema
        info_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        info_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(info_frame, text=f"📊 Total de observaciones: {self.excel_manager.get_next_id() - 1}", 
                font=("Arial", 10), fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor="w", pady=2)
        
        tk.Label(info_frame, text=f"📁 Archivo Excel: {self.excel_manager.excel_path}", 
                font=("Arial", 10), fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor="w", pady=2)
        
        # Botones de administración
        buttons_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        def open_excel():
            if self.excel_manager.open_excel_file():
                messagebox.showinfo("Éxito", "📊 Archivo Excel abierto correctamente")
            else:
                messagebox.showerror("Error", "❌ No se pudo abrir el archivo Excel")
        
        def refresh_data():
            self.load_today_observations()
            messagebox.showinfo("Actualizado", "🔄 Datos actualizados correctamente")
        
        def delete_all_data():
            """Función para borrar todos los datos con protección por contraseña"""
            # Solicitar contraseña de administrador
            password = tk.simpledialog.askstring("Contraseña de Administrador", 
                                                "Ingrese la contraseña de administrador para continuar:", 
                                                show='*')
            
            if password != "admin123":
                messagebox.showerror("Error", "❌ Contraseña incorrecta")
                return
            
            # Doble confirmación
            confirm1 = messagebox.askyesno("⚠️ ADVERTENCIA", 
                                          "¿Está COMPLETAMENTE SEGURO de que desea BORRAR TODOS los datos?\n\n" +
                                          "Esta acción NO SE PUEDE DESHACER.\n\n" +
                                          "Se eliminarán TODAS las observaciones de TODAS las fechas.")
            
            if not confirm1:
                return
            
            confirm2 = messagebox.askyesno("⚠️ ÚLTIMA CONFIRMACIÓN", 
                                          "ÚLTIMA OPORTUNIDAD:\n\n" +
                                          "¿Confirma que desea ELIMINAR PERMANENTEMENTE todos los datos?\n\n" +
                                          "Escriba SÍ para continuar.")
            
            if not confirm2:
                return
            
            try:
                # Llamar al método para limpiar todas las observaciones
                success = self.excel_manager.clear_all_observations()
                
                if success:
                    messagebox.showinfo("✅ Éxito", 
                                       "Todos los datos han sido eliminados correctamente.\n\n" +
                                       "Se ha creado un nuevo archivo Excel vacío.")
                    # Actualizar la vista
                    self.load_today_observations()
                    admin_console.destroy()
                else:
                    messagebox.showerror("❌ Error", "No se pudieron eliminar los datos")
                    
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error al eliminar datos: {str(e)}")
        
        # Botón para abrir Excel
        excel_button = tk.Button(buttons_frame, text="📊 Abrir Base de Datos (Excel)", 
                                 command=open_excel,
                                 bg=self.colors.BUTTON_PRIMARY, fg=self.colors.TEXT_ON_GOLD,
                                 font=("Arial", 11, "bold"), padx=20, pady=8)
        excel_button.pack(fill="x", pady=(0, 10))
        
        # Botón Ver Lista Completa
        list_button = tk.Button(buttons_frame, text="📋 Ver Lista Completa", 
                               command=self.show_complete_list,
                               bg="#4299e1", fg="white",
                               font=("Arial", 11, "bold"), padx=20, pady=8)
        list_button.pack(fill="x", pady=(0, 10))
        
        # Botón para actualizar datos
        refresh_button = tk.Button(buttons_frame, text="🔄 Actualizar Datos", 
                                  command=refresh_data,
                                  bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                                  font=("Arial", 11, "bold"), padx=20, pady=8)
        refresh_button.pack(fill="x", pady=(0, 10))
        
        # Botón para ver lista completa
        list_button = tk.Button(buttons_frame, text="📋 Ver Lista Completa", 
                               command=self.show_complete_list,
                               bg="#38a169", fg="white",
                               font=("Arial", 11, "bold"), padx=20, pady=8)
        list_button.pack(fill="x", pady=(0, 10))
        
        # Botón para gestión de usuarios
        users_button = tk.Button(buttons_frame, text="👥 Gestión de Usuarios", 
                                command=self.show_user_management,
                                bg="#4299e1", fg="white",
                                font=("Arial", 11, "bold"), padx=20, pady=8)
        users_button.pack(fill="x", pady=(0, 10))
        
        # Botón para borrar todas las observaciones (TESTING)
        def delete_all_observations():
            # Solicitar contraseña de administrador
            password = tk.simpledialog.askstring(
                "Contraseña de Administrador",
                "Ingrese la contraseña de administrador para continuar:",
                show='*'
            )
            
            if password != "admin123":
                messagebox.showerror("Error", "Contraseña incorrecta")
                return
            
            # Doble confirmación
            confirm1 = messagebox.askyesno(
                "⚠️ ADVERTENCIA",
                "¿Está COMPLETAMENTE SEGURO de que desea BORRAR TODAS las observaciones?\n\n" +
                "Esta acción NO SE PUEDE DESHACER.\n\n" +
                "Se eliminará toda la información del archivo Excel."
            )
            
            if not confirm1:
                return
            
            confirm2 = messagebox.askyesno(
                "⚠️ CONFIRMACIÓN FINAL",
                "ÚLTIMA OPORTUNIDAD\n\n" +
                "¿Confirma que desea ELIMINAR PERMANENTEMENTE todas las observaciones?\n\n" +
                "Escriba SÍ para continuar."
            )
            
            if confirm2:
                try:
                    # Llamar al método para limpiar todas las observaciones
                    self.excel_manager.clear_all_observations()
                    messagebox.showinfo(
                        "✅ Completado",
                        "Todas las observaciones han sido eliminadas.\n" +
                        "Se ha creado un nuevo archivo Excel limpio."
                    )
                    # Actualizar la vista
                    self.load_today_observations()
                    admin_console.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar observaciones: {str(e)}")
        
        delete_button = tk.Button(buttons_frame, text="🗑️ Borrar Todas las Observaciones (TESTING)", 
                                 command=delete_all_observations,
                                 bg="#e53e3e", fg="white",
                                 font=("Arial", 11, "bold"), padx=20, pady=8)
        delete_button.pack(fill="x", pady=(0, 20))
        
        # Botón cerrar
        close_button = tk.Button(buttons_frame, text="❌ Cerrar Panel", 
                                command=admin_console.destroy,
                                bg="#718096", fg="white",
                                font=("Arial", 11, "bold"), padx=20, pady=8)
        close_button.pack(fill="x", pady=(0, 0))

    def show_complete_list(self):
        """Muestra ventana con lista completa de observaciones con filtros"""
        list_window = tk.Toplevel(self.root)
        list_window.title("Lista Completa de Observaciones")
        list_window.geometry("1200x700")
        list_window.transient(self.root)
        
        # Centrar ventana
        list_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Frame principal
        main_frame = tk.Frame(list_window, bg=self.colors.BACKGROUND_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="📋 Lista Completa de Observaciones", 
                              font=("Arial", 16, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.SURFACE_LIGHT)
        title_label.pack(pady=(0, 20))
        
        # Frame de filtros
        filters_frame = tk.LabelFrame(main_frame, text="🔍 Filtros", 
                                     font=("Arial", 12, "bold"),
                                     fg=self.colors.TEXT_PRIMARY,
                                     bg=self.colors.BACKGROUND_PRIMARY)
        filters_frame.pack(fill="x", pady=(0, 10))
        
        # Variables de filtro
        filter_id = tk.StringVar()
        filter_user = tk.StringVar()
        filter_machine = tk.StringVar()
        filter_date_from = tk.StringVar()
        filter_date_to = tk.StringVar()
        
        # Crear filtros en una fila
        filters_row = tk.Frame(filters_frame, bg=self.colors.SURFACE_LIGHT)
        filters_row.pack(fill="x", padx=10, pady=10)
        
        # Filtro por ID
        tk.Label(filters_row, text="ID:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=0, sticky="w", padx=(0, 5))
        id_entry = tk.Entry(filters_row, textvariable=filter_id, width=8, font=("Arial", 9))
        id_entry.grid(row=0, column=1, padx=(0, 15))
        
        # Filtro por Usuario
        tk.Label(filters_row, text="Usuario:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=2, sticky="w", padx=(0, 5))
        user_entry = tk.Entry(filters_row, textvariable=filter_user, width=12, font=("Arial", 9))
        user_entry.grid(row=0, column=3, padx=(0, 15))
        
        # Filtro por Máquina
        tk.Label(filters_row, text="Máquina:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=4, sticky="w", padx=(0, 5))
        machine_entry = tk.Entry(filters_row, textvariable=filter_machine, width=12, font=("Arial", 9))
        machine_entry.grid(row=0, column=5, padx=(0, 15))
        
        # Filtro por rango de fechas
        tk.Label(filters_row, text="Desde:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=6, sticky="w", padx=(0, 5))
        date_from_entry = DateEntry(filters_row, textvariable=filter_date_from, width=10, 
                                   background='darkblue', foreground='white', borderwidth=2,
                                   date_pattern='dd/mm/yyyy', font=("Arial", 9))
        date_from_entry.grid(row=0, column=7, padx=(0, 10))
        
        tk.Label(filters_row, text="Hasta:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=0, column=8, sticky="w", padx=(0, 5))
        date_to_entry = DateEntry(filters_row, textvariable=filter_date_to, width=10,
                                 background='darkblue', foreground='white', borderwidth=2,
                                 date_pattern='dd/mm/yyyy', font=("Arial", 9))
        date_to_entry.grid(row=0, column=9, padx=(0, 15))
        
        # Botones de filtro
        apply_button = tk.Button(filters_row, text="🔍 Aplicar Filtros", 
                                command=lambda: apply_filters(),
                                bg=self.colors.BUTTON_PRIMARY, fg=self.colors.TEXT_ON_GOLD,
                                font=("Arial", 9, "bold"), padx=10, pady=3)
        apply_button.grid(row=0, column=10, padx=(0, 5))
        
        clear_button = tk.Button(filters_row, text="🗑️ Limpiar", 
                                command=lambda: clear_filters(),
                                bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                                font=("Arial", 9, "bold"), padx=10, pady=3)
        clear_button.grid(row=0, column=11)
        
        # Tabla de observaciones
        table_frame = tk.Frame(main_frame, bg=self.colors.BACKGROUND_PRIMARY)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview
        columns = ("ID", "Fecha", "Hora", "Línea", "Máquina", "Subcategoría", "Observación", "Usuario")
        observations_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Configurar columnas
        column_widths = {"ID": 50, "Fecha": 80, "Hora": 60, "Línea": 60, "Máquina": 80, 
                        "Subcategoría": 100, "Observación": 300, "Usuario": 80}
        
        for col in columns:
            observations_tree.heading(col, text=col)
            observations_tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=observations_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=observations_tree.xview)
        observations_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Posicionar tabla y scrollbars
        observations_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        def load_all_observations():
            """Carga todas las observaciones en la tabla"""
            try:
                # Limpiar tabla
                for item in observations_tree.get_children():
                    observations_tree.delete(item)
                
                # Obtener todas las observaciones
                all_observations = self.excel_manager.get_all_observations_with_id()
                
                if all_observations:
                    for obs in all_observations:
                        # ✅ Acceder como diccionario
                        obs_id = obs.get('id', 'N/A')
                        fecha = obs.get('fecha', 'N/A')
                        hora = obs.get('hora', 'N/A')
                        linea = obs.get('linea', 'N/A')
                        maquina = obs.get('maquina', 'N/A')
                        observacion = obs.get('observacion', 'N/A')
                        usuario = obs.get('usuario', 'N/A')
                        
                        # Extraer subcategoría
                        subcategoria = 'General'
                        if observacion.startswith('[') and ']' in observacion:
                            end_bracket = observacion.find(']')
                            subcategoria = observacion[1:end_bracket]
                            observacion = observacion[end_bracket+2:]  # +2 para saltar '] '
                        
                        observations_tree.insert('', 'end', values=(
                            obs_id, fecha, hora, linea, maquina, subcategoria, observacion, usuario
                        ))
                else:
                    observations_tree.insert('', 'end', values=(
                        '-', '-', '-', '-', '-', '-', 'No hay observaciones registradas', '-'
                    ))
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar observaciones: {str(e)}")
        
        def apply_filters():
            """Aplica los filtros seleccionados"""
            try:
                # Limpiar tabla
                for item in observations_tree.get_children():
                    observations_tree.delete(item)
                
                # Obtener todas las observaciones
                all_observations = self.excel_manager.get_all_observations_with_id()
                filtered_observations = []
                
                for obs in all_observations:
                    # ✅ Aplicar filtros usando diccionario
                    obs_id = str(obs.get('id', ''))
                    fecha = obs.get('fecha', '')
                    usuario = obs.get('usuario', '')
                    maquina = obs.get('maquina', '')
                    
                    # Filtro por ID
                    if filter_id.get() and filter_id.get() not in obs_id:
                        continue
                    
                    # Filtro por Usuario
                    if filter_user.get() and filter_user.get().lower() not in usuario.lower():
                        continue
                    
                    # Filtro por Máquina
                    if filter_machine.get() and filter_machine.get().lower() not in maquina.lower():
                        continue
                    
                    # Filtro por rango de fechas
                    if filter_date_from.get() or filter_date_to.get():
                        try:
                            obs_date = datetime.strptime(fecha, '%d-%m-%Y').date()  # ✅ Formato correcto
                            
                            if filter_date_from.get():
                                from_date = datetime.strptime(filter_date_from.get(), '%d/%m/%Y').date()
                                if obs_date < from_date:
                                    continue
                            
                            if filter_date_to.get():
                                to_date = datetime.strptime(filter_date_to.get(), '%d/%m/%Y').date()
                                if obs_date > to_date:
                                    continue
                        except:
                            continue
                    
                    filtered_observations.append(obs)
                
                # Mostrar resultados filtrados
                if filtered_observations:
                    for obs in filtered_observations:
                        obs_id = obs.get('id', 'N/A')
                        fecha = obs.get('fecha', 'N/A')
                        hora = obs.get('hora', 'N/A')
                        linea = obs.get('linea', 'N/A')
                        maquina = obs.get('maquina', 'N/A')
                        observacion = obs.get('observacion', 'N/A')
                        usuario = obs.get('usuario', 'N/A')
                        
                        # Extraer subcategoría
                        subcategoria = 'General'
                        if observacion.startswith('[') and ']' in observacion:
                            end_bracket = observacion.find(']')
                            subcategoria = observacion[1:end_bracket]
                            observacion = observacion[end_bracket+2:]
                        
                        observations_tree.insert('', 'end', values=(
                            obs_id, fecha, hora, linea, maquina, subcategoria, observacion, usuario
                        ))
                else:
                    observations_tree.insert('', 'end', values=(
                        '-', '-', '-', '-', '-', '-', 'No se encontraron observaciones con los filtros aplicados', '-'
                    ))
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al aplicar filtros: {str(e)}")
        
        def clear_filters():
            """Limpia todos los filtros"""
            filter_id.set('')
            filter_user.set('')
            filter_machine.set('')
            filter_date_from.set('')
            filter_date_to.set('')
            load_all_observations()
        
        # Cargar todas las observaciones al inicio
        load_all_observations()
        
        # Frame de botones inferiores
        bottom_frame = tk.Frame(main_frame, bg=self.colors.BACKGROUND_PRIMARY)
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        close_list_button = tk.Button(bottom_frame, text="❌ Cerrar", 
                                     command=list_window.destroy,
                                     bg=self.colors.BUTTON_SECONDARY, fg=self.colors.TEXT_ON_GOLD,
                                     font=("Arial", 11, "bold"), padx=20, pady=5)
        close_list_button.pack(side=tk.RIGHT)

    def show_user_management(self):
        """Muestra gestión de usuarios"""
        messagebox.showinfo("Gestión de Usuarios", "Gestión de usuarios - Próximamente disponible")

    def show_advanced_config(self):
        """Muestra configuración avanzada"""
        messagebox.showinfo("Configuración Avanzada", "Configuración avanzada - Próximamente disponible")

    def show_system_tools(self):
        """Muestra herramientas del sistema"""
        messagebox.showinfo("Herramientas del Sistema", "Herramientas del sistema - Próximamente disponible")

    def clear_fields(self):
        """Limpia todos los campos del formulario"""
        pass

    def show_user_profile(self):
        """Muestra el perfil del usuario con menú desplegable"""
        # Crear menú contextual
        profile_menu = tk.Menu(self.root, tearoff=0)
        
        # Información del usuario
        profile_menu.add_command(label=f"👤 {self.user_name}", state="disabled")
        profile_menu.add_command(label=f"🏷️ {self.get_role_display_name(self.user_role)}", state="disabled")
        profile_menu.add_separator()
        
        # Opciones disponibles
        profile_menu.add_command(label="ℹ️ Información del Rol", command=lambda: messagebox.showinfo(
            "Información del Rol", 
            self.get_role_info()
        ))
        
        if self.user_permissions[self.user_role]['can_configure']:
            profile_menu.add_command(label="⚙️ Configuración", command=self.show_config)
        
        profile_menu.add_separator()
        profile_menu.add_command(label="🚪 Cerrar Sesión", command=self.handle_logout)
        profile_menu.add_command(label="❌ Salir del Programa", command=self.on_window_close)
        
        # Mostrar menú en la posición del cursor
        try:
            profile_menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            profile_menu.grab_release()