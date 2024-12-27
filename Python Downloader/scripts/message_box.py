import tkinter as tk
from tkinter import messagebox

def show_error(root, message):
    """Mostrar un mensaje de error si no hay enlace en el portapapeles."""
    messagebox.showerror("Error", message, parent=root)
