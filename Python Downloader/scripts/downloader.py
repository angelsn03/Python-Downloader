import flet as ft
import yt_dlp as youtube_dl
from message_box import show_dialog
import pyperclip
import os
import subprocess

# Carpeta donde se almacenarán los videos
video_dir = "videos/"
os.makedirs(video_dir, exist_ok=True)  # Crear la carpeta si no existe

# Configuración de ancho de las celdas
cell_widths = {
    "nombre": 275,
    "peso": 45,
    "duracion": 40,
}

def main(page: ft.Page):
    # Modificar el tamaño de la ventana
    page.window.width = 600  # Ancho de la ventana
    page.window.height = 800  # Alto de la ventana
    page.window.center()  # Centrar la ventana

    page.title = "Python Downloader"
    page.bgcolor = ft.Colors.BLACK12

    # Widgets
    progreso = ft.ProgressBar(width=page.window.width-10, value=0)
    status_label = ft.Text("", size=14, color=ft.Colors.BLUE, opacity=1.0)

    video_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tus descargas", width=cell_widths["nombre"])),
            ft.DataColumn(ft.Text(" ", width=cell_widths["peso"])),
            ft.DataColumn(ft.Text(" ", width=cell_widths["duracion"])),
        ],
        rows=[]
    )

    def actualizar_lista_videos():
        video_table.rows.clear()
        for filename in os.listdir(video_dir):
            if filename.endswith((".mp4", ".mkv", ".avi")):
                video_path = os.path.join(video_dir, filename)
                _, codec, duration = obtener_info_video(video_path)
                file_size = os.path.getsize(video_path) / (1024 * 1024)
                file_size_str = f"{file_size:.2f} mb"
                video_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(filename, width=cell_widths["nombre"])),
                        ft.DataCell(ft.Text(file_size_str, width=cell_widths["peso"])),
                        ft.DataCell(ft.Text(duration, width=cell_widths["duracion"])),
                    ])
                )
        page.update()

    def obtener_info_video(video_path):
        try:
            # Ejecutar ffprobe para obtener información del video
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=codec_name,duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode != 0:
                raise RuntimeError(f"ffprobe error: {result.stderr.strip()}")

            # Extraer codec y duración de la salida
            info = result.stdout.strip().split("\n")
            codec = info[0] if len(info) > 0 else "Desconocido"
            duration = float(info[1]) if len(info) > 1 and info[1].replace('.', '', 1).isdigit() else None

            # Convertir duración a formato mm:ss
            duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}" if duration else "Desconocida"
            return None, codec, duration_str
        except Exception as e:
            print(f"Error al obtener información del video: {e}")
            return None, "Error", "Error"


    def descargar_video(e):
        video_link = pyperclip.paste()

        if not video_link.strip():
            show_dialog(page, "No tienes ningún enlace en el portapapeles.", "Error")
            return

        try:
            def actualizar_progreso(d):
                if d['status'] == 'downloading':
                    porcentaje = d['downloaded_bytes'] / d['total_bytes'] * 100
                    progreso.value = porcentaje / 100
                    status_label.value = f"Descargando: {int(porcentaje)}%"
                    page.update()

            ydl_opts = {
                'outtmpl': f'{video_dir}%(title)s.%(ext)s',
                'format': 'best',
                'progress_hooks': [actualizar_progreso],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                status_label.value = "Descargando..."
                page.update()
                ydl.download([video_link])

            status_label.value = "¡Descarga completada!"
            status_label.color = ft.Colors.GREEN
            progreso.value = 1.0
            page.update()

            # Mostrar mensaje de descarga completada
            show_dialog(page, "¡Tu descarga se concluyó exitosamente!", "Descarga completada")

            actualizar_lista_videos()

        except Exception as ex:
            show_dialog(page, f"Error al descargar el video: {str(ex)}", "Error")
            print(f"Error al descargar el video: {str(ex)}")
   
        finally:
            page.update()
            status_label.value = " "


    def abrir_carpeta_videos(e):
        try:
            carpeta_absoluta = os.path.abspath(video_dir)
            subprocess.Popen(f'explorer "{carpeta_absoluta}"' if os.name == "nt" else f'open "{carpeta_absoluta}"')
        except Exception as ex:
            show_dialog(page, f"No se pudo abrir la carpeta: {str(ex)}", "Error")

    # Botones
    button_descargar = ft.ElevatedButton("Descargar", icon=ft.Icons.DOWNLOAD, on_click=descargar_video)
    button_abrir_carpeta = ft.ElevatedButton("Abrir carpeta", icon=ft.Icons.FOLDER_OPEN, on_click=abrir_carpeta_videos)
    button_settings = ft.ElevatedButton(" ",icon=ft.Icons.SETTINGS, on_click=lambda e: show_dialog(page, "Esta funcionalidad aún no está disponible.", "Atención"))

    # Agregar al layout
    page.add(
        ft.Row(
            controls=[
                ft.Row(
                    controls=[button_descargar, button_abrir_carpeta],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[button_settings],
                    alignment=ft.MainAxisAlignment.END,
                ),   
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Column([
            progreso,
            status_label,
            video_table
        ], alignment=ft.MainAxisAlignment.START, spacing=20, expand=True)
    )

    actualizar_lista_videos()

ft.app(target=main)
