#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidad general para modificar archivos de código de forma segura
"""

import os
import re
from datetime import datetime

class FileModifier:
    def __init__(self, file_path):
        self.file_path = file_path
        self.backup_path = None
        
    def create_backup(self):
        """Crea un backup del archivo original"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")
            
        self.backup_path = f"{self.file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        with open(self.file_path, 'r', encoding='utf-8') as original:
            with open(self.backup_path, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        
        return self.backup_path
    
    def replace_text(self, old_text, new_text, use_regex=False):
        """Reemplaza texto en el archivo"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if use_regex:
            new_content = re.sub(old_text, new_text, content)
        else:
            new_content = content.replace(old_text, new_text)
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return content != new_content
    
    def insert_after_pattern(self, pattern, text_to_insert):
        """Inserta texto después de un patrón encontrado"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
            insertion_point = match.end()
            new_content = content[:insertion_point] + text_to_insert + content[insertion_point:]
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        return False