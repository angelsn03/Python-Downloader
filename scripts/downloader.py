import tkinter as tk
from tkinter import ttk
import yt_dlp as youtube_dl

# Configuración de la ventana
width = 600
height = 400

root = tk.Tk()
root.title("Python Downloader")

def centrar_window(window, width, height):
    # Obtener las dimensiones de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular coordenadas para centrar
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Establecer la geometría de la ventana
    window.geometry(f"{width}x{height}+{x}+{y}")

def actualizar_progreso(d):
    """Actualizar la barra de progreso durante la descarga."""
    if d['status'] == 'downloading':
        # Calcula el porcentaje de progreso
        porcentaje = d['downloaded_bytes'] / d['total_bytes'] * 100
        progreso['value'] = porcentaje
        status_label.config(text=f"Descargando: {int(porcentaje)}%", fg="blue")
        root.update_idletasks()  # Actualiza la interfaz gráficamente

def descargar_video():
    """Descargar el video usando el enlace proporcionado."""
    video_link = link.get()  # Obtener el enlace del Entry
    if not video_link.strip():
        status_label.config(text="Por favor, ingresa un enlace válido.", fg="red")
        return
    
    try:
        # Configuración para descargar el video
        ydl_opts = {
            'outtmpl': 'videos/%(title)s.%(ext)s',  # Carpeta de salida y formato de nombre
            'format': 'best',  # Descargar en la mejor calidad disponible
            'progress_hooks': [actualizar_progreso],  # Hook para actualizar el progreso
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            status_label.config(text="Descargando...", fg="blue")
            ydl.download([video_link])
            status_label.config(text="¡Descarga completada!", fg="green")
            progreso['value'] = 100  # Asegurarse de que la barra llegue al 100%
            root.update_idletasks()  # Actualiza la interfaz al terminar
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

# Widgets
link = tk.Entry(root, width=50)
link.pack(side="top", padx=10, pady=20)

button = tk.Button(root, text="Descargar", command=descargar_video)
button.pack(side="top", padx=10, pady=10)

# Barra de progreso
progreso = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progreso.pack(side="top", padx=10, pady=10)

# Etiqueta de estado
status_label = tk.Label(root, text="", bg="white", font=("Arial", 10))
status_label.pack(side="top", pady=20)

# Configurar y centrar ventana
centrar_window(root, width, height)
root.configure(bg="white")

root.mainloop()
