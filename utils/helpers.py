from datetime import datetime, date, timedelta
import os
import re

def get_production_lines():
    """Retorna la estructura de líneas de producción con sus máquinas"""
    return {
        "LÍNEA 1": [
            "MÁQUINA 30 T8",
            "MÁQUINA 31 T12", 
            "MÁQUINA 32 T23",
            "MÁQUINA 33 T16"
        ],
        "LÍNEA 2": [
            "MÁQUINA 29 T8",
            "MÁQUINA 28 T12",
            "MÁQUINA 27 T15",
            "MÁQUINA 26 T20",
            "MÁQUINA 25 T18"
        ],
        "LÍNEA 3": [
            "MÁQUINA 24 T10",
            "MÁQUINA 23 T14",
            "MÁQUINA 22 T16",
            "MÁQUINA 21 T22"
        ],
        "LÍNEA 4": [
            "MÁQUINA 20 T12",
            "MÁQUINA 19 T18",
            "MÁQUINA 18 T25",
            "MÁQUINA 17 T30"
        ],
        "LÍNEA 5": [
            "MÁQUINA 16 T8",
            "MÁQUINA 15 T12",
            "MÁQUINA 14 T16",
            "MÁQUINA 13 T20",
            "MÁQUINA 12 T24"
        ]
    }

def get_default_machines():
    """Retorna la lista de máquinas por defecto (para compatibilidad)"""
    lines = get_production_lines()
    all_machines = []
    for line_machines in lines.values():
        all_machines.extend(line_machines)
    return all_machines

def get_lines_list():
    """Retorna solo la lista de líneas disponibles"""
    return list(get_production_lines().keys())

def get_machines_by_line(line_name):
    """Retorna las máquinas de una línea específica"""
    lines = get_production_lines()
    return lines.get(line_name, [])

def validate_date(date_string):
    """Valida si una cadena es una fecha válida"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_date_for_display(date_obj):
    """Formatea una fecha para mostrar en la interfaz"""
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
    return date_obj.strftime("%d/%m/%Y")

def get_today_date():
    """Obtiene la fecha de hoy en formato YYYY-MM-DD"""
    return date.today().strftime("%Y-%m-%d")

def validate_observation(observation):
    """Valida que la observación no esté vacía y tenga un mínimo de caracteres"""
    if not observation or len(observation.strip()) < 3:
        return False, "La observación debe tener al menos 3 caracteres"
    if len(observation) > 500:
        return False, "La observación no puede exceder 500 caracteres"
    return True, "Observación válida"

def validate_machine(machine, machine_list):
    """Valida que la máquina seleccionada esté en la lista"""
    if not machine:
        return False, "Debe seleccionar una máquina"
    if machine not in machine_list:
        return False, "La máquina seleccionada no es válida"
    return True, "Máquina válida"

def ensure_directory_exists(file_path):
    """Asegura que el directorio del archivo exista"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def get_file_size_mb(file_path):
    """Obtiene el tamaño de un archivo en MB"""
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    return 0

def truncate_text(text, max_length=50):
    """Trunca un texto si excede la longitud máxima"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_current_user():
    """Obtiene el nombre del usuario actual del sistema"""
    import getpass
    return getpass.getuser()

# Funciones de filtrado por períodos
def get_filter_options():
    """Retorna las opciones de filtrado disponibles"""
    return [
        "Día actual",
        "1 semana",
        "15 días",
        "1 mes",
        "Personalizado"
    ]

def calculate_date_range(filter_option, base_date=None):
    """Calcula el rango de fechas según la opción de filtrado"""
    if base_date is None:
        base_date = datetime.now().date()
    elif isinstance(base_date, str):
        base_date = datetime.strptime(base_date, "%Y-%m-%d").date()
    
    if filter_option == "Día actual":
        return base_date, base_date
    elif filter_option == "1 semana":
        start_date = base_date - timedelta(days=6)
        return start_date, base_date
    elif filter_option == "15 días":
        start_date = base_date - timedelta(days=14)
        return start_date, base_date
    elif filter_option == "1 mes":
        start_date = base_date - timedelta(days=29)
        return start_date, base_date
    else:  # Personalizado
        return base_date, base_date

def filter_dates_in_range(all_dates, start_date, end_date):
    """Filtra las fechas que están dentro del rango especificado"""
    filtered_dates = []
    
    for date_str in all_dates:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date_obj <= end_date:
                filtered_dates.append(date_str)
        except ValueError:
            continue
    
    return sorted(filtered_dates)

def get_date_range_description(filter_option, start_date, end_date):
    """Retorna una descripción del rango de fechas seleccionado"""
    if filter_option == "Día actual":
        return f"Mostrando observaciones del {format_date_for_display(start_date.strftime('%Y-%m-%d'))}"
    elif filter_option == "Personalizado":
        if start_date == end_date:
            return f"Mostrando observaciones del {format_date_for_display(start_date.strftime('%Y-%m-%d'))}"
        else:
            return f"Mostrando observaciones desde {format_date_for_display(start_date.strftime('%Y-%m-%d'))} hasta {format_date_for_display(end_date.strftime('%Y-%m-%d'))}"
    else:
        return f"Mostrando observaciones de {filter_option.lower()} (desde {format_date_for_display(start_date.strftime('%Y-%m-%d'))} hasta {format_date_for_display(end_date.strftime('%Y-%m-%d'))})"