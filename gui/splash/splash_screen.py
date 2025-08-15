# -*- coding: utf-8 -*-
"""
Splash Screen corporativo para COPY VALLS
Versión 0.1.4.0 - Pantalla de carga inicial
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from gui.themes.corporate_colors import CorporateColors

class SplashScreen:
    """Pantalla de carga corporativa con branding COPY VALLS"""
    
    def __init__(self, on_complete_callback=None):
        self.on_complete = on_complete_callback
        self.colors = CorporateColors()
        self.root = None
        self.progress_var = None
        
    def show(self):
        """Muestra la pantalla de splash"""
        self.root = tk.Tk()
        self.root.title("COPY VALLS - Cargando...")
        
        # Configuración de ventana
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=self.colors.BACKGROUND_PRIMARY)
        self.root.overrideredirect(True)  # Sin barra de título
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(
            self.root,
            bg=self.colors.BACKGROUND_PRIMARY,
            relief="raised",
            bd=2
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo/Título principal
        title_frame = tk.Frame(main_frame, bg=self.colors.BACKGROUND_PRIMARY)
        title_frame.pack(expand=True, fill="both")
        
        # COPY VALLS
        company_label = tk.Label(
            title_frame,
            text="COPY VALLS",
            font=("Arial", 32, "bold"),
            fg=self.colors.TEXT_ON_GOLD,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        company_label.pack(pady=(50, 10))
        
        # MANTENIMIENTO DE MÁQUINAS
        subtitle_label = tk.Label(
            title_frame,
            text="MANTENIMIENTO DE MÁQUINAS",
            font=("Arial", 16, "normal"),
            fg=self.colors.TEXT_SECONDARY,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Barra de progreso
        progress_frame = tk.Frame(main_frame, bg=self.colors.BACKGROUND_PRIMARY)
        progress_frame.pack(side="bottom", fill="x", pady=(0, 30))
        
        # Texto de carga
        self.loading_label = tk.Label(
            progress_frame,
            text="Iniciando sistema...",
            font=("Arial", 10),
            fg=self.colors.TEXT_SECONDARY,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        self.loading_label.pack(pady=(0, 10))
        
        # Barra de progreso estilizada
        style = ttk.Style()
        style.configure(
            "Corporate.Horizontal.TProgressbar",
            background=self.colors.CORPORATE_GOLD,
            troughcolor=self.colors.SURFACE_LIGHT,
            borderwidth=1,
            lightcolor=self.colors.CORPORATE_GOLD,
            darkcolor=self.colors.CORPORATE_DARK_GOLD
        )
        
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="Corporate.Horizontal.TProgressbar",
            length=400
        )
        progress_bar.pack(pady=(0, 10))
        
        # Versión
        from version import get_version_string
        version_label = tk.Label(
            progress_frame,
            text=f"Versión {get_version_string()}",
            font=("Arial", 8),
            fg=self.colors.TEXT_MUTED,
            bg=self.colors.BACKGROUND_PRIMARY
        )
        version_label.pack()
        
        # Iniciar animación de carga
        self.start_loading_animation()
        
        self.root.mainloop()
    
    def start_loading_animation(self):
        """Inicia la animación de carga en un hilo separado"""
        loading_thread = threading.Thread(target=self.loading_process)
        loading_thread.daemon = True
        loading_thread.start()
    
    def loading_process(self):
        """Proceso de carga simulado"""
        steps = [
            ("Iniciando sistema...", 20),
            ("Cargando configuración...", 40),
            ("Conectando base de datos...", 60),
            ("Preparando interfaz...", 80),
            ("Finalizando carga...", 100)
        ]
        
        for message, progress in steps:
            if self.root:
                self.root.after(0, lambda m=message: self.update_loading_text(m))
                self.root.after(0, lambda p=progress: self.update_progress(p))
                time.sleep(0.8)  # Simular tiempo de carga
        
        # Esperar un momento antes de cerrar
        time.sleep(0.5)
        
        if self.root:
            self.root.after(0, self.close_splash)
    
    def update_loading_text(self, text):
        """Actualiza el texto de carga"""
        if self.loading_label:
            self.loading_label.config(text=text)
    
    def update_progress(self, value):
        """Actualiza la barra de progreso"""
        if self.progress_var:
            self.progress_var.set(value)
    
    def close_splash(self):
        """Cierra la pantalla de splash"""
        if self.root:
            self.root.destroy()
            self.root = None
            
        # Llamar callback si existe
        if self.on_complete:
            self.on_complete()