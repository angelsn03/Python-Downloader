import flet as ft

def show_dialog(page: ft.Page, message: str, title: str):
    """Mostrar un mensaje de error si no hay enlace en el portapapeles."""
    def close_dialog(e):
        page.dialog.open = False
        page.update()

    error_dialog = ft.AlertDialog(
        title=ft.Text(title, weight="bold"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=close_dialog)
        ],
        on_dismiss=close_dialog,
    )
    page.dialog = error_dialog
    error_dialog.open = True
    page.update()
