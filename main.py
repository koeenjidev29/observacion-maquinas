#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa de Observación de Máquinas - COPY VALLS
Versión 0.1.4.0 - Rediseño Corporativo

Este programa permite registrar observaciones de máquinas por fecha,
creando automáticamente pestañas en Excel organizadas por fecha.

Autor: KoeenjiDEV
Versión: 0.1.4.0
Fecha: 2024-12-20
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.splash import SplashScreen
    from gui.login import LoginWindow
    from gui.main_window import MainWindow
    from version import get_full_version_string
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que todas las dependencias estén instaladas.")
    print("Ejecute: pip install -r requirements.txt")
    sys.exit(1)

class CopyVallsApplication:
    """Aplicación principal de COPY VALLS"""
    
    def __init__(self):
        self.root = None
        self.current_user = None
        self.user_role = None
    
    def start(self):
        """Inicia la aplicación mostrando la pantalla de splash"""
        try:
            self.create_data_directory()
            self.show_splash_screen()
        except Exception as e:
            messagebox.showerror(
                "Error de Inicio",
                f"Error inesperado al iniciar la aplicación:\n{str(e)}"
            )
            return 1
        return 0
    
    def show_splash_screen(self):
        """Muestra la pantalla de splash"""
        splash = SplashScreen(on_complete_callback=self.show_login)
        splash.show()
    
    def show_login(self):
        """Muestra la ventana de login"""
        login_window = LoginWindow(
            on_login_success=self.on_login_success,
            on_exit=self.on_application_exit
        )
        login_window.show()
    
    def on_login_success(self, username):
        """Maneja el login exitoso"""
        self.current_user = username
        self.user_role = self.determine_user_role(username)
        
        print(f"Login exitoso: {username} (Rol: {self.user_role})")
        self.show_main_window()
    
    def determine_user_role(self, username):
        """Determina el rol del usuario basado en el nombre de usuario"""
        admin_users = ['admin', 'administrador', 'supervisor']
        operator_users = ['operador', 'usuario', 'user']
        
        username_lower = username.lower()
        
        if username_lower in admin_users:
            return 'admin'
        elif username_lower in operator_users:
            return 'operator'
        else:
            return 'supervisor'  # Rol por defecto
    
    def show_main_window(self):
        """Muestra la ventana principal"""
        print(f"🚀 [DEBUG] show_main_window() - Usuario: {self.current_user}, Rol: {self.user_role}")
        
        try:
            # ✅ Crear y mostrar MainWindow correctamente
            main_window = MainWindow(
                user_name=self.current_user,
                user_role=self.user_role
            )
            main_window.set_logout_callback(self.on_logout)
            
            print("🚀 [DEBUG] Llamando a main_window.show()...")
            # ✅ ESTO es lo que faltaba - llamar al método show() de MainWindow
            main_window.show()
            
        except Exception as e:
            error_msg = f"Error al abrir la ventana principal: {str(e)}"
            print(f"❌ [DEBUG] {error_msg}")
            messagebox.showerror("Error", error_msg)
            
            # Centrar la ventana
            self.center_window(self.root)
            
            # Iniciar el loop principal
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al abrir la ventana principal:\n{str(e)}"
            )
    
    def on_logout(self):
        """Maneja el logout del usuario"""
        if self.root:
            self.root.destroy()
            self.root = None
        
        self.current_user = None
        self.user_role = None
        
        # Volver a mostrar el login
        self.show_login()
    
    def center_window(self, window):
        """Centra una ventana en la pantalla"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_application_exit(self):
        """Maneja la salida de la aplicación"""
        if self.root:
            self.root.quit()
            self.root.destroy()
        sys.exit(0)
    
    def create_data_directory(self):
        """Crea el directorio de datos si no existe"""
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Directorio de datos creado: {data_dir}")

def main():
    """Función principal"""
    print("="*50)
    print(f"Iniciando COPY VALLS v{get_full_version_string()}...")
    print("="*50)
    
    try:
        app = CopyVallsApplication()
        return app.start()
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
        return 0
    except Exception as e:
        print(f"Error inesperado: {e}")
        messagebox.showerror(
            "Error Fatal",
            f"Error inesperado en la aplicación:\n{str(e)}\n\nLa aplicación se cerrará."
        )
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)