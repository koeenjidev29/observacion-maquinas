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
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
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
        """Muestra ventana de login y valida credenciales"""
        login_window = tk.Toplevel()
        login_window.title("Iniciar Sesión")
        login_window.geometry("300x200")
        login_window.resizable(False, False)
        login_window.transient(self.root)
        login_window.grab_set()
        
        # Centrar ventana
        login_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 250, self.root.winfo_rooty() + 200))
        
        # Variables
        username_var = tk.StringVar()
        password_var = tk.StringVar()
        login_successful = [False]
        
        # Frame principal
        main_frame = ttk.Frame(login_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Iniciar Sesión", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Usuario
        ttk.Label(main_frame, text="Usuario:").pack(anchor=tk.W)
        username_entry = ttk.Entry(main_frame, textvariable=username_var, width=25)
        username_entry.pack(pady=(5, 10), fill=tk.X)
        
        # Contraseña
        ttk.Label(main_frame, text="Contraseña:").pack(anchor=tk.W)
        password_entry = ttk.Entry(main_frame, textvariable=password_var, show="*", width=25)
        password_entry.pack(pady=(5, 15), fill=tk.X)
        
        def validate_login():
            users = self.load_users_with_passwords()
            username = username_var.get().strip()
            password = password_var.get().strip()
            
            for user_data in users:
                if len(user_data) >= 4 and user_data[1] == username and user_data[2] == password:
                    self.current_user = username
                    self.current_user_role = user_data[3] if len(user_data) > 4 else 'usuario'
                    login_successful[0] = True
                    login_window.destroy()
                    return
            
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            password_entry.delete(0, tk.END)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Iniciar Sesión", command=validate_login).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancelar", command=login_window.destroy).pack(side=tk.LEFT)
        
        # Enter para login
        login_window.bind('<Return>', lambda e: validate_login())
        username_entry.focus()
        
        login_window.wait_window()
        return login_successful[0]

    def load_users_with_passwords(self):
        """Carga usuarios con contraseñas desde archivo"""
        users_file = "data/usuarios.txt"
        default_users = [
            (1, "usuario", "123", "usuario", "2024-12-19"),
            (2, "mecanico", "456", "mecanico", "2024-12-19"),
            (3, "admin", "789", "admin", "2024-12-19")
        ]
        
        try:
            if os.path.exists(users_file):
                users = []
                with open(users_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split('|')
                            if len(parts) >= 4:
                                users.append(tuple(parts))
                return users if users else default_users
            else:
                # Crear archivo con usuarios por defecto
                os.makedirs(os.path.dirname(users_file), exist_ok=True)
                self.save_users_with_passwords(default_users)
                return default_users
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")
            return default_users

    def save_users_with_passwords(self, users):
        """Guarda usuarios con contraseñas en archivo"""
        users_file = "data/usuarios.txt"
        try:
            os.makedirs(os.path.dirname(users_file), exist_ok=True)
            with open(users_file, 'w', encoding='utf-8') as f:
                for user in users:
                    f.write(f"{user[0]}|{user[1]}|{user[2]}|{user[3]}|{user[4]}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar usuarios: {str(e)}")

    def setup_ui(self):
        """Configura la interfaz de usuario reorganizada"""
        # NUEVA: Barra de usuario superior
        self.setup_user_bar()
        
        # Frame principal (ahora en row=1)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)  # Cambiar a row=1
        main_frame.columnconfigure(0, weight=1)
        
        # Título simplificado (sin info de usuario, ya está arriba)
        title_text = f"Registro de Observaciones de Máquinas\n{get_version_string()}"
        title_label = ttk.Label(main_frame, text=title_text, font=('Arial', 14, 'bold'), justify='center')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # NUEVA ESTRUCTURA: Vista principal de incidencias del día
        today_frame = ttk.LabelFrame(main_frame, text=f"Incidencias de Hoy - {get_today_date()}", padding="10")
        today_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        today_frame.columnconfigure(0, weight=1)
        today_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Botones de acción principales
        action_frame = ttk.Frame(today_frame)
        action_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botón Nueva Incidencia (solo si tiene permisos)
        if self.user_permissions[self.current_user_role]['can_add']:
            new_incident_btn = ttk.Button(action_frame, text="➕ Nueva Incidencia", 
                                        command=self.show_new_incident_dialog, style='Accent.TButton')
            new_incident_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Ver Lista Completa
        full_list_btn = ttk.Button(action_frame, text="📋 Ver Lista Completa", command=self.open_full_list_window)
        full_list_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Actualizar
        refresh_btn = ttk.Button(action_frame, text="🔄 Actualizar", command=self.load_today_observations)
        refresh_btn.pack(side=tk.LEFT)
        
        # Tabla de observaciones del día
        self.setup_today_observations_table(today_frame)
        
        # Barra de estado
        self.status_bar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def setup_today_observations_table(self, parent):
        """Configura la tabla de observaciones del día actual"""
        # Frame para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Crear Treeview
        columns = ('Hora', 'Línea', 'Máquina', 'Usuario', 'Rol', 'Observación')
        self.today_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.today_tree.heading('Hora', text='Hora')
        self.today_tree.heading('Línea', text='Línea')
        self.today_tree.heading('Máquina', text='Máquina')
        self.today_tree.heading('Usuario', text='Usuario')
        self.today_tree.heading('Rol', text='Rol')
        self.today_tree.heading('Observación', text='Observación')
        
        # Configurar anchos de columna
        self.today_tree.column('Hora', width=80, minwidth=80)
        self.today_tree.column('Línea', width=100, minwidth=80)
        self.today_tree.column('Máquina', width=120, minwidth=100)
        self.today_tree.column('Usuario', width=100, minwidth=80)
        self.today_tree.column('Rol', width=80, minwidth=60)
        self.today_tree.column('Observación', width=300, minwidth=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.today_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.today_tree.xview)
        self.today_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid
        self.today_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Menú contextual
        self.today_tree.bind("<Button-3>", self.show_context_menu)

    def load_today_observations(self):
        """Carga automáticamente las observaciones del día actual"""
        try:
            today = get_today_date()
            observations = self.excel_manager.get_observations_by_date(today)
            
            # Limpiar tabla
            for item in self.today_tree.get_children():
                self.today_tree.delete(item)
            
            # Cargar observaciones
            for obs in observations:
                # Obtener rol del usuario
                user_role = self.get_user_role(obs[5]) if len(obs) > 5 else 'N/A'
                
                # Insertar en tabla con rol
                self.today_tree.insert('', 'end', values=(
                    obs[1],  # Hora
                    obs[2],  # Línea
                    obs[3],  # Máquina
                    obs[5] if len(obs) > 5 else 'N/A',  # Usuario
                    user_role,  # Rol
                    obs[4]   # Observación
                ))
            
            count = len(observations)
            self.update_status(f"Cargadas {count} observaciones del día {today}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar observaciones del día: {str(e)}")
            self.update_status("Error al cargar observaciones")

    def get_user_role(self, username):
        """Obtiene el rol de un usuario"""
        users = self.load_users_with_passwords()
        for user_data in users:
            if len(user_data) >= 4 and user_data[1] == username:
                return user_data[3] if len(user_data) > 3 else 'usuario'
        return 'N/A'

    def show_new_incident_dialog(self):
        """Muestra diálogo para nueva incidencia según permisos del usuario"""
        if not self.user_permissions[self.current_user_role]['can_add']:
            messagebox.showwarning("Sin permisos", "No tienes permisos para añadir incidencias")
            return
        
        dialog = tk.Toplevel(self.root)
        # Configurar diálogo
        dialog.title(f"Nueva Incidencia - {self.current_user} ({self.user_permissions.get('role', 'N/A')})")
        dialog.geometry("500x600")  # Tamaño fijo
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 150, self.root.winfo_rooty() + 100))
        
        # Variables
        selected_date = tk.StringVar(value=get_today_date())
        selected_time = tk.StringVar(value=datetime.now().strftime("%H:%M:%S"))
        selected_line = tk.StringVar()
        selected_machine = tk.StringVar()
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = f"Nueva Incidencia - {self.current_user} ({self.current_user_role})"
        ttk.Label(main_frame, text=title_text, font=('Arial', 12, 'bold')).pack(pady=(0, 20))
        
        # Fecha (editable solo para admin)
        ttk.Label(main_frame, text="Fecha:").pack(anchor=tk.W)
        if self.user_permissions[self.current_user_role]['can_edit_datetime']:
            date_entry = DateEntry(main_frame, textvariable=selected_date, date_pattern='dd/mm/yyyy')
        else:
            date_entry = ttk.Entry(main_frame, textvariable=selected_date, state='readonly')
        date_entry.pack(pady=(5, 10), fill=tk.X)
        
        # Hora (editable solo para admin)
        ttk.Label(main_frame, text="Hora:").pack(anchor=tk.W)
        if self.user_permissions[self.current_user_role]['can_edit_datetime']:
            time_entry = ttk.Entry(main_frame, textvariable=selected_time)
        else:
            time_entry = ttk.Entry(main_frame, textvariable=selected_time, state='readonly')
        time_entry.pack(pady=(5, 10), fill=tk.X)
        
        # Línea
        ttk.Label(main_frame, text="Línea:").pack(anchor=tk.W)
        line_combo = ttk.Combobox(main_frame, textvariable=selected_line, values=self.lines, state="readonly")
        line_combo.pack(pady=(5, 10), fill=tk.X)
        
        # Máquina
        ttk.Label(main_frame, text="Máquina:").pack(anchor=tk.W)
        machine_combo = ttk.Combobox(main_frame, textvariable=selected_machine, values=self.machines, state="readonly")
        machine_combo.pack(pady=(5, 10), fill=tk.X)
        
        # Observación
        ttk.Label(main_frame, text="Observación:").pack(anchor=tk.W)
        observation_text = scrolledtext.ScrolledText(main_frame, height=6, width=50)
        observation_text.pack(pady=(5, 15), fill=tk.BOTH, expand=True)
        
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
                
                # Debug: Mostrar valores que se van a guardar
                print(f"Guardando: Fecha={selected_date.get()}, Hora={selected_time.get()}, Línea={selected_line.get()}, Máquina={selected_machine.get()}, Usuario={self.current_user}")
                
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
                    messagebox.showinfo("Éxito", "Incidencia guardada correctamente")
                    dialog.destroy()
                    self.load_today_observations()  # Recargar tabla
                else:
                    messagebox.showerror("Error", "Error al guardar la incidencia - El método save_observation devolvió False")
                    
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"Error completo: {error_details}")
                messagebox.showerror("Error", f"Error al guardar: {str(e)}\n\nRevisa la consola para más detalles")
        
        # Botones (versión mejorada)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(15, 10), padx=10)
        
        # Botón Guardar
        btn_guardar = ttk.Button(button_frame, text="Guardar", command=save_incident)
        btn_guardar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Cancelar
        btn_cancelar = ttk.Button(button_frame, text="Cancelar", command=dialog.destroy)
        btn_cancelar.pack(side=tk.LEFT)
        
        # Centrar el diálogo
        dialog.update_idletasks()
        dialog.geometry(f"500x650+{(dialog.winfo_screenwidth()//2)-250}+{(dialog.winfo_screenheight()//2)-325}")
        # ❌ ELIMINAR ESTA LÍNEA:
        # ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT)

    def load_available_users(self):
        """Carga lista de nombres de usuario disponibles (sin contraseñas)"""
        try:
            users_with_passwords = self.load_users_with_passwords()
            # Extraer solo los nombres de usuario (índice 1)
            user_names = [user_data[1] for user_data in users_with_passwords if len(user_data) > 1]
            return user_names
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios disponibles: {str(e)}")
            return ["usuario", "mecanico", "admin"]  # Lista por defecto en caso de error
    
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
        """Configura menú contextual para la tabla"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Actualizar", command=self.load_today_observations)
    
    def show_context_menu(self, event):
        """Muestra el menú contextual en la posición del cursor"""
        try:
            # Mostrar el menú en la posición del clic derecho
            self.context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error al mostrar menú contextual: {str(e)}")
    
    def open_full_list_window(self):
        """Abre ventana con lista completa de observaciones"""
        messagebox.showinfo("Información", "Funcionalidad de lista completa en desarrollo")
    
    def update_status(self, message):
        """Actualiza la barra de estado"""
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=message)
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error en la aplicación: {str(e)}")
        finally:
            # Cerrar recursos si es necesario
            if hasattr(self, 'excel_manager'):
                self.excel_manager.close()

    def setup_user_bar(self):
        """Configura la barra superior con información del usuario"""
        # Frame para la barra de usuario
        user_bar = ttk.Frame(self.root, style='UserBar.TFrame')
        user_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        user_bar.columnconfigure(1, weight=1)  # Espacio flexible en el medio
        
        # Configurar estilo para la barra
        self.style.configure('UserBar.TFrame', background='#f0f0f0', relief='solid', borderwidth=1)
        
        # Logo/Icono del programa (izquierda)
        app_label = ttk.Label(user_bar, text="🏭 Observación de Máquinas", font=('Arial', 10, 'bold'))
        app_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Información del usuario (derecha)
        user_info_frame = ttk.Frame(user_bar)
        user_info_frame.grid(row=0, column=2, padx=10, pady=5, sticky=tk.E)
        
        # Icono y nombre de usuario (AHORA CLICKEABLE)
        user_icon = self.get_user_icon(self.current_user_role)
        user_text = f"{user_icon} {self.current_user} ({self.get_role_display_name(self.current_user_role)})"
        user_label = ttk.Label(user_info_frame, text=user_text, font=('Arial', 9), 
                              cursor='hand2', foreground='#0066cc')
        user_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Agregar evento de clic al perfil
        user_label.bind('<Button-1>', self.show_profile_menu)
        
        # Botón de logout
        logout_btn = ttk.Button(user_info_frame, text="🚪 Salir", 
                               command=self.logout, width=8)
        logout_btn.pack(side=tk.LEFT)
    
    def show_profile_menu(self, event):
        """Muestra el menú desplegable del perfil"""
        # Crear menú contextual
        profile_menu = tk.Menu(self.root, tearoff=0)
        
        # Opciones según el rol
        profile_menu.add_command(label=f"👤 Perfil: {self.current_user}", state='disabled')
        profile_menu.add_separator()
        
        if self.current_user_role == 'admin':
            profile_menu.add_command(label="👥 Gestionar Usuarios", command=self.show_user_management)
            profile_menu.add_command(label="📊 Estadísticas Avanzadas", command=self.show_advanced_stats)
            profile_menu.add_separator()
        elif self.current_user_role == 'mecanico':
            profile_menu.add_command(label="🔧 Vista de Trabajo", command=self.show_work_view)
            profile_menu.add_command(label="🔔 Notificaciones", command=self.show_notifications)
            profile_menu.add_separator()
        
        # Opciones comunes
        profile_menu.add_command(label="🔑 Cambiar Contraseña", command=self.change_password)
        profile_menu.add_command(label="⚙️ Configuración", command=self.show_settings)
        profile_menu.add_separator()
        profile_menu.add_command(label="ℹ️ Acerca de", command=self.show_about)
        
        # Mostrar menú en la posición del cursor
        try:
            profile_menu.tk_popup(event.x_root, event.y_root)
        finally:
            profile_menu.grab_release()

    # Métodos placeholder para las nuevas funcionalidades
    def show_user_management(self):
        """Muestra la ventana de gestión de usuarios (solo admin)"""
        messagebox.showinfo("Gestión de Usuarios", "Funcionalidad en desarrollo...\n\n👑 Solo disponible para Administradores")

    def show_advanced_stats(self):
        """Muestra estadísticas avanzadas (solo admin)"""
        messagebox.showinfo("Estadísticas Avanzadas", "Funcionalidad en desarrollo...\n\n📊 Reportes detallados y análisis")

    def show_work_view(self):
        """Muestra vista de trabajo (solo mecánico)"""
        messagebox.showinfo("Vista de Trabajo", "Funcionalidad en desarrollo...\n\n🔧 Panel especializado para mecánicos")

    def show_notifications(self):
        """Muestra notificaciones (solo mecánico)"""
        messagebox.showinfo("Notificaciones", "Funcionalidad en desarrollo...\n\n🔔 Alertas y recordatorios")

    def change_password(self):
        """Permite cambiar la contraseña del usuario"""
        messagebox.showinfo("Cambiar Contraseña", "Funcionalidad en desarrollo...\n\n🔑 Cambio seguro de contraseña")

    def show_settings(self):
        """Muestra configuración personal"""
        messagebox.showinfo("Configuración", "Funcionalidad en desarrollo...\n\n⚙️ Preferencias personales")

    def show_about(self):
        """Muestra información sobre el programa"""
        version = get_full_version_string()
        messagebox.showinfo("Acerca de", f"🏭 Observación de Máquinas\n\nVersión: {version}\n\nUsuario: {self.current_user}\nRol: {self.get_role_display_name(self.current_user_role)}")

    def get_user_icon(self, role):
        """Devuelve el icono según el rol del usuario"""
        icons = {
            'admin': '👑',
            'mecanico': '🔧', 
            'usuario': '👤'
        }
        return icons.get(role, '👤')

    def get_role_display_name(self, role):
        """Devuelve el nombre del rol para mostrar"""
        names = {
            'admin': 'Administrador',
            'mecanico': 'Mecánico',
            'usuario': 'Usuario'
        }
        return names.get(role, 'Usuario')

    def logout(self):
        """Cierra la sesión actual y vuelve al login"""
        result = messagebox.askyesno("Cerrar Sesión", 
                                   f"¿Está seguro que desea cerrar la sesión de {self.current_user}?")
        if result:
            # Limpiar datos de usuario
            self.current_user = None
            self.current_user_role = None
            
            # Cerrar ventana principal
            self.root.destroy()
            
            # Crear nueva instancia para mostrar login
            new_app = MainWindow()
            if new_app.current_user:  # Si login exitoso
                new_app.run()