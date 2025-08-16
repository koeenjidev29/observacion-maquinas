#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para completar la implementación del método show_new_incident_dialog
que está truncado en main_window.py
"""

import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.maintenance.file_modifier import FileModifier

def fix_new_incident_dialog():
    """Completa la implementación del método show_new_incident_dialog"""
    
    # Ruta del archivo a modificar
    main_window_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'gui', 'main_window.py'
    )
    
    if not os.path.exists(main_window_path):
        print(f"❌ Error: No se encontró el archivo {main_window_path}")
        return False
    
    print(f"🔧 Completando implementación de show_new_incident_dialog en {main_window_path}")
    
    # Crear modificador de archivos
    modifier = FileModifier(main_window_path)
    
    # Leer el contenido actual
    with open(main_window_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el método incompleto
    method_start = content.find('def show_new_incident_dialog(self):')
    if method_start == -1:
        print("❌ Error: No se encontró el método show_new_incident_dialog")
        return False
    
    # Buscar el siguiente método para determinar dónde termina el método incompleto
    next_method_start = content.find('def show_complete_list(self):', method_start)
    if next_method_start == -1:
        print("❌ Error: No se encontró el método show_complete_list")
        return False
    
    # Extraer la parte antes del método incompleto
    before_method = content[:method_start]
    
    # Extraer la parte después del método incompleto
    after_method = content[next_method_start:]
    
    # Implementación completa del método
    complete_method = '''def show_new_incident_dialog(self):
        """Muestra diálogo para nueva incidencia"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Observación")
        
        # RESTAURAR comportamiento anterior - tamaño fijo y centrado
        window_width, window_height = self.calculate_window_size(
            width_percent=0.25,   # Más pequeño (25%)
            height_percent=0.35,  # Más pequeño (35%)
            min_width=450,        # Mínimo más pequeño
            min_height=450,       # Mínimo más pequeño
            max_width=550,        # Máximo más pequeño
            max_height=550        # Máximo más pequeño
        )
        
        # Centrar respecto a la ventana principal
        self.center_window(dialog, window_width, window_height)
        
        # BLOQUEAR completamente - NO redimensionable
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame principal con MENOS padding vertical
        main_frame = tk.Frame(dialog, bg=self.colors.SURFACE_LIGHT, padx=15, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="📝 Nueva Observación", 
                              font=("Arial", 14, "bold"),
                              fg=self.colors.CORPORATE_GOLD,
                              bg=self.colors.BACKGROUND_PRIMARY)
        title_label.pack(pady=(0, 20))
        
        # ID automático (solo lectura)
        auto_id = tk.StringVar(value=str(self.db_manager.get_next_id()))
        tk.Label(main_frame, text="ID:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.BACKGROUND_PRIMARY).pack(anchor=tk.W, pady=(0, 2))
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
        
        # Línea de producción
        tk.Label(fields_frame, text="Línea:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=1, column=0, sticky="w", pady=2)
        selected_line = tk.StringVar()
        line_combo = ttk.Combobox(fields_frame, textvariable=selected_line, values=get_lines_list(), 
                                 width=15, font=("Arial", 9), state="readonly")
        line_combo.grid(row=1, column=1, sticky="ew", padx=(5, 15), pady=2)
        
        # Máquina
        tk.Label(fields_frame, text="Máquina:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=1, column=2, sticky="w", pady=2)
        selected_machine = tk.StringVar()
        machine_combo = ttk.Combobox(fields_frame, textvariable=selected_machine, width=15, 
                                    font=("Arial", 9), state="readonly")
        machine_combo.grid(row=1, column=3, sticky="ew", padx=(5, 0), pady=2)
        
        # Función para actualizar máquinas cuando cambia la línea
        def update_machines(*args):
            line = selected_line.get()
            if line:
                machines = get_machines_by_line(line)
                machine_combo['values'] = machines
                selected_machine.set('')  # Limpiar selección anterior
            else:
                machine_combo['values'] = []
                selected_machine.set('')
        
        selected_line.trace('w', update_machines)
        
        # Operador
        tk.Label(fields_frame, text="Operador:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).grid(row=2, column=0, sticky="w", pady=2)
        selected_operator = tk.StringVar(value=get_current_user())
        operator_entry = tk.Entry(fields_frame, textvariable=selected_operator, width=20, font=("Arial", 9))
        operator_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=(5, 0), pady=2)
        
        # Configurar grid weights
        fields_frame.grid_columnconfigure(1, weight=1)
        fields_frame.grid_columnconfigure(3, weight=1)
        
        # Observación (área de texto)
        tk.Label(main_frame, text="Observación:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(10, 2))
        observation_text = scrolledtext.ScrolledText(main_frame, height=4, width=50, font=("Arial", 9),
                                                   wrap=tk.WORD, bg='white')
        observation_text.pack(fill=tk.X, pady=(2, 10))
        
        # Acción tomada
        tk.Label(main_frame, text="Acción Tomada:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(0, 2))
        action_text = scrolledtext.ScrolledText(main_frame, height=3, width=50, font=("Arial", 9),
                                              wrap=tk.WORD, bg='white')
        action_text.pack(fill=tk.X, pady=(2, 10))
        
        # Estado
        tk.Label(main_frame, text="Estado:", font=("Arial", 9, "bold"),
                fg=self.colors.TEXT_PRIMARY, bg=self.colors.SURFACE_LIGHT).pack(anchor=tk.W, pady=(0, 2))
        selected_status = tk.StringVar(value="Pendiente")
        status_combo = ttk.Combobox(main_frame, textvariable=selected_status, 
                                   values=["Pendiente", "En Proceso", "Completado", "Cancelado"],
                                   width=20, font=("Arial", 9), state="readonly")
        status_combo.pack(anchor=tk.W, pady=(2, 15))
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg=self.colors.SURFACE_LIGHT)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def save_observation():
            """Guarda la nueva observación"""
            try:
                # Validar campos requeridos
                if not selected_line.get():
                    messagebox.showerror("Error", "Debe seleccionar una línea de producción")
                    return
                
                if not selected_machine.get():
                    messagebox.showerror("Error", "Debe seleccionar una máquina")
                    return
                
                if not observation_text.get("1.0", tk.END).strip():
                    messagebox.showerror("Error", "Debe ingresar una observación")
                    return
                
                # Preparar datos
                observation_data = {
                    'fecha': selected_date.get(),
                    'hora': selected_time.get(),
                    'linea': selected_line.get(),
                    'maquina': selected_machine.get(),
                    'operador': selected_operator.get(),
                    'observacion': observation_text.get("1.0", tk.END).strip(),
                    'accion_tomada': action_text.get("1.0", tk.END).strip(),
                    'estado': selected_status.get()
                }
                
                # Guardar en la base de datos
                success = self.db_manager.save_observation(
                    fecha=observation_data['fecha'],
                    hora=observation_data['hora'],
                    linea=observation_data['linea'],
                    maquina=observation_data['maquina'],
                    observacion=observation_data['observacion'],
                    usuario=observation_data['operador']
                )
                
                if success:
                    messagebox.showinfo("Éxito", "Observación guardada correctamente")
                    dialog.destroy()
                    self.refresh_data()  # Actualizar la vista principal
                else:
                    messagebox.showerror("Error", "No se pudo guardar la observación")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        # Botón Guardar
        save_btn = tk.Button(button_frame, text="💾 Guardar", command=save_observation,
                            bg=self.colors.CORPORATE_GOLD, fg='white',
                            font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=8)
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botón Cancelar
        cancel_btn = tk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy,
                              bg=self.colors.TEXT_SECONDARY, fg='white',
                              font=("Arial", 10), relief=tk.FLAT, padx=20, pady=8)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Enfocar el primer campo editable
        line_combo.focus_set()

    '''
    
    # Crear el nuevo contenido
    new_content = before_method + complete_method + after_method
    
    # Crear backup
    modifier.create_backup()
    
    # Escribir el nuevo contenido
    try:
        with open(main_window_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Método show_new_incident_dialog completado exitosamente")
        print("📝 Se creó un backup del archivo original")
        print("\n🔧 Cambios realizados:")
        print("   • Agregados todos los campos faltantes (línea, máquina, operador, observación, acción, estado)")
        print("   • Implementada validación de campos requeridos")
        print("   • Agregada funcionalidad dinámica para actualizar máquinas según línea")
        print("   • Implementados botones Guardar y Cancelar")
        print("   • Integración completa con DatabaseManager")
        print("   • Actualización automática de la vista principal")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al escribir el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando corrección del método show_new_incident_dialog...")
    
    success = fix_new_incident_dialog()
    
    if success:
        print("\n✅ ¡Corrección completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Ejecuta 'py main.py' para probar la aplicación")
        print("   2. Prueba crear una nueva observación")
        print("   3. Verifica que todos los campos funcionen correctamente")
    else:
        print("\n❌ La corrección no se pudo completar")
        print("   Revisa los errores mostrados arriba")