import tkinter as tk
from tkinter import ttk
import yt_dlp as youtube_dl
import pyperclip
import os
from message_box import show_error  # Importa la función show_error desde message_box.py

# Configuración de la ventana
width = 600
height = 600  # Aumentamos la altura para mostrar la lista de videos
root = tk.Tk()
root.title("Python Downloader")

# Carpeta donde se almacenarán los videos
video_dir = "videos/"

def centrar_window(window, width, height):
    """Centrar la ventana en la pantalla"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def actualizar_progreso(d):
    """Actualizar la barra de progreso durante la descarga."""
    if d['status'] == 'downloading':
        porcentaje = d['downloaded_bytes'] / d['total_bytes'] * 100
        progreso['value'] = porcentaje
        status_label.config(text=f"Descargando: {int(porcentaje)}%", fg="blue")
        root.update_idletasks()

def descargar_video():
    """Descargar el video usando el enlace del portapapeles."""
    # Obtener el enlace del portapapeles
    video_link = pyperclip.paste()

    if not video_link.strip():
        show_error(root, "No tienes ningún enlace en el portapapeles")  # Mostrar el error con el mensaje
        return
    
    try:
        # Configuración para descargar el video
        ydl_opts = {
            'outtmpl': f'{video_dir}%(title)s.%(ext)s',  # Carpeta de salida y formato de nombre
            'format': 'best',  # Descargar en la mejor calidad disponible
            'progress_hooks': [actualizar_progreso],  # Hook para actualizar el progreso
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            status_label.config(text="Descargando...", fg="blue")
            ydl.download([video_link])
            status_label.config(text="¡Descarga completada!", fg="green")
            progreso['value'] = 100
            root.update_idletasks()

        # Después de descargar el video, actualizar la lista de videos
        actualizar_lista_videos()

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

def obtener_info_video(video_path):
    """Obtener información sobre el video (resolución, calidad de sonido, duración)."""
    try:
        # Usamos ffprobe (parte de ffmpeg) para obtener los metadatos del video
        import subprocess
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,codec_name,duration', 
             '-of', 'default=noprint_wrappers=1', video_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # Parseamos los datos obtenidos
        info = result.stdout.split('\n')
        width = height = None
        codec = None
        duration = None
        
        for line in info:
            if "width=" in line:
                width = line.split('=')[1]
            elif "height=" in line:
                height = line.split('=')[1]
            elif "codec_name=" in line:
                codec = line.split('=')[1]
            elif "duration=" in line:
                duration = float(line.split('=')[1])

        resolution = f"{width}x{height}" if width and height else "Desconocida"
        duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}" if duration else "Desconocida"
        return resolution, codec, duration_str
    except Exception as e:
        return "Error", "Error", "Error"

def actualizar_lista_videos():
    """Actualizar la lista de videos en la interfaz gráfica."""
    # Limpiar la lista actual
    for row in video_tree.get_children():
        video_tree.delete(row)

    # Leer todos los videos en la carpeta
    for filename in os.listdir(video_dir):
        if filename.endswith((".mp4", ".mkv", ".avi")):  # Filtrar archivos de video
            video_path = os.path.join(video_dir, filename)

            # Obtener información del video
            resolution, codec, duration = obtener_info_video(video_path)

            # Obtener el tamaño del archivo
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # Convertir a MB
            file_size = f"{file_size:.2f} MB"

            # Agregar una fila a la lista
            video_tree.insert("", "end", values=(filename, file_size, resolution, codec, duration))

# Widgets
button = tk.Button(root, text="Descargar", command=descargar_video)
button.pack(side="top", padx=10, pady=10)

# Barra de progreso
progreso = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progreso.pack(side="top", padx=10, pady=10)

# Etiqueta de estado
status_label = tk.Label(root, text="", bg="white", font=("Arial", 10))
status_label.pack(side="top", pady=20)

# Lista de videos
columns = ("Nombre", "Peso", "Resolución", "Calidad de sonido", "Duración")
video_tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
video_tree.pack(side="top", padx=10, pady=10)

# Configurar las cabeceras de las columnas
for col in columns:
    video_tree.heading(col, text=col)

# Configurar y centrar ventana
centrar_window(root, width, height)
root.configure(bg="white")

# Actualizar la lista de videos al inicio
actualizar_lista_videos()

root.mainloop()
