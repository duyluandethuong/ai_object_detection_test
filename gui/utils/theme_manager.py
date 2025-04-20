import os
import subprocess
import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self):
        self.style = ttk.Style()
        self.setup_base_styles()
        self.setup_custom_styles()
        
    def setup_base_styles(self):
        """Configure base styles for all widgets"""
        self.style.configure("TFrame", background=self.get_theme_color("background"))
        self.style.configure("TLabel", 
                           background=self.get_theme_color("background"),
                           foreground=self.get_theme_color("text"))
        self.style.configure("TButton",
                           background=self.get_theme_color("button"),
                           foreground=self.get_theme_color("text"))
        self.style.configure("TEntry",
                           fieldbackground=self.get_theme_color("entry"),
                           foreground=self.get_theme_color("text"))
        self.style.configure("TCombobox",
                           fieldbackground=self.get_theme_color("entry"),
                           foreground=self.get_theme_color("text"))
                           
    def setup_custom_styles(self):
        """Configure custom styles for specific widgets"""
        self.style.configure("Title.TLabel",
                           font=('SF Pro Display', 16, 'bold'))
        self.style.configure("Subtitle.TLabel",
                           font=('SF Pro Display', 12))
        self.style.configure("Accent.TButton",
                           font=('SF Pro Display', 12))
        self.style.configure("Danger.TButton",
                           font=('SF Pro Display', 12),
                           background="#FF3B30")
                           
    def get_theme_color(self, element):
        """Get color based on current system theme"""
        if self.is_dark_mode():
            colors = {
                "background": "#1e1e1e",
                "text": "#ffffff",
                "button": "#007AFF",
                "entry": "#2c2c2e",
                "canvas": "#2c2c2e"
            }
        else:
            colors = {
                "background": "#ffffff",
                "text": "#000000",
                "button": "#007AFF",
                "entry": "#f2f2f7",
                "canvas": "#f2f2f7"
            }
        return colors.get(element, "#ffffff")
        
    def is_dark_mode(self):
        """Check if system is in dark mode"""
        try:
            # For macOS
            if os.name == 'posix':
                cmd = 'defaults read -g AppleInterfaceStyle'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return result.stdout.strip() == 'Dark'
        except:
            pass
        return False 