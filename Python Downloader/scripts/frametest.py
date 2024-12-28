import flet as ft
import os

def main(page: ft.Page):
    boton_abrir_carpeta = ft.ElevatedButton("Abrir carpeta", icon=ft.icons.FOLDER_OPEN)
    boton_pegar_enlace = ft.ElevatedButton("Pegar enlace", icon=ft.icons.PASTE)
    boton_configuraciones = ft.ElevatedButton("Configuraciones", icon=ft.icons.SETTINGS)

    mensaje = ft.Text()

    # Layout principal
    page.add(
        ft.Row(
            controls=[
                ft.Row(
                    controls=[boton_abrir_carpeta, boton_pegar_enlace],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[boton_configuraciones],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )

ft.app(target=main)
    